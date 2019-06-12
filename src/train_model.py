from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import scipy.sparse

import pandas as pd
import numpy as np
import os
import boto3
import io
import pickle
import logging.config

logger = logging.getLogger(__name__)



# read the file from the processed folder

def load_data(path, s3=False, bucket=None, key=None):
    """Load csv into dataframe from specified path

        Args:
            path (string): Path from which data should be loaded.
            s3 (boolean): Load from S3 or not
            bucket (string): Name of bucket to be loaded from
            key (string): File name for s3

        Returns:
            pandas dataframe of processed data
    """

    if s3:

        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(io.BytesIO(obj['Body'].read()))

    else:
        # read all lines from The Office
        df = pd.read_csv(path)

    logger.info('File read into df')

    return df


def tfidf_vector(lines_text, path, filename, s3=False, bucket=None, key=None):
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

        with open(path + '/' + filename, 'wb') as fin:
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


def split_data(X, y, configs, s3=False, bucket=None):
    """Split data into train and test

        Args:
            X (matrix): Features
            y (list): Response values
            configs (dict): All configurations related to split
            s3 (boolean): Save to S3 or not
            bucket (string): Name of the bucket

        Returns:
            train features and responses

    """

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=configs['train_size'], test_size = 1-configs['train_size'], random_state=configs['random_state']
    )

    os.makedirs(configs['TEST_PATH'], exist_ok=True)
    scipy.sparse.save_npz(configs['TEST_PATH'] + '/' + configs['X_TEST_NAME'], X_test, compressed=True)
    np.save(configs['TEST_PATH'] + '/' + configs['Y_TEST_NAME'], y_test)

    if s3:
        s3 = boto3.resource('s3')
        key = configs['S3_X_TEST_NAME']
        s3.Bucket(bucket).upload_file(configs['TEST_PATH'] + '/' + configs['X_TEST_NAME'], key)
        key = configs['S3_Y_TEST_NAME']
        s3.Bucket(bucket).upload_file(configs['TEST_PATH'] + '/' + configs['Y_TEST_NAME'], key)

    logger.info('Data split into train and test. Test saved')

    return X_train, y_train


def training_model(X, y, configs, s3=False, bucket=None):
    """Saves a pickle file with trained logistic regression model

        Args:
            X (matrix): Features for training
            y (list): Actual values
            configs (dict): Configurations related to the model
            s3 (boolean): Save to S3 or not
            bucket (string): Name of bucket to be saved to

    """

    lr = LogisticRegression(C=configs['C'], solver="liblinear")
    lr.fit(X, y)

    logger.info("Accuracy for logistic regression with C=%s: %s", configs['C'], accuracy_score(y, lr.predict(X)))

    if s3:
        key = configs['S3_MODEL_SAVE']
        pickle_byte_obj = pickle.dumps(lr)
        s3_resource = boto3.resource('s3')
        s3_resource.Object(bucket, key).put(Body=pickle_byte_obj)

    else:
        with open(configs['MODEL_SAVE'], 'wb') as fin:
            pickle.dump(lr, fin)

    logger.info('Model trained and saved')


def train(args):
    """Runs all the training steps including tfidf vectorizer
        Args:
            args: All arguments from run.py

        Returns:
            NA
    """

    trainConf = args.localConf
    s3_config = args.s3config

    path = trainConf['SOURCE_PATH']
    lines = load_data(path, args.s3, s3_config['DEST_S3_BUCKET'], trainConf['S3_SOURCE'])

    lines = lines.dropna()

    X = tfidf_vector(lines['line_text'], path=trainConf['TFIDF_PATH'], filename=trainConf['TFIDF_NAME'],
                     s3=args.s3, bucket=s3_config['DEST_S3_BUCKET'], key=trainConf['S3_TFIDF'])

    response = extract_response(lines)

    X_train, y_train = split_data(X, response, trainConf['split'], args.s3, s3_config['DEST_S3_BUCKET'])

    training_model(X_train, y_train, trainConf['model'], args.s3, s3_config['DEST_S3_BUCKET'])
