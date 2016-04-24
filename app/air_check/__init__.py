# Import app-based dependencies
from app import app
from util import utils

# Import core libraries
from lib import database
from nmi_mysql import nmi_mysql

# Other imports
import math
import os
from datetime import datetime


config = app.config
db = app.db

def get_data_by_point(_long, _lat, km):
    """add an aircheck record entry"""

    miles = float(km) * 0.621371

    query = '''
            SELECT *, ( 
                3959 * acos( 
                    cos( radians(%s) ) * 
                    cos( radians( latitude ) ) * 
                    cos( radians( longitude ) - radians(%s) ) + sin( radians(%s) ) * 
                    sin( radians( latitude ) ) ) 
                ) AS distance 
            FROM air_check_data HAVING distance < %s OR distance IS NULL
        '''

    db = nmi_mysql.DB(config['MYSQL_SPACEAPP'], True)
    result = db.query(query, [_lat, _long, _lat, miles])
    db.close()

    return result


def get_data_by_country(_country):

    query = 'SELECT * FROM air_check_data WHERE LOWER(country) = %s'

    db = nmi_mysql.DB(config['MYSQL_SPACEAPP'], True)
    result = db.query(query, [_country.lower()])
    db.close()

    return result


def add_data(_cols, _data):

    query = 'INSERT INTO air_check_data (' + _cols + ') VALUES(%s)'

    db = nmi_mysql.DB(config['MYSQL_SPACEAPP'], True)
    result = db.query(query, _data)
    db.close()
    
    if result['affected_rows'] == 0:
        raise Exception('Failed to insert')
        
    return result
