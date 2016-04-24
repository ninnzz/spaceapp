import requests

from geopy.geocoders import Nominatim

# Import global context
from flask import request

# Import flask dependencies
from flask import Blueprint

# Import app-based dependencies
from app import app, gateway, air_check
from util import utils

# Import core libraries
from lib.decorators import make_response
from lib.error_handler import FailedRequest


# Get config
config = app.config

# Define the blueprint: 'gateway', set its url prefix: app.url/gateway
mod_gateway = Blueprint('gateway', __name__)

geolocator = Nominatim()

# Declare all the routes
@mod_gateway.route('/subscribe', methods=['GET'])
@make_response
def gateway_all(res):
    """gateway all tracks

    Keyword arguments:
    res -- instance of Response class
    """

    params = utils.get_data(['access_token', 'subscriber_number'], [], request.args)

    result = gateway.store_mobile_info(params)

    if not result:
        raise FailedRequest('Cannot do that. Sorry :(', 403)

    return res.send(request.args)


@mod_gateway.route('/', methods=['POST'])
@make_response
def receive_message(res):
    """autocomplete gateway query

    Keyword arguments:
    res -- instance of Response class
    """
    help_msg =  'AirVironment allows everyone to submit a rating for  air quality of a place.\n\n'
    help_msg += 'All ratings are on a 1-10 scale, 10 being the highest\n'
    help_msg += 'Just send: do rating <air quality>, <coughing>,  <shortness of breath>, <sneezing> @ <location>\n'
    help_msg += 'Example: do rating 8,7,6,6 @ eastwood quezon city philippines'

    invalid_location = 'Sorry, we cannot find that location'
    success_msg = 'The monkeys are now processing your feedback! The average air quality in your place is 0! '

    notify_url = 'http://6848a814.ngrok.io/gateway/'
    
    request_body = request.get_json(force=True)
    request_body = request_body['inboundSMSMessageList']
    msg = request_body['inboundSMSMessage'][0]['message']
    msg_id = request_body['inboundSMSMessage'][0]['messageId']
    sender = request_body['inboundSMSMessage'][0]['senderAddress'].strip()
    msg = msg.strip()

    sender = gateway.get_sender_info(sender)
    if not len(sender):
        raise FailedRequest('No record of you. Sorry :(', 403)
    sender = sender[0]

    payload = {
        'address': sender['mobile_number'],
        'clientCorrelator': '00100',
        'senderAddress': 'tel:' + config['GOBE_NUMBER_SUFF'],
        'message': ''
    }
    endpoint = config['GLOBE_SMS_ENDPOINT'].format(sender['access_token'])
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }

    # Keyword submit rating
    if msg.lower() == 'how to':
        payload['message'] = help_msg
        r = requests.post(
            endpoint, 
            data=payload,
            headers=headers
        )

    elif msg.startswith('do rating'):
        full_location = msg.split('@')
        rating_data = full_location[0].lstrip('do rating').strip()
        full_location = full_location[1].strip()
        
        rating = rating_data.split(',')
        location = geolocator.geocode(full_location, language='en', exactly_one=True, addressdetails=True)
        
        if not location:
            payload['message'] = invalid_location
            r = requests.post(
                endpoint, 
                data=payload,
                headers=headers
            )
            return res.send('ok')


        longitude = location.longitude
        latitude = location.latitude

        # averages = gateway.get_data_by_point(longitude, latitude, 10)
        cols =  '''
                    `country`, `state`, `raw_location`, `longitude`,
                    `latitude`, `air_pollution`, `caugh`, `shortness_of_breath`,
                    `sneezing`, `source`, `mobile_number`
                '''
        air_check_data = [
            location.raw['address']['country'],
            location.raw['address']['country_code'],
            location.address,
            longitude,
            latitude,
            rating[0].strip(),
            rating[1].strip(),
            rating[2].strip(),
            rating[3].strip(),
            'sms.globe',
            sender['mobile_number']
        ]

        air_check_data = [tuple(air_check_data)]
        to_insert = air_check.add_data(cols, air_check_data)

        payload['message'] = success_msg + 'Location: {}'.format(
            location.address)

        r = requests.post(
            endpoint, 
            data=payload,
            headers=headers
        )
        print(r.text)
        print(r.status_code)

    return res.send('ok')
