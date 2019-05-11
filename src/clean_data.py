import pandas as pd
import re
from nltk.corpus import stopwords
import os


def load_data(path):
    """
    Load csv into datafram from specified path

    :param path (string): path to file
    :return: pandas dataframe
    """
    # read all lines from The Office
    df = pd.read_csv(path)

    return df


def extract_m_and_d(df):
    """
    Filter only Michael and Dwight's lines

    :param df (dataframe): all Office lines
    :return: df with only Dwight and Mike's lines
    """

    df = df.loc[(df['speaker'] == "Michael") | (df['speaker'] == "Dwight")]

    return df


def preprocess(df):
    """
    Removing spaces and other punctuations in the text. Lowercase all text

    :param df (dataframe): line text
    :return: cleaned list
    """
    # clean spaces, punctuation, replace with lowercase
    replace_no_space = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")
    replace_with_space = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
    no_space = ""
    space = " "

    df = [replace_no_space.sub(no_space, line.lower()) for line in df]
    df = [replace_with_space.sub(space, line) for line in df]

    return df


def remove_stop_words(df):
    """ Removing generic English stop words from text

    :param df (dataframe): line text
    :return: cleaned list
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


def process_data(path):
    """
    Loads processed data to the path

    :param path (string): path to file
    :return: NA
    """
    # read all lines from The Office
    all_lines = load_data(path + "raw/the_office_lines.csv")

    lines = extract_m_and_d(all_lines)

    processed = preprocess(lines['line_text'])
    processed = remove_stop_words(processed)

    lines_new = lines.copy()
    lines_new['line_text'] = processed

    #    processed = get_lemmatized_text(processed)

    os.makedirs(path + 'processed', exist_ok=True)

    lines_new.to_csv(path + "processed/processed_lines.csv", index=False)


if __name__ == '__main__':

    path = "data/"
    process_data(path)
