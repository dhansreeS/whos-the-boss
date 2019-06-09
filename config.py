from os import path
PROJECT_HOME = path.dirname(path.abspath(__file__))
DEBUG = True
LOGGING_CONFIG = path.join(PROJECT_HOME, 'config/logging/local.conf')

HOST = '127.0.0.1'
PORT = 9033
APP_NAME = 'whos-the-boss'

# all configurations
CONFIG_FILE = path.join(PROJECT_HOME, 'config/config.yml')

