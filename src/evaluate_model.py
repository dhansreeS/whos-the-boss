import numpy as np
import pandas as pd
import boto3
import logging.config
import io
import pickle
import os
from sklearn.metrics import roc_auc_score, confusion_matrix, accuracy_score
import scipy.sparse
from sklearn.linear_model import LogisticRegression

logger = logging.getLogger(__name__)


def load_data(configs, s3=False, bucket=None):
    """Load feature and response numpy arrays from specified path

        Args:
            configs (dict): Configurations for loading
            s3 (boolean): Load from S3 or not
            bucket (string): Name of bucket to be loaded from

        Returns:
            X_test and y_test for model scoring
    """

    if s3:
        s3 = boto3.client('s3')
        os.makedirs(configs['DATA_PATH'], exist_ok=True)
        s3.download_file(bucket, configs['S3_X_TEST_NAME'], configs['DATA_PATH'] + configs['X_TEST_NAME'])
        s3.download_file(bucket, configs['S3_Y_TEST_NAME'], configs['DATA_PATH'] + configs['Y_TEST_NAME'])

    X_test = scipy.sparse.load_npz(configs['DATA_PATH'] + '/' + configs['X_TEST_NAME'])
    y_test = np.load(configs['DATA_PATH'] + '/' + configs['Y_TEST_NAME'])

    logger.info('Files read into X_test and y_test')

    return X_test, y_test


def predict_test(X_test, configs, s3=False, bucket=None):
    """Predict test values based on previously trained model

        Args:
            X_test (matrix): Features of testing set
            configs (dict): Configurations for model path
            s3 (boolean): Load from S3 or not
            bucket (string): Name of bucket to be loaded from

        Returns:
            y_pred for model scoring

    """

    if s3:
        s3 = boto3.resource('s3')
        with io.BytesIO() as data:
            s3.Bucket(bucket).download_fileobj(configs['S3_MODEL_PATH'], data)
            data.seek(0)  # move back to the beginning after writing
            model = pickle.load(data)

    else:
        model = pickle.load(open(configs['MODEL_PATH'], 'rb'))

    y_pred = model.predict(X_test)

    logger.info('Predicted for test data')

    return y_pred


def calculate_metrics(y_pred, y_test, configs, s3=False, bucket=None):
    """Calculate accuracy metrics for the model using test predictions
        Args:
            y_pred (list): Predictions for test set
            y_test (list): Actuals for test set
            configs (dict): Configurations for metric calculation
            s3 (boolean): Save to S3 or not
            bucket (string): Name of bucket

        Returns:
           NA
    """

    auc = roc_auc_score(y_pred, y_test)
    confusion = pd.DataFrame(confusion_matrix(y_pred, y_test), index=['Actual Dwight','Actual Michael'],
                  columns=['Predicted Dwight', 'Predicted Michael'])
    accuracy = accuracy_score(y_pred, y_test)

    with open(configs['METRIC_PATH']+configs['METRIC_NAME'], 'w') as the_file:
        the_file.write('AUC on test: %0.3f' % auc + '\n')
        the_file.write('Accuracy on test: %0.3f' % accuracy + '\n')

    confusion.to_csv(configs['METRIC_PATH']+configs['CONFUSION_NAME'])

    if s3:
        s3 = boto3.resource('s3')
        key = configs['S3_METRIC_NAME']
        s3.Bucket(bucket).upload_file(configs['METRIC_PATH']+configs['METRIC_NAME'], key)
        key = configs['S3_CONFUSION_NAME']
        s3.Bucket(bucket).upload_file(configs['METRIC_PATH']+configs['CONFUSION_NAME'], key)

    logger.info('Saved metrics in desired folder')


def evaluate(args):
    """Evaluate the model generated in train
        Args:
            args: Arguments from command line
        Returns:
            NA
    """
    localConf = args.localConf
    s3_config = args.s3config

    X_test, y_test = load_data(localConf['load'], args.s3, s3_config['DEST_S3_BUCKET'])

    y_pred = predict_test(X_test, localConf['predict'], args.s3, s3_config['DEST_S3_BUCKET'])

    calculate_metrics(y_pred, y_test, localConf['metrics'], args.s3, s3_config['DEST_S3_BUCKET'])



