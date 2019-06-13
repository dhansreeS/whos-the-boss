import pandas as pd
import os
from os import path
import sys
rel_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(rel_path)
import src.train_model as tm
import scipy
from scipy.sparse import csr_matrix
import numpy as np

def test_extract_response():

    # input dataframe
    inputs = {
        'speaker': ['Michael', 'Dwight', 'Dwight', 'Michael', 'Michael', 'Michael',
                    'Dwight', 'Michael', 'Dwight']
    }

    input_df = pd.DataFrame(data=inputs)

    # Expected data frame
    expected = [1, 0, 0, 1, 1, 1, 0, 1, 0]

    expected_df = expected

    created_df = tm.extract_response(input_df)

    # Check expected output
    assert expected_df == created_df


def test_tfidf_vector():

    # input dataframe
    inputs = {
        'line_text': ['Does this work?', 'I have no idea', 'This would make sense',
                      'Coming up with test cases is weird', 'Should i be using existing text?',
                      'Whassup!', 'No, but I still have my medal from that.', 'Only two more',
                      "That is it! I'm done"]
    }

    input_df = pd.DataFrame(data=inputs)

    created_df = tm.tfidf_vector(input_df['line_text'], "models", "test_tfidf.pkl")

    os.remove('models/test_tfidf.pkl')

    # Check type
    assert scipy.sparse.issparse(created_df)


def test_split_data():

    # input
    row = np.array([0, 0, 1, 2, 2, 2])
    col = np.array([0, 2, 2, 0, 1, 2])
    data = np.array([1, 2, 3, 4, 5, 6])

    X = csr_matrix((data, (row, col)), shape=(3, 3))

    y = [1,0,1]

    created_df1, created_df2 = tm.split_data(X, y,
                                             {'train_size': 0.8, 'random_state': 12345,
                                              'TEST_PATH':'data/test', 'X_TEST_NAME': 'abc_test.npz',
                                              'Y_TEST_NAME': 'abc_y.npy'})

    print(created_df1)
    print(created_df2)

    os.remove('data/test/abc_test.npz')
    os.remove('data/test/abc_y.npy')

    # Check type
    assert scipy.sparse.issparse(created_df1)
    assert isinstance(created_df2, list)
