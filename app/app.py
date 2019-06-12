from flask import render_template, request, redirect, url_for, Flask
import logging.config
import pandas as pd
import pickle
import os
from os import path
import sys
import datetime
from flask_sqlalchemy import SQLAlchemy
import yaml
import boto3
import io

rel_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(rel_path)

from src.clean_data import preprocess, remove_stop_words, get_lemmatized_text
from src.data_model import UserLines
import config

# Define LOGGING_CONFIG in config.py - path to config file for setting up the logger (e.g. config/logging/local.conf)
logger = logging.getLogger("whos-the-boss")
logger.debug('Test log')

app = Flask(__name__, template_folder='templates')

# Configure flask app from flask_config.py
app.config.from_pyfile('../config/flask_config.py')

try:
    with open(config.CONFIG_FILE, 'r') as f:
        config = yaml.load(f)
except FileNotFoundError:
    logger.error('config YAML File not Found')
    sys.exit(1)

if app.config['USE_RDS']:
    aws_config = config['rds']

    conn_type = aws_config['CONN_TYPE']
    host = aws_config['HOST_NAME']
    port = aws_config['PORT_NO']
    database = aws_config['DATABASE_NAME']
    user = os.environ.get('MYSQL_USER')
    password = os.environ.get('MYSQL_PASSWORD')

    app.config['SQLALCHEMY_DATABASE_URI'] = '{}://{}:{}@{}:{}/{}'. \
        format(conn_type, user, password, host, port, database)

db = SQLAlchemy(app)


def process_data(new_line):
    """Process the new line entered
        Args:
            new_line (string): String to be processed before being scored

        Returns:
            new_line processed (string)
    """

    new = []
    new.append(new_line)
    new_df = pd.DataFrame(new, columns=['line_text'])

    processed = preprocess(new_df['line_text'])
    processed = remove_stop_words(processed)
    processed = get_lemmatized_text(processed)

    return processed


@app.route('/', methods=['GET', 'POST'])
def main():
    """Main view that shows the text box for input and displays the prediction results in a separate div"""
    try:
        if request.method == 'GET':
            return render_template('main.html')
        if request.method == 'POST':
            time_db = datetime.datetime.now()
            statement = str(request.form['statement'])

            processed = process_data(statement)
            # load models - tfidf

            if app.config['USE_S3']:
                s3 = boto3.resource('s3')
                with io.BytesIO() as data:
                    s3.Bucket(app.config['DEST_S3_BUCKET']).download_fileobj(app.config['S3_TFIDF'], data)
                    data.seek(0)  # move back to the beginning after writing
                    vectorizer = pickle.load(data)
                with io.BytesIO() as data2:
                    s3.Bucket(app.config['DEST_S3_BUCKET']).download_fileobj(app.config['S3_MODEL'], data2)
                    data2.seek(0)  # move back to the beginning after writing
                    model = pickle.load(data2)
            else:
                vectorizer = pickle.load(open(app.config['TFIDF_PATH'], 'rb'))
                model = pickle.load(open(app.config['MODEL_PATH'], 'rb'))

            processed = vectorizer.transform(processed)

            prediction = model.predict(processed)

            if prediction == 0:
                prediction = "Dwight"
            else:
                prediction = "Michael"

            try:
                user_input = UserLines(user_text=statement, predicted=prediction, time=time_db)
                db.session.add(user_input)
                db.session.commit()
                logger.info('New user input added')

            except Exception as e:
                logger.warning(e)
                sys.exit(5)

            prob_pred = model.predict_proba(processed)

            mike = "{0:.0f}%".format(prob_pred[0][1]*100)
            dwight = "{0:.0f}%".format(prob_pred[0][0]*100)

            logger.info('Prediction made and updated.')

            return render_template('main.html', original_input=statement, result={'Michael':mike,
                                                         'Dwight':dwight}, )

    except:
        logger.warning('Error raised while rendering template.')

        return render_template('error.html')


def start_app(args):
    """Start application and choose to store user input in sqlite or rds
        Args:
            args: arguments including app specific configurations and specifications

        Returns:
            NA
    """
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'], host=app.config['HOST'])
