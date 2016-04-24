# Import app-based dependencies
from app import app
from util import utils
from lib import database
from nmi_mysql import nmi_mysql

config = app.config


def store_mobile_info(_params):

    query = '''
                INSERT INTO mobile_nums 
                    (`mobile_number`, `access_token`)
                    VALUES(%s, %s)
            '''

    _params['subscriber_number'] = 'tel:+63' + _params['subscriber_number']

    db = nmi_mysql.DB(config['MYSQL_SPACEAPP'], True)
    result = db.query(query, 
        [
            _params['subscriber_number'],
            _params['access_token']
        ]
    )
    db.close()

    if result['affected_rows'] == 0:
        return False

    return True


def get_sender_info(_number):

    db = nmi_mysql.DB(config['MYSQL_SPACEAPP'], True)
    result = db.query('SELECT * FROM mobile_nums WHERE mobile_number = %s', 
        [_number]
    )
    db.close()

    return result