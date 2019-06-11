import pandas as pd
from os import path
import sys
rel_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(rel_path)
import src.clean_data as cd


def test_extract_m_and_d():

    # input dataframe
    inputs = {
        'speaker': ['Michael', 'Dwight', 'Jim', 'Pam', 'Angela', 'Michael',
                      'Dwight', 'Jim', 'Dwight'],
        'line_text': ['Does this work?', 'I have no idea', 'This would make sense',
                      'Coming up with test cases is weird', 'Should i be using existing text?',
                      'Whassup!', 'No, but I still have my medal from that.', 'Only two more',
                      "That is it! I'm done"]
    }

    input_df = pd.DataFrame(data=inputs)

    # Expected data frame
    expected = {
        'speaker': ['Michael', 'Dwight', 'Michael',
                    'Dwight', 'Dwight'],
        'line_text': ['Does this work?', 'I have no idea',
                      'Whassup!', 'No, but I still have my medal from that.',
                      "That is it! I'm done"]
    }

    expected_df = pd.DataFrame(data=expected)

    created_df = cd.extract_m_and_d(input_df).reset_index(drop=True)

    # Check type
    assert isinstance(created_df, pd.DataFrame)

    # Check expected output
    assert expected_df.equals(created_df)


def test_preprocess():

    # input dataframe
    inputs = {
        'line_text': ['Does this work?', 'I have no idea',
                      'Whassup!', 'No, but I still have my medal from that.',
                      "That is it! I'm done"]
    }

    input_df = pd.DataFrame(data=inputs)

    # Expected data frame
    expected = ['does this work', 'i have no idea', 'whassup',
                'no but i still have my medal from that', 'that is it im done']

    created_df = cd.preprocess(input_df['line_text'])

    # Check expected output
    assert all([a == b for a, b in zip(created_df, expected)])


def test_remove_stop_words():

    # input dataframe
    inputs = {
        'line_text': ['does this work', 'i have no idea', 'whassup',
                      'no but i still have my medal from that', 'that is it im done']
    }

    input_df = pd.DataFrame(data=inputs)

    # Expected data frame
    expected = ['work', 'idea', 'whassup',
                'still medal', 'done']

    created_df = cd.remove_stop_words(input_df['line_text'])
    print(created_df)

    # Check expected output
    assert all([a == b for a, b in zip(created_df, expected)])
