# Import global context
from flask import current_app as app, request

# Import app-based dependencies
from util import utils

# Import core libraries
from lib import database
from lib.error_handler import FailedRequest
from lib.response import Response

# Other imports
from functools import wraps
from threading import Thread


def async(f):

    def wrapper(*args, **kwds):
        return app.pool.apply_async(f, args=args, kwds=kwds)

    return wrapper


def async_threaded(f):

    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


def check_tokens(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = request.headers.get('Access-Token')
        mida = request.headers.get('mida')
        request.user_id = None
        request.artist_id = None
        request.music_provider_id = None
        request.is_admin = False

        if mida and access_token:
            data = database.get(
                app.db.music_db,
                '''
                    SELECT  *
                    FROM    session s
                            JOIN    users u
                            ON      s.user_id = u.user_id
                    WHERE   mida = :mida
                ''',
                {'mida': mida}
            )

            if not data or utils.mida(access_token) != mida:
                raise FailedRequest('Session expired', 401)

            request.user_id = data[0]['user_id']
            request.is_admin = data[0]['role'] == 'admin'
            request.mida = mida
            request.access_token = access_token
            music_provider_name = request.headers.get('music-provider-name')

            if not music_provider_name:
                if data[0]['role'] != 'artist':
                    return func(*args, **kwargs)

                filters = {
                    'term': {
                        'user_id': request.user_id
                    }
                }
                data = app.elastic_search.filter('artists', filters, 1)

                request.artist_id = data['results'][0]['artist_id']

                return func(*args, **kwargs)

            filters = {
                'exists': {
                    'field': 'users.' + request.user_id
                }
            }
            queries = [
                {
                    'key': 'music-provider-name',
                    'value': music_provider_name
                }
            ]
            data = app.elastic_search.filter('music_providers', filters, 1,
                                             queries=queries)

            if not data['results']:
                raise FailedRequest('Invalid music_provider_name', 400)

            request.music_provider_id = data['results'][0]['id']

            return func(*args, **kwargs)

        elif mida or access_token:
            raise FailedRequest('Session expired', 401)

        else:
            return func(*args, **kwargs)

    return wrapper


def make_response(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        response = Response()
        response.set_header('nida', utils.nida())

        return func(res=response, *args, **kwargs)

    return wrapper
