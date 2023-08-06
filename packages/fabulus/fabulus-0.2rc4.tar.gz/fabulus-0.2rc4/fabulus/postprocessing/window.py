from typing import Union

import numpy as np
from scipy.stats import norm

from fabulus._internal.utils import to_string


class Window:
    """
    Utility class for smoothing 1D labels. Values at the beginning and end of the labels,
    where window would reach out of bounds are left as is.

    Provides functionality for smoothing wrt.
        - mode
        - mean
        - median
        - squares
        - weights
        - gaussian weights
    """

    def __init__(self, k: int):
        """
        :param k: window size; has to be an odd number >= 3
        """
        if k % 2 == 0 or not k >= 3:
            raise ValueError(f'Window size must be odd and >= 3! {k}')
        self.k = k
        # using integer division, truncating span
        self._span = int(self.k / 2)

        self.labels_ = None
        # begin of smoothing window
        self._beg = self._span
        # end of smoothing window
        self._end = -1

        # return labels as integers
        self._to_int = None

    def fit(self, labels: np.ndarray) -> 'Window':
        """
        Fits label vector (deep copy)

        :param labels: label vector
        :return: self
        """
        if labels is None:
            raise ValueError('Labels must not be None!')
        if labels.ndim != 1:
            raise ValueError(f'Labels must be one dimensional! {labels.shape}')

        self.labels_ = labels.copy()
        self._end = len(self.labels_) - self._span

        self._to_int = self.labels_.dtype == np.int
        return self

    def _is_fit(self) -> None:
        """
        Check if Window has been fit
        """
        if self.labels_ is None:
            raise AttributeError(f'{self} has not been fit!')

    def _as_type(self, labels: np.ndarray) -> np.ndarray:
        """
        Returns labels as ``float`` or ``int``, depending on ``self._to_int``

        :param labels: label vector
        :return: converted labels
        """
        return labels.round().astype(int) if self._to_int else labels

    def median(self) -> np.ndarray:
        """
        Smooths label vector wrt. median

        :return: smoothed labels
        """
        self._is_fit()

        smooth = self.labels_.copy()
        for i in range(self._beg, self._end):
            smooth[i] = np.median(self.labels_[i - self._span:i + self._span + 1])

        return self._as_type(smooth)

    @staticmethod
    def _mode(labels: np.ndarray) -> Union[float, int]:
        """
        Calculates the mode of a given vector.

        If two values occur the same number of times, the smaller element wrt. natural order is
        chosen.

        :param labels: label vector
        :return: mode of ``labels``
        """
        uni, cnt = np.unique(labels, return_counts=True)
        return uni[np.argmax(cnt)]

    def mode(self) -> np.ndarray:
        """
        Smooths label vector wrt. mode

        :return: smoothed labels
        """
        self._is_fit()

        smooth = self.labels_.copy()
        for i in range(self._beg, self._end):
            smooth[i] = self._mode(self.labels_[i - self._span:i + self._span + 1])

        return self._as_type(smooth)

    def mean(self) -> np.ndarray:
        """
        Smooths label vector wrt. mean

        :return: smoothed labels
        """
        self._is_fit()

        smooth = self.labels_.copy()
        for i in range(self._beg, self._end):
            smooth[i] = np.mean(self.labels_[i - self._span:i + self._span + 1])

        return self._as_type(smooth)

    def squares(self) -> np.ndarray:
        """
        Smooths label vector wrt. squares

        labels_new[i] = labels[i] + sum(sqrt(1 / index_difference²) * value_difference)

        :return: smoothed labels
        """
        self._is_fit()

        smooth = self.labels_.copy()
        for i, pivot in enumerate(self.labels_[self._beg:self._end], self._span):
            offset = 0
            for j in range(i - self._span, i + self._span + 1):
                if i != j:
                    offset += (self.labels_[j] - pivot) * np.sqrt((i - j) ** -2)
            smooth[i] = np.round(pivot + offset / self.k)

        return self._as_type(smooth)

    def weighted(self, weights: np.ndarray) -> np.ndarray:
        """
        Smooths label vector wrt. weights

        :param weights: Vector specifying weights for window
        :return: smoothed labels
        """
        self._is_fit()

        if not weights:
            raise ValueError('Weights must not be null')
        if len(weights) != self.k:
            raise ValueError(
                f'Weights must be of same length as window-size! {len(weights)} != {self.k}')

        return self._weighted(weights)

    def _weighted(self, weights: np.ndarray) -> np.ndarray:
        smooth = self.labels_.copy()
        for i in range(self._beg, self._end):
            smooth[i] = np.average(self.labels_[i - self._span:i + self._span + 1], weights=weights)

        return self._as_type(smooth)

    def gaussian(self, width: float) -> np.ndarray:
        """
        Weights label vector with respect to guassian unit pdf.
        Weights are linspace(-width, width, k).

        :param width: One-sided interval size for pdf
        :return: smoothed labels
        """
        self._is_fit()

        if width <= 0:
            raise ValueError(f'Width must be greater than 0! {width}')

        weights = norm.pdf(np.linspace(-width, width, num=self.k))
        return self._weighted(weights)

    def __str__(self) -> str:
        return to_string(self, internal=True)

    __repr__ = __str__
