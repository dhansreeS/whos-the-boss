import pandas as pd
from os import path
import sys
rel_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(rel_path)
import src.train_model as tm

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