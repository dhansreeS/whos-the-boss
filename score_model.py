from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
import os
import boto3
import io
import pickle
import logging.config
#import config
import yaml
import sys
from src.clean_data import preprocess, remove_stop_words, get_lemmatized_text
logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger(__name__)


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


if __name__ == '__main__':

#    statement = 'Best Boss EVER!'
#    statement = 'What can you tell me about the prank in question?'
#    statement = 'Identity theft is not a joke, Jim.'
#    statement = 'How rude!'
#    statement = 'Im calling a meeting'
    statement = 'To kill a bear, you have to run quickly'
#    statement = 'I like Joes cocaine party countdown'
#    statement = 'The watercooler is the best place to hang out'
    processed = process_data(statement)
    processed = tfidf_vector(processed, path='models/tfidf_vectorizer.pkl')

    prediction = predict_class(processed, path='models/model.pkl')

    if prediction == 0:
        print(statement)
        print('Your boss is a Dwight!')
    else:
        print(statement)
        print('Your boss is a Michael! ')


