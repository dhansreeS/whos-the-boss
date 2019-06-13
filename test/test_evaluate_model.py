import os
from os import path
import sys
rel_path = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(rel_path)
import src.evaluate_model as em
import src.train_model as tm
from scipy.sparse import csr_matrix
import numpy as np


def test_predict_test():

    # input
    row = np.array([0, 0, 1, 2, 2, 2])
    col = np.array([0, 2, 2, 0, 1, 2])
    data = np.array([1, 2, 3, 4, 5, 6])

    X = csr_matrix((data, (row, col)), shape=(3, 3))

    y = [1, 0, 1]

    tm.training_model(X, y, {'C': 0.8, 'MODEL_SAVE': 'models/test_model.pkl'})

    y_preds = em.predict_test(X, {'MODEL_PATH': 'models/test_model.pkl'})

    print(type(y_preds))
    print(y_preds)

    os.remove('models/test_model.pkl')
    # check type
    assert isinstance(y_preds, np.ndarray)

    assert np.all((y_preds == 1) | (y_preds == 0))
