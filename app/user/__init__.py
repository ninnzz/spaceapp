# Import app-based dependencies
from app import app, auth, music_provider, artist
from util import utils

# Import core libraries
from lib import database
from lib.error_handler import FailedRequest
from lib.uploader import Uploader

# Other imports
from datetime import datetime


config = app.config
db = app.db
elastic_search = app.elastic_search


def accept_invitation(_params):
    data = get_user(_params['user_id'])

    _params['email'] = data['email']
    mp_op = '=' if _params['music_provider_id'] else 'IS'
    a_op = '=' if _params['artist_id'] else 'IS'

    data = database.get(
        db.music_db,
        '''
            SELECT  *
            FROM    user_invites
            WHERE   email = :email
                    AND role = :role
                    AND music_provider_id %s :music_provider_id
                    AND artist_id %s :artist_id
        ''' % (mp_op, a_op),
        _params
    )

    if not data:
        raise FailedRequest('Invalid parameters', 400)

    if _params['role'] == 'artist':
        database.query(
            db.music_db,
            '''
                UPDATE  artists
                SET     user_id = :user_id
                WHERE   artist_id = :artist_id
                LIMIT   1
            ''',
            _params
        )

        elastic_search.update_from_index('artists', 'artist',
                                         _params['artist_id'],
                                         ['user_id', 'email'], _params)

        database.query(
            db.music_db,
            '''
                DELETE FROM user_invites
                WHERE       artist_id = :artist_id
            ''',
            _params
        )

    else:
        database.query(
            db.music_db,
            '''
                INSERT IGNORE INTO music_provider_owners_managers
                VALUES (
                    :user_id,
                    :music_provider_id,
                    :role
                )
            ''',
            _params
        )

        data = music_provider.get_music_provider(_params['music_provider_id'])

        _params['users'] = data['users']
        _params['users'][_params['user_id']] = _params['role']

        elastic_search.update_from_index('music_providers', 'music_provider',
                                         _params['music_provider_id'],
                                         ['users'], _params)

        database.query(
            db.music_db,
            '''
                DELETE FROM user_invites
                WHERE       music_provider_id = :music_provider_id
            ''',
            _params
        )

    if _params['role'] != 'artist':
        _params['role'] = 'music_provider'

    database.query(
        db.music_db,
        '''
            UPDATE  users
            SET     role = :role
            WHERE   user_id = :user_id
            LIMIT   1
        ''',
        _params
    )

    elastic_search.update_from_index('users', 'user', _params['user_id'],
                                     ['role'], _params)

    _params['scopes'] = config['SCOPES'][_params['role']]

    auth.remove_scopes(_params['user_id'])
    auth.add_scopes(_params)

    database.query(
        db.music_db,
        '''
            DELETE FROM user_invites
            WHERE       email = :email
        ''',
        _params
    )


def add_user(_params):
    """add user information to database servers

    Keyword arguments:
    _params includes:
        email -- email of user
        role -- role of user
        user_id -- id of user
    """

    _params.update({
        'active': 1,
        'rank': 0,
        'picture': None,
        'genre': [],
        'mood': [],
        'instrument': [],
        'skype': None,
        'date_created': datetime.now(),
        'date_updated': None
    })

    database.query(
        db.music_db,
        '''
            INSERT INTO users
            VALUES (
                :user_id,
                :email,
                :name,
                :active,
                :rank,
                :role,
                :picture,
                :skype,
                :application_status,
                :date_created,
                :date_updated
            )
        ''',
        _params
    )

    database.query(
        db.music_db,
        '''
            INSERT INTO user_preferences (
                user_id
            )
            VALUES (
                :user_id
            )
        ''',
        _params
    )

    elastic_search.add_to_index('users', 'user', _params, _params['user_id'],
                                config['ES']['user_cols'])


def apply(_params):
    _params.update({
        'artist_id': utils.generate_UUID(),
        'application_id': 0,
        'application_status': 'accepted',
        'agree_on_contract': 'yes',
        'picture': None,
        'rating': None,
        'music_provider_id': config['DEFAULT_MUSIC_PROVIDER'],
        'date_applied': datetime.now(),
        'date_approved': None,
        'date_created': datetime.now(),
        'date_updated': None
    })

    artist.process_artist_params(_params, True)

    artist.insert_artist(_params)

    database.query(
        db.music_db,
        '''
            INSERT INTO applications
            VALUES (
                :application_id,
                :user_id,
                :contract_id,
                :agree_on_contract,
                :source,
                :date_applied,
                :date_approved,
                :date_created,
                :date_updated
            )
        ''',
        _params
    )

    database.query(
        db.music_db,
        '''
            UPDATE  users
            SET     skype = :skype,
                    application_status = :application_status
            WHERE   user_id = :user_id
            LIMIT   1
        ''',
        _params
    )

    elastic_search.update_from_index('users', 'user', _params['user_id'],
                                     ['skype', 'application_status'], _params)


def autocomplete_users(_params):
    query = {
        'key': 'email',
        'value': _params['query']
    }
    filters = {
        'term': {
            'role': 'user'
        }
    }

    users = elastic_search.search('users', query, _params['entries'],
                                  filters=filters)

    return [data['email'] for data in users['results']]


def decline_invitation(_params):
    data = get_user(_params['user_id'])

    _params['email'] = data['email']
    mp_op = '=' if _params['music_provider_id'] else 'IS'
    a_op = '=' if _params['artist_id'] else 'IS'

    database.query(
        db.music_db,
        '''
            DELETE FROM user_invites
            WHERE       email = :email
                        AND role = :role
                        AND music_provider_id %s :music_provider_id
                        AND artist_id %s :artist_id
        ''' % (mp_op, a_op),
        _params
    )


def delete_user(user_id):
    """delete user from elastic search index, set active to 0 in mysql

    Keyword arguments:
    _params includes:
        user_id -- id of user
    """

    get_user(user_id)

    database.query(
        db.music_db,
        '''
            UPDATE  users
            SET     active = 0
            WHERE   user_id = :user_id
            LIMIT   1
        ''',
        {'user_id': user_id}
    )

    elastic_search.delete_from_index('users', 'user', user_id)


def edit_user_preference(_params):
    """edit user preferences

    Keyword arguments:
    _params includes:
        genre -- genre preferences of user (default None)
        instrument -- instrument preferences of user (default None)
        mood -- mood preferences of user (default None)
    """

    get_user(_params['user_id'])

    for category in ['genre', 'instrument', 'mood']:
        if not _params[category]:
            continue

        results = []
        for preference in utils.split(_params[category], ','):
            results.append(preference)

        data = elastic_search.multi_get(category + 's', key='name',
                                        values=results)

        results = [row['name'] for row in data]
        _params[category] = ','.join(results) or None

    database.query(
        db.music_db,
        '''
            UPDATE  user_preferences
            SET     genre = :genre,
                    mood = :mood,
                    instrument = :instrument
            WHERE   user_id = :user_id
            LIMIT   1
        ''',
        _params
    )

    _params.update({
        'genre': utils.split(_params['genre'], ','),
        'instrument': utils.split(_params['instrument'], ','),
        'mood': utils.split(_params['mood'], ',')
    })

    elastic_search.update_from_index('users', 'user', _params['user_id'],
                                     ['genre', 'mood', 'instrument'], _params)


def edit_user_active(_params):
    """edit user preferences

    Keyword arguments:
    _params includes:
        active -- activity state of user
        user_id -- id of user
    """

    if _params['active'] not in ['0', '1']:
        raise FailedRequest('Invalid active', 400)

    get_user(_params['user_id'])

    _params['active'] = int(_params['active'])

    database.query(
        db.music_db,
        '''
            UPDATE  users
            SET     active = :active
            WHERE   user_id = :user_id
            LIMIT   1
        ''',
        _params
    )

    elastic_search.update_from_index('users', 'user', _params['user_id'],
                                     ['active'], _params)


def edit_user_picture(_params):
    """edit user picture

    Keyword arguments:
        _params includes:
            picture -- picture of user
    """

    data = get_user(_params['user_id'])

    file_ext = _params['image_filename'][_params['image_filename'].rfind('.'):]
    new_filename = _params['user_id'] + file_ext

    path = '/'.join([
        utils.hash_string(data['email']),
        utils.generate_filename(new_filename)
    ])

    _params['picture'] = '/'.join([
        app.config['CLOUDFRONT_URL'],
        'users',
        path
    ])

    uploader = Uploader(config)
    uploader.upload_image('users', path, _params['image'].read())

    database.query(
        db.music_db,
        '''
            UPDATE  users
            SET     picture = :picture
            WHERE   user_id = :user_id
            LIMIT   1
        ''',
        _params
    )

    elastic_search.update_from_index('users', 'user', _params['user_id'],
                                     ['picture'], _params)


def export_applications():
    applications = database.get(
        db.music_db,
        '''
            SELECT  agree_on_contract,
                    source,
                    date_applied,
                    email,
                    ar.name AS artist_name,
                    skype,
                    ar.genre,
                    original_music,
                    music_location,
                    c.name AS contract_name,
                    c.type AS contract_type,
                    c.version AS contract_version,
                    c.date_effective
            FROM    applications a
                    LEFT OUTER JOIN users u
                    ON              u.user_id = a.user_id
                    LEFT OUTER JOIN artists ar
                    ON              u.user_id = ar.user_id
                    LEFT OUTER JOIN contracts c
                    ON              c.contract_id = a.contract_id
            WHERE   date_approved IS NULL
        '''
    )

    data = [('Artist Name', 'Email', 'Skype', 'Original Music',
             'Music Location', 'Genre', 'Source', 'Date Applied',
             'Agree on Contract', 'Contract Name', 'Type', 'Version',
             'Date Effective')]

    for a in applications:
        data.append((a['artist_name'], a['email'], a['skype'],
                     a['original_music'], a['music_location'], a['genre'],
                     a['source'], a['date_applied'], a['agree_on_contract'],
                     a['contract_name'], a['contract_type'],
                     a['contract_version'], a['date_effective']))

    return data


def get_all_users(_params):
    """get all users

    Keyword arguments:
    _params includes:
        picture -- picture of user
    """

    _params = utils.update_pagination_params(config, _params)
    start = (_params['page'] - 1) * _params['entries']
    sort_by_email = {
        'email.raw': {
            'order': 'asc',
            'ignore_unmapped': True
        }
    }

    data = elastic_search.get_all('users', _params['entries'], start,
                                  sort_by_email)

    return utils.get_pagination_results(_params, data)


def get_contract():
    data = database.get(
        db.music_db,
        '''
            SELECT      *
            FROM        contracts
            WHERE       type = "artist_contract"
            ORDER BY    version DESC
            LIMIT       1
        '''
    )

    return data[0]


def get_user(user_id, raise_exception=True):
    """get user

    Keyword arguments:
    user_id -- id of user
    """

    data = elastic_search.get('users', 'user', user_id)

    if not data:
        if raise_exception:
            raise FailedRequest('Invalid user_id', 400)

        return {}

    return data


def get_user_artist(user_id):
    filters = {
        'term': {
            'user_id': user_id
        }
    }

    return elastic_search.filter('artists', filters, 1)


def get_user_flagged_tracks(_params):
    get_user(_params['user_id'])

    _params = utils.update_pagination_params(config, _params)
    _params['start'] = (_params['page'] - 1) * _params['entries']

    count = database.get(
        db.music_db,
        '''
            SELECT  COUNT(*) AS total
            FROM    flagged_tracks
            WHERE   user_id = :user_id
        ''',
        _params
    )

    data = database.get(
        db.music_db,
        '''
            SELECT  t.*,
                    ar.name AS artist,
                    al.name AS album,
                    al.cover AS album_cover
            FROM    track_upload_to_youtube_requests t
                    LEFT OUTER JOIN artists ar
                    ON              t.artist_id = ar.artist_id
                    LEFT OUTER JOIN albums al
                    ON              t.album_id = al.album_id
                                    AND ar.artist_id = al.artist_id
            LIMIT   :start, :entries
        ''',
        _params
    )

    data = {
        'results': data,
        'total': count[0]['total']
    }

    return utils.get_pagination_results(_params, data)


def get_user_invitations(email):
    data = database.get(
        db.music_db,
        '''
            SELECT  ui.*,
                    a.name AS artist,
                    mp.name AS music_provider
            FROM    user_invites ui
                    LEFT OUTER JOIN artists a
                    ON              ui.artist_id = a.artist_id
                    LEFT OUTER JOIN music_providers mp
                    ON              ui.music_provider_id = mp.id
            WHERE   ui.email = :email
        ''',
        {'email': email}
    )

    return data


def get_user_tracks(_params, status=None):
    get_user(_params['user_id'])

    _params = utils.update_pagination_params(config, _params)
    start = (_params['page'] - 1) * _params['entries']
    filters = {
        'and': [
            {
                'term': {
                    'user_id': _params['user_id']
                }
            },
            {
                'missing': {
                    'field': 'music_provider_id'
                }
            }
        ]
    }
    sort_by_title = {
        'title.raw': {
            'order': 'asc',
            'ignore_unmapped': True
        }
    }

    data = elastic_search.filter('tracks', filters, _params['entries'], start,
                                 sort_by_title, status)

    return utils.get_pagination_results(_params, data)


def search_users(_params):
    _params = utils.update_pagination_params(config, _params)
    start = (_params['page'] - 1) * _params['entries']

    query = {
        'key': 'email',
        'value': _params['query']
    }

    data = elastic_search.search('users', query, _params['entries'], start)

    return utils.get_pagination_results(_params, data)


def update_user(_params):
    get_user(_params['user_id'])

    database.query(
        db.music_db,
        '''
            UPDATE  users
            SET     name = :name,
                    application_status = :application_status
            WHERE   user_id = :user_id
            LIMIT   1
        ''',
        _params
    )

    elastic_search.update_from_index('users', 'user', _params['user_id'],
                                     ['name', 'application_status'], _params)


def user_exists(email):
    """check if user exists

    Keyword arguments:
    email -- email of user
    """

    return elastic_search.get('users', key='email', value=email)
