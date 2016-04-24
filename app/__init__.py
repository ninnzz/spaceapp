# Import flask
from flask import Flask
from flask.ext.cors import CORS

# Import core libraries
from lib import database_connection
from lib.database_connection import mod_db_connection
from lib.error_handler import mod_err

# Other imports
from multiprocessing import Pool, Queue


# App declaration
app = Flask(__name__, instance_relative_config=True)

# Configurations
app.config.from_pyfile('config.py')

# Adjust config based on the environment
env = app.config['APP_ENV']
if env == 'stage':
    app.config.from_pyfile('env/staging.py')

elif env == 'prod':
    app.config.from_pyfile('env/production.py')

else:
    app.config.from_pyfile('env/development.py')


CORS(app, allow_headers=app.config['ALLOWED_HEADERS'], origins=app.config[
     'ALLOWED_ORIGINS'], methods=app.config['ALLOWED_METHODS'])

# Error and exception handling
app.register_blueprint(mod_err)

# DB connection
app.register_blueprint(mod_db_connection)

database_connection.add_databases(app.config)
app.db = database_connection.db


# Create queue of Youtube API keys

# Create pool of workers
app.pool = Pool()

# Import blueprints
from app.gateway.dispatch import mod_gateway as gateway_module
from app.air_check.dispatch import mod_air_check as air_check_module


# Register imported blueprints for modules
app.register_blueprint(gateway_module, url_prefix='/gateway')
app.register_blueprint(air_check_module, url_prefix='/records')
