from typing import Tuple

import numpy as np
from tensorflow.python.keras import models
from tensorflow.python.keras.engine.training import Model
from tensorflow.python.keras.layers import Dense, Dropout
from tensorflow.python.keras.metrics import accuracy, categorical_crossentropy as cross_entropy
from tensorflow.python.keras.optimizers import Optimizer

from fabulus.labels import labels_to_01 as to_01, labels_to_11 as to_11


def network(input_units: int, n_layer: int, activation: Tuple[str] = None, output: str = 'sigmoid',
            dropout: float = None) -> Model:
    """
    Generates simple dense network of ``layer`` hidden layers and one output

    :param input_units: number of input neurons
    :param n_layer: number of hidden layers (excluding output and dropout layer)
    :param activation: activation functions for dense layer; defaults to 'relu'
    :param output: activation of output layer
    :param dropout: rate of dropout layers between fully connected layers; no dropouts
    when ``dropout=None``
    :return: constructed model
    """
    if input_units <= 1:
        raise ValueError(f'Input layer has to have more than 2 neurons! {input_units}')
    if n_layer <= 1:
        raise ValueError(f'Number of hidden layers needs to be greater than 0! {n_layer}')
    if activation is not None and len(activation) != n_layer:
        raise ValueError(f'Length of activations differs from number of hidden layers! '
                         f'{len(activation)} != {n_layer}')
    if not (0 < dropout < 1):
        raise ValueError(f'Dropout-rate needs to be in (0, 1)! {dropout}')

    activation = activation or ['relu'] * n_layer

    model = models.Sequential()

    # hidden layer
    for n, a in zip(np.logspace(np.log10(input_units), 4 / 3, n_layer), activation):
        model.add(Dense(np.ceil(n), activation=a))

        # dropout units
        if dropout:
            model.add(Dropout(rate=dropout))

    # output layer
    model.add(Dense(1, activation=output))
    return model


def compile_model(model: Model, optimizer: Optimizer = None, loss_fun=cross_entropy,
                  metrics: Tuple = (accuracy,)) -> Model:
    """
    Compiles tensorflow model with optimizer, loss function and metrics

    :param model: tensorflow network
    :param optimizer: optimizer
    :param loss_fun: loss function
    :param metrics: metrics to be printed during train-stage
    :return: compiled model
    """
    if model is None:
        raise ValueError('Model must not be None!')
    if loss_fun is None:
        raise ValueError('Loss function must not be None!')
    if metrics is None or len(metrics) <= 0:
        raise ValueError('Metrics must not be None or empty')

    model.compile(optimizer=optimizer, loss=loss_fun, metrics=metrics)
    return model


def fit(model: Model, X: np.ndarray, y: np.ndarray, batch_size: int = 128, epochs: int = 10):
    """
    Fits model with data X and class labels y

    :param model: compiled models
    :param X: data
    :param y: class labels
    :param batch_size: batch size
    :param epochs: number of epochs
    """
    if model is None:
        raise ValueError('Model must not be null!')
    if X is None:
        raise ValueError('Data must not be null!')
    if y is None:
        raise ValueError('Labels must not be null!')
    if not (8 <= batch_size <= 1024):
        raise ValueError(f'Batch size was not in [8, 1024]! {batch_size}')
    if epochs <= 0:
        raise ValueError(f'Number of epochs must be positive! {epochs}')

    if set(y) != {-1, +1}:
        y = to_01(y)

    model.fit(X, y, batch_size=batch_size, epochs=epochs, verbose=2)


def _discretise_y(y: np.ndarray, threshold: float = 0.5) -> np.ndarray:
    """
    Discretises y to (0, 1)

    1 iff y >= threshold

    0 iff y < threshold

    :param y: continuous label vector
    :param threshold: voting threshold
    :return: 1d vector in (0, 1)
    """
    return (y >= threshold).astype(int)


def predict(model: Model, X: np.ndarray, label_mapper=to_11) -> np.ndarray:
    """
    Predicts labels of data X

    :param model: fitted model
    :param X: data
    :param label_mapper: mapper of predicted labels
    :return: 1d-vector of predicted class labels
    """
    if model is None:
        raise ValueError('Model must not be null!')
    if X is None:
        raise ValueError('Data must not be null!')
    if label_mapper is None:
        raise ValueError('Label mapping function must not be null!')

    y = model.predict(X).ravel()
    return label_mapper(_discretise_y(y))
