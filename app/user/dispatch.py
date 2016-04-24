# Import global context
from flask import request

# Import flask dependencies
from flask import Blueprint

# Import app-based dependencies
from app import app, auth, music_provider, user
from util import utils

# Import core libraries
from lib.decorators import check_tokens, make_response
from lib.error_handler import FailedRequest

# Other imports
from datetime import datetime
from werkzeug import secure_filename


# Get config
config = app.config
db = app.db

# Define the blueprint: 'user', set its url prefix: app.url/user
mod_user = Blueprint('user', __name__)


# Declare all the routes

@mod_user.route('/', methods=['GET'])
@mod_user.route('/<user_id>', methods=['GET'])
@check_tokens
@make_response
def get_user(res, user_id=None):
    """get user information

    Keyword arguments:
    res -- instance of Response class
    user_id --  id of user (default None)
    """

    if not user_id:
        if not utils.has_scopes(db, request.user_id, 'self.info'):
            raise FailedRequest(config['ERROR']['permission'], 403)

    elif not utils.has_scopes(db, request.user_id, 'user.info'):
        raise FailedRequest(config['ERROR']['permission'], 403)

    user_id = user_id or request.user_id
    result = user.get_user(user_id)

    if result['role'] == 'music_provider' or result['role'] == 'admin':
        music_providers = music_provider.get_user_music_providers(user_id)
        result['music_providers'] = music_providers

    elif result['role'] == 'artist':
        artist = user.get_user_artist(user_id)
        result['artist'] = artist['results'][0]

    elif result['role'] == 'user':
        invitations = user.get_user_invitations(result['email'])
        result['invitations'] = invitations

    return res.send(result)


@mod_user.route('/all', methods=['GET'])
@check_tokens
@make_response
def get_all_users(res):
    """get all users information sorted by email

    Keyword arguments:
    res -- instance of Response class
    """

    if not utils.has_scopes(db, request.user_id, 'user.list'):
        raise FailedRequest(config['ERROR']['permission'], 403)

    params = utils.get_data([], ['page', 'entries'], request.args)

    result = user.get_all_users(params)

    return res.send(result)


@mod_user.route('/auto', methods=['GET'])
@check_tokens
@make_response
def autocomplete_users(res):
    if not utils.has_scopes(db, request.user_id, 'user.available.list'):
        raise FailedRequest(config['ERROR']['permission'], 403)

    params = utils.get_data(['query'], ['entries'], request.args)

    params['entries'] = int(params['entries'] or config['ENTRIES'])

    result = user.autocomplete_users(params)

    return res.send(result)


@mod_user.route('/applications/csv', methods=['GET'])
@check_tokens
@make_response
def export_applications_csv(res):
    if not utils.has_scopes(db, request.user_id, 'user.info'):
        raise FailedRequest(config['ERROR']['permission'], 403)

    secret_id = request.mida + '.' + request.access_token

    return res.send('/user/applications/secret/' + secret_id)


@mod_user.route('/applications/secret/<secret_id>', methods=['GET'])
@make_response
def export_applications(res, secret_id):
    utils.check_tokens(db, config, secret_id)

    result = user.export_applications()

    timestamp = datetime.now()

    res.set_header('Content-Disposition', 'attachment; \
        filename=%s_Artist_Applications.csv' % timestamp.strftime('%Y%m%d'))

    return res.stream(utils.generate_csv_content(result), mimetype='text/csv')


@mod_user.route('/contract', methods=['GET'])
@check_tokens
@make_response
def get_contract(res):
    if not utils.has_scopes(db, request.user_id, 'self.info'):
        raise FailedRequest(config['ERROR']['permission'], 403)

    application_status = user.get_user(request.user_id)['application_status']

    if application_status != 'applied':
        raise FailedRequest(config['ERROR']['permission'], 403)

    result = user.get_contract()

    return res.send(result)


@mod_user.route('/search', methods=['GET'])
@check_tokens
@make_response
def search_users(res):
    if not utils.has_scopes(db, request.user_id, 'user.list'):
        raise FailedRequest(config['ERROR']['permission'], 403)

    params = utils.get_data(['query'], ['page', 'entries'], request.args)

    result = user.search_users(params)

    return res.send(result)


@mod_user.route('/tracks', methods=['GET'])
@check_tokens
@make_response
def get_user_tracks(res):
    if not utils.has_scopes(db, request.user_id, 'user.music.list'):
        raise FailedRequest(config['ERROR']['permission'], 403)

    params = utils.get_data([], ['page', 'entries'], request.args)

    params['user_id'] = request.user_id

    result = user.get_user_tracks(params)

    return res.send(result)


@mod_user.route('/tracks/flagged', methods=['GET'])
@check_tokens
@make_response
def get_user_flagged_tracks(res):
    if not utils.has_scopes(db, request.user_id, 'user.music.list'):
        raise FailedRequest(config['ERROR']['permission'], 403)

    params = utils.get_data([], ['page', 'entries'], request.args)

    params['user_id'] = request.user_id

    result = user.get_user_flagged_tracks(params)

    return res.send(result)


@mod_user.route('/', methods=['POST'])
@mod_user.route('/<user_id>', methods=['POST'])
@check_tokens
@make_response
def edit_user(res, user_id=None):
    """edit user information

    Keyword arguments:
    res -- instance of Response class
    user_id --  id of user to be edited (default None)
    """

    if not user_id:
        if not utils.has_scopes(db, request.user_id, 'self.info'):
            raise FailedRequest(config['ERROR']['permission'], 403)

        user_id = request.user_id

        params = utils.get_data([], ['genre', 'mood', 'instrument',
                                     'picture'], request.values)

    else:
        if not utils.has_scopes(db, request.user_id, 'user.info'):
            raise FailedRequest(config['ERROR']['permission'], 403)

        params = utils.get_data(['active'], [], request.values)

    params['user_id'] = user_id

    if 'active' in params:
        user.edit_user_active(params)

    else:
        user_image = request.files.get('image')

        if user_image and utils.is_file_type(user_image.filename,
                                             user_image.mimetype, 'image'):
            params.update({
                'image': user_image,
                'image_filename': secure_filename(user_image.filename)
            })
            user.edit_user_picture(params)

        user.edit_user_preference(params)

    result = dict(params)
    result.pop('image', None)

    return res.send(result)


@mod_user.route('/accept', methods=['POST'])
@check_tokens
@make_response
def accept_invitation(res):
    if not utils.has_scopes(db, request.user_id, 'self.info'):
        raise FailedRequest(config['ERROR']['permission'], 403)

    params = utils.get_data(['role'], ['music_provider_id',
                                       'artist_id'], request.values)

    params['user_id'] = request.user_id
    user.accept_invitation(params)

    return res.send(params)


@mod_user.route('/apply', methods=['POST'])
@check_tokens
@make_response
def apply(res):
    if not utils.has_scopes(db, request.user_id, 'self.info'):
        raise FailedRequest(config['ERROR']['permission'], 403)

    application_status = user.get_user(request.user_id)['application_status']

    if application_status != 'applied':
        raise FailedRequest(config['ERROR']['permission'], 403)

    params = utils.get_data(['contract_id', 'original_music', 'name', 'source'],
                            ['skype', 'genre', 'music_location'],
                            request.values)

    params['user_id'] = request.user_id

    user.apply(params)

    return res.send(params)


@mod_user.route('/decline', methods=['POST'])
@check_tokens
@make_response
def decline_invitation(res):
    if not utils.has_scopes(db, request.user_id, 'self.info'):
        raise FailedRequest(config['ERROR']['permission'], 403)

    params = utils.get_data(['role'], ['music_provider_id',
                                       'artist_id'], request.values)

    params['user_id'] = request.user_id
    user.decline_invitation(params)

    return res.send(params)


@mod_user.route('/<user_id>', methods=['DELETE'])
@check_tokens
@make_response
def delete_user(res, user_id):
    """delete a user, set active to 0

    Keyword arguments:
    res -- instance of Response class
    user_id --  id of user to be deleted
    """

    if not utils.has_scopes(db, request.user_id, 'user.delete'):
        raise FailedRequest(config['ERROR']['permission'], 403)

    user.delete_user(user_id)

    auth.remove_scopes(user_id)
    auth.remove_session(user_id)

    return res.send('User deleted')
