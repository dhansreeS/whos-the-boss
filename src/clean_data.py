import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os
import boto3
import io
import logging.config
logger = logging.getLogger(__name__)


def load_data(path, s3=False, bucket=None):
    """Load csv into dataframe from specified path

        Args:
            path (string): Path from which data should be loaded.
            s3 (boolean): Load from S3 or not
            bucket (string): Name of bucket to be loaded from

        Returns:
            pandas dataframe of loaded data
    """

    if s3:

        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket, Key='raw/the_office_lines.csv')
        df = pd.read_csv(io.BytesIO(obj['Body'].read()))

    else:
        # read all lines from The Office
        df = pd.read_csv(path)

    logger.info('File read into df')

    return df


def extract_m_and_d(df):
    """Filter only Michael and Dwight's lines

        Args:
            df (dataframe): Dataframe with all office lines

        Returns:
            pandas dataframe of with only Michael and Dwight's lines
    """

    df = df.loc[(df['speaker'] == "Michael") | (df['speaker'] == "Dwight")]

    logger.info('Df reduced to only Mike and Dwight lines')

    return df


def preprocess(df):
    """Removing spaces and other punctuations in the text. Lowercase all text

        Args:
            df (dataframe): Dataframe with Mike and Dwight's lines
        Returns:
            pandas dataframe with preprocessed text
    """
    # clean spaces, punctuation, replace with lowercase
    replace_no_space = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")
    replace_with_space = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
    no_space = ''
    space = ' '

    df = [replace_no_space.sub(no_space, line.lower()) for line in df]
    df = [replace_with_space.sub(space, line) for line in df]

    return df


def remove_stop_words(df):
    """ Removing generic English stop words from text

        Args:
            df (dataframe): Dataframe with lines
        Returns:
            pandas dataframe with no stop words in text

    """

    english_stop_words = stopwords.words('english')
    english_stop_words.extend(('would', 'im', 'na'))
    removed_stop_words = []
    for d in df:
        removed_stop_words.append(
            ' '.join([word for word in d.split()
                      if word not in english_stop_words])
        )
    return removed_stop_words


def get_lemmatized_text(df):
    """ Lemmatize words in corpus to generalize or normalize words for training """

    lemmatizer = WordNetLemmatizer()
    return [' '.join([lemmatizer.lemmatize(word) for word in d.split()]) for d in df]


def process_data(args):
    """Loads processed data to the path.

        Args:
            args (argument from user): Including string with path to load processed data to

        Returns:
            None
    """

    # read all lines from The Office
    localConf = args.localConf
    s3_config = args.s3config

    all_lines = load_data(localConf['SOURCE_PATH'], args.s3, s3_config['DEST_S3_BUCKET'])

    lines = extract_m_and_d(all_lines)

    processed = preprocess(lines['line_text'])
    processed = remove_stop_words(processed)
    processed = get_lemmatized_text(processed)

    lines_new = lines.copy()
    lines_new['line_text'] = processed
    lines_new = lines_new.dropna()

    logger.info('Dataframe cleaned')

    if args.s3:
        csv_buffer = io.StringIO()
        lines_new.to_csv(csv_buffer)
        s3_resource = boto3.resource('s3')
        s3_resource.Object(s3_config['DEST_S3_BUCKET'], localConf['FILE_NAME_S3']).put(Body=csv_buffer.getvalue())

    else:
        os.makedirs(localConf['DEST_PATH'], exist_ok=True)

        lines_new.to_csv(localConf['DEST_PATH'] + '/' + localConf['FILE_NAME'], index=False)

    logger.info('Dataframe uploaded to desired path')

