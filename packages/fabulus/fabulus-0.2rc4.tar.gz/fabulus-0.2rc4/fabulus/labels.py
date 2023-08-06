import numpy as np


def labels_to_11(y: np.ndarray) -> np.ndarray:
    """
    Converts labels from (0, 1) to (-1, 1)

    :param y: label vector
    :return: new labels
    """
    if y is None:
        raise ValueError('Labels must not be None!')

    return y * 2 - 1


def labels_to_01(y: np.ndarray) -> np.ndarray:
    """
    Converts labels from (-1, 1) to (0, 1)

    :param y: label vector
    :return: new labels
    """
    if y is None:
        raise ValueError('Labels must not be None!')

    return (y + 1) / 2


def to_int(y: np.ndarray) -> np.ndarray:
    """
    Converts labels to ``np.int`` or leaves as is, if they already are
    :param y: label vector
    :return: labels as ``np.int``
    """
    return y.astype(int) if y.dtype is not np.int else y
