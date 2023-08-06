from typing import Tuple

import numpy as np
from sklearn.base import BaseEstimator


def fit_predict(clf: BaseEstimator, X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray) \
        -> Tuple[BaseEstimator, np.ndarray]:
    """
    Wrapper for clf.fit(X_train, y_train) and clf.predict(X_test)

    :param clf: sklearn classifier
    :param X_train: train data
    :param y_train: train labels
    :param X_test: test data
    :return: fitted classifier, predicted test labels
    """
    if clf is None:
        raise ValueError('Classifier must not be None!')
    if X_train is None:
        raise ValueError('Train data must not be None!')
    if y_train is None:
        raise ValueError('Train labels must not be None!')
    if X_test is None:
        raise ValueError('Test data must not be None!')

    if X_train.ndim != 2:
        raise ValueError(f'Train data must have ndim = 2! {X_train.ndim}')
    if X_test.ndim != 2:
        raise ValueError(f'Train data must have ndim = 2! {X_test.ndim}')

    if len(X_train) != len(y_train):
        raise ValueError(f'Train data and samples must have same length! '
                         f'{len(X_train)} != {len(y_train)}')
    if X_train.shape[1] != X_test.shape[1]:
        raise ValueError(f'Train and Test data must have same dimensionality! '
                         f'{X_train.shape[1]} != {X_test.shape[1]}')

    clf.fit(X_train, y_train)
    return clf, clf.predict(X_test)
