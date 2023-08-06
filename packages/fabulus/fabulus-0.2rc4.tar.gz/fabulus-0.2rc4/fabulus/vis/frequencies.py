from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def show_class_frequencies(y: np.array, save: str = None, **kwargs) -> Tuple[np.ndarray, np.ndarray]:
    """
    Creates a bar chart showing the relative class frequencies given the label-vector.

    :param y: class labels
    :param save: Path to save the plot iff not 'None'
    :param kwargs: Arguments to modify the style of the plot. Supports: 'xlabel', 'ylabel', 'title', 'palette'
    :return: tuple containing an array of unique class labels and an array of their according frequencies
    """
    unique_values, n_occurrences = np.unique(y, return_counts=True)
    frequencies = n_occurrences / n_occurrences.sum()

    plt.style.use('ggplot')
    plt.title(kwargs.get('title', 'Baseline'))
    plt.ylabel(kwargs.get('ylabel', 'Frequency'))
    plt.xlabel(kwargs.get('xlabel', 'Label'))

    ax = sns.barplot(unique_values, frequencies, tick_label=unique_values,
                     palette=sns.color_palette(kwargs.get('palette', 'Blues_d')))

    for rect in ax.patches:
        y_val = rect.get_height()
        x_val = rect.get_x() + rect.get_width() / 2

        plt.annotate('{:.2f}'.format(y_val),
                     xy=(x_val, y_val),
                     xytext=(0, 5),
                     textcoords='offset points',
                     ha='center')

    if save:
        plt.savefig(save)
    else:
        plt.show()

    return unique_values, frequencies
