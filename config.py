from os import path
PROJECT_HOME = path.dirname(path.abspath(__file__))
DEBUG = True
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging/local.conf')

HOST = '127.0.0.1'
PORT = 9033
APP_NAME = 'whos-the-boss'

# database configurations
DATABASE_NAME = 'msia423'   # also update config_aws.yml
DB_PATH = path.join(PROJECT_HOME, 'data/'+DATABASE_NAME+'.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:////{}'.format(DB_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = True

# aws configurations
AWS_CONFIG = path.join(PROJECT_HOME, 'config/config_aws.yml')

