# Import global context
from flask import request

# Import flask dependencies
from flask import Blueprint

# Import app-based dependencies
from app import app, air_check
from util import utils

# Import core libraries
from lib.decorators import check_tokens, make_response
from lib.error_handler import FailedRequest

# Other imports
import os

# Get config
config = app.config
db = app.db

# Define the blueprint: 'air_check', set its url prefix: app.url/air_check
mod_air_check = Blueprint('air_check', __name__)


# Declare all the routes

@mod_air_check.route('/', methods=['GET'])
@make_response
def get_data(res):
    """get air_check information"""

    params = utils.get_data(['country'], [], request.args)

    result = air_check.get_data_by_country(params['country'])

    if len(result) == 0:
    	raise FailedRequest('Seems the ninjas cannot find any record. Sorry :(', 404)

    return res.send(result)


@mod_air_check.route('/coordinates', methods=['GET'])
@make_response
def get_data2(res):
    """get air_check information"""

    params = utils.get_data(['lat','lng'], ['distance'], request.args)

    if not params['distance']:
    	params['distance'] = 15 #15KM default

    result = air_check.get_data_by_point(params['lng'], params['lat'], params['distance'])

    if len(result) == 0:
    	raise FailedRequest('Seems the ninjas cannot find any record. Sorry :(', 404)

    return res.send(result)