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
    help_msg += 'Just send: do rating <air pollution>, <coughing>,  <shortness of breath>, <sneezing> @ <location>\n'
    help_msg += 'Example: do rating 8,7,6,6 @ eastwood quezon city philippines'

    invalid_location = 'Sorry, we cannot find that location'
    success_msg = 'The monkeys are now processing your feedback! The average air pollution rating in your place is  '
    low_quality = 'Seems there are pollutants causing this, please coordinate with your local government'
    high_quality = 'Wow! Seems you are breathing good air overthere. Lets try to keep it that way by protecting the environment.'

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

        average = 0
        health_index = 0
        _ap_sum = 0
        _ac_sum = 0
        _sb_sum = 0
        _s_sum = 0

        to_average = air_check.get_data_by_point(
            longitude, latitude, 15)

        for item in to_average:
            _ap_sum += item['air_pollution']
            _ac_sum += item['caugh']
            _sb_sum += item['shortness_of_breath']
            _s_sum += item['sneezing']

        if len(to_average) != 0:
            average = _ap_sum / len(to_average)
            health_index += (_ac_sum / len(to_average))
            health_index += (_sb_sum / len(to_average))
            health_index += (_s_sum / len(to_average))
            
            success_msg += str(round(average,2)) + ' of 10!\n\n'

            if average > 6:
                success_msg += low_quality + '\n\n'
            elif average < 4:
                success_msg += high_quality + '\n\n'

            if health_index > 20:
                success_msg += 'We also noticed that there are lots of symptoms of coughing, shortness of breath, sneezing, etc in your area. '
                success_msg += 'It is highly recommended to wear face mask or go to the doctor for checkup. \n\n'

        else:
            success_msg += '"cannot be determine". We are still gathering information about that area.'

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
