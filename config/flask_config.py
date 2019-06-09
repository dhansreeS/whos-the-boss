from os import path
from config import PROJECT_HOME
DEBUG = False
LOGGING_CONFIG = "config/logging/local.conf"

HOST = '127.0.0.1'
PORT = 9033
APP_NAME = 'whos-the-boss'

USE_S3 = True

USE_RDS = True
DB_PATH = path.join(PROJECT_HOME, 'data/msia423.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DB_PATH)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed

# Paths
TFIDF_PATH = path.join(PROJECT_HOME, 'models/tfidf_vectorizer.pkl')
MODEL_PATH = path.join(PROJECT_HOME, 'models/model.pkl')

# S3 model, bucket, tfidf_vectorizer
S3_MODEL = 'models/model.pkl'
S3_TFIDF = 'models/tfidf_vectorizer.pkl'
DEST_S3_BUCKET = 'bucket-boss'

