from keras import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import optimizers
import keras.models

from phased_lstm_keras.PhasedLSTM import PhasedLSTM
import numpy as np


class Predictor:
    learning_rate = 0.001

    decay_lr = 0

    loss_fn = 'mean_squared_error'

    def __init__(self, activation, ft_range):
        self.model = None
        self.activation = activation
        self.ft_range = ft_range

    def predict(self, input):
        return self.model.predict(input)

    def classify(self, input):
        return self.model.predict(input)[0]

    def load_model(self, path):
        self.model = keras.models.load_model(path, custom_objects={"PhasedLSTM": PhasedLSTM})
        self.model._make_predict_function()

    def get_model(self, shape, num_forecasts, activation='tanh'):
        """
        Builds and returns a model based on LSTM using the sizes given as param.
        :param layers: array/tuple (4 elements) with values: [0]: unused, [1]: Time steps, [2]: number of features,
        [3]: Size of output space
        :param activation: activation function for the LSTM - default is 'tanh' (values must be in range (-1,1)). If
        modified, please take care of range of values.
        :return: keras LSTM model compiled
        """
        model = Sequential()
        # Shape = (Samples, Timesteps, Features)
        model.add(PhasedLSTM(units=128, input_shape=shape,
                             return_sequences=False, activation=activation))
        model.add(Dropout(0.2))

        model.add(Dense(units=num_forecasts, activation=self.activation))

        opt = optimizers.Adagrad(lr=self.learning_rate, decay=self.decay_lr)
        # opt = optimizers.rmsprop(lr=0.01)
        model.compile(optimizer=opt, loss=self.loss_fn, metrics=['mae'])
        model.summary()
        return model
