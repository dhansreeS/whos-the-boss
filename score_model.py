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
logging.config.fileConfig('../config/logging/local.conf')
logger = logging.getLogger(__name__)


def process_data(new_line):
    """Process the new line entered
        Args:
            new_line (string): String to be processed before being scored

        Returns:
            new_line processed (string)
    """

    new_df = pd.DataFrame(new_line, columns=['line_text'])

    processed = preprocess(new_df['line_text'])
    processed = remove_stop_words(processed)
    processed = get_lemmatized_text(processed)

    print(processed)


if __name__ == '__main__':

    process_data('Please help! Does this work?')