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
logging.config.fileConfig('../config/logging/local.conf')
logger = logging.getLogger(__name__)



# read the file from the processed folder

def load_data(path, s3=False, bucket=None):
    """Load csv into dataframe from specified path

        Args:
            path (string): Path from which data should be loaded.
            s3 (boolean): Load from S3 or not
            bucket (string): Name of bucket to be loaded from

        Returns:
            pandas dataframe of processed data
    """

    if s3:

        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket, Key='processed/processed_lines.csv')
        df = pd.read_csv(io.BytesIO(obj['Body'].read()))

    else:
        # read all lines from The Office
        df = pd.read_csv(path)

    logger.info('File read into df')

    return df


def tfidf_vector(lines_text, path, s3=False, bucket=None):
    """Vectorize the lines using tfidf_vectorizer, also save for further use

        Args:
            lines_text (list): All the processed lines
            path (string): Path to which the vectorizer should be saved
            s3 (boolean): Save to S3 or not
            bucket (string): Name of bucket to be saved to

        Returns:
            matrix with vectorized lines

    """
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectorizer.fit(lines_text)
    X1 = tfidf_vectorizer.transform(lines_text)

    if s3:
        key = 'pickles/tfidf.pkl'
        pickle_byte_obj = pickle.dumps(tfidf_vectorizer)
        s3_resource = boto3.resource('s3')
        s3_resource.Object(bucket, key).put(Body=pickle_byte_obj)

    else:
        try:
            # Create target Directory
            os.mkdir(path)
            print("Directory ", path, " Created ")
        except FileExistsError:
            print("Directory ", path, " already exists")

        with open(path + '/tfidf_vectorizer.pkl', 'wb') as fin:
            pickle.dump(tfidf_vectorizer, fin)

    logger.info('Tfidf features created for training')

    return X1


def extract_response(df):
    """Return a list with all Michael's coded as 1 and Dwight coded as 0

        Args:
            df (dataframe): All processed lines dataframe with speaker info

        Returns:
            list of one hot encoded responses

    """

    response = list(pd.get_dummies(df['speaker'])['Michael'])

    logger.info('Response column created for training')

    return response


def training_model(X, y, C, path, s3=False, bucket=None):
    """Saves a pickle file with trained logistic regression model

        Args:
            X (matrix): Features for training
            y (list): Actual values
            C (float): Regularization parameter for logistic regression

    """

    lr = LogisticRegression(C=C, solver="liblinear")
    lr.fit(X, y)

    logger.info("Accuracy for logistic regression with C=%s: %s", C, accuracy_score(y, lr.predict(X)))

    if s3:
        key = 'models/model.pkl'
        pickle_byte_obj = pickle.dumps(lr)
        s3_resource = boto3.resource('s3')
        s3_resource.Object(bucket, key).put(Body=pickle_byte_obj)

    else:
        with open(path + '/model.pkl', 'wb') as fin:
            pickle.dump(lr, fin)


if __name__ == '__main__':

    # read all lines from The Office
    path = '../data/processed/processed_lines.csv'
    lines = load_data(path)

    lines = lines.dropna()

    X1 = tfidf_vector(lines['line_text'], path='../data/pickles')
    response = extract_response(lines)
    training_model(X1, response, C=0.8, path='../models')


