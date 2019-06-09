from os import path
from config import PROJECT_HOME
DEBUG = False
LOGGING_CONFIG = "config/logging/local.conf"

HOST = '127.0.0.1'
PORT = 9033
APP_NAME = 'whos-the-boss'

USE_RDS = True
DB_PATH = path.join(PROJECT_HOME, 'data/msia423.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DB_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed

# Paths
TFIDF_PATH = path.join(PROJECT_HOME, 'models/tfidf_vectorizer.pkl')
MODEL_PATH = path.join(PROJECT_HOME, 'models/model.pkl')
