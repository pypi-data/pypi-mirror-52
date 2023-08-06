from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt

from fabulus.labels import to_int


def confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, plot: bool = True, save: str = None,
                     transparent: bool = True, cmap: str = None) -> np.ndarray:
    """
    Confusion matrix of ``y_true`` and ``y_pred``

    :param y_true: true labels
    :param y_pred: predicted labels
    :param plot: plot the image
    :param save: path to save image; do not save iff ``None``
    :param transparent: transparency of plot
    :param cmap: colormap; defaults to viridis
    :return: confusion matrix
    """
    if y_true is None:
        raise ValueError('True labels must not be None!')
    if y_pred is None:
        raise ValueError('Predicted labels must not be None!')

    y_true = to_int(y_true)
    y_pred = to_int(y_pred)
    t_min, t_end, p_min, p_end, mat = _create_matrix(y_true, y_pred)

    _, ax = plt.subplots(figsize=(12, 12))
    plt.title('Confusion matrix')
    plt.colorbar(ax.matshow(mat, cmap=plt.get_cmap(cmap or 'viridis')))
    ax.set_xlabel('Predicted class')
    ax.set_ylabel('True class')
    ax.set_xticks(range(p_end - p_min))
    ax.set_xticklabels(range(p_min, p_end))
    ax.set_yticks(range(t_end - t_min))
    ax.set_yticklabels(range(t_min, t_end))

    for i in range(t_end - t_min):
        for j in range(p_end - p_min):
            ax.text(j, i, mat[i, j], ha='center', va='center', color='white')

    if save:
        plt.savefig(save, transparent=transparent)

    if plot:
        plt.show()
    else:
        plt.close()

    return mat


def _create_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> Tuple[int, int, int, int, np.ndarray]:
    """
    Creates confusion matrix of ``y_true`` and ``y_pred``

    :param y_true: true labels
    :param y_pred: predicted labels
    :return: min(y_true), max(y_true) + 1, min(y_pred), max(y_pred) + 1, confusion matrix
    """
    t_min, t_max = y_true.min(), y_true.max()
    p_min, p_max = y_pred.min(), y_pred.max()

    mat = np.zeros((t_max - t_min + 1, p_max - p_min + 1))

    for t, p in zip(y_true, y_pred):
        mat[t - t_min, p - p_min] += 1

    return t_min, t_max + 1, p_min, p_max + 1, mat
