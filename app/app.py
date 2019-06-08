from flask import render_template, request, redirect, url_for, Flask
import logging.config
from src.clean_data import preprocess, remove_stop_words, get_lemmatized_text
import pandas as pd
import pickle
#from app import db, app
#from app.models import Track

# Define LOGGING_CONFIG in config.py - path to config file for setting up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig('../config/logging/local.conf')
logger = logging.getLogger("whos-the-boss")
logger.debug('Test log')

app = Flask(__name__, template_folder='templates')

# Configure flask app from flask_config.py
app.config.from_pyfile('../config/flask_config.py')


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


def tfidf_vector(text, path, s3=False, bucket=None):
    """Vectorize the line using tfidf_vectorizer

            Args:
                lines_text (list): processed line
                path (string): Path from which the vectorizer should be loaded
                s3 (boolean): Load from S3 or not
                bucket (string): Name of bucket to be loaded from

            Returns:
                matrix with vectorized lines
    """
    vectorizer = pickle.load(open(path, 'rb'))
    X = vectorizer.transform(text)

    return X


def predict_class(X, path, s3=False, bucket=None):
    """Predict class for given text

        Args:
            X (matrix): vectorized line
            path (string): Path from which the model should be loaded
            s3 (boolean): Load from S3 or not
            bucket (string): Name of bucket to be loaded from

        Returns:
            Prediction (string)
    """
    model = pickle.load(open(path, 'rb'))
    prediction = model.predict(X)

    return prediction


@app.route('/', methods=['GET', 'POST'])
def main():

    if request.method == 'GET':
        return render_template('main.html')
    if request.method == 'POST':
        statement = request.form['statement']

        processed = process_data(statement)
        processed = tfidf_vector(processed, path='../models/tfidf_vectorizer.pkl')

        prediction = predict_class(processed, path='../models/model.pkl')

        return render_template('main.html', original_input=statement, result=prediction, )


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], port=app.config['PORT'], host=app.config['HOST'])


# @app.route('/')
# def index():
#     """Main view that lists songs in the database.
#
#     Create view into index page that uses data queried from Track database and
#     inserts it into the msiapp/templates/index.html template.
#
#     Returns: rendered html template
#
#     """
#
#     try:
#         tracks = Track.query.all()
#         logger.debug("Index page accessed")
#         return render_template('index.html', tracks=tracks)
#     except:
#         logger.warning("Not able to display tracks, error page returned")
#         return render_template('error.html')
#
#
# @app.route('/add', methods=['POST'])
# def add_entry():
#     """View that process a POST with new song input
#
#     :return: redirect to index page
#     """
#
#     try:
#         track1 = Track(artist=request.form['artist'], album=request.form['album'], title=request.form['title'])
#         db.session.add(track1)
#         db.session.commit()
#         logger.info("New song added: %s by %s", request.form['title'], request.form['artist'])
#         return redirect(url_for('index'))
#     except:
#         logger.warning("Not able to display tracks, error page returned")
#         return render_template('error.html')
#
#
# if __name__ == "__main__":
#     app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
