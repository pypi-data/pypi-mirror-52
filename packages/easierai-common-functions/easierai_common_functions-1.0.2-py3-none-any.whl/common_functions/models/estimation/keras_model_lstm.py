from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Convolution1D, BatchNormalization, LSTM, Activation, GlobalAveragePooling1D, Input, \
    concatenate, Dropout
from tensorflow.keras import optimizers
from tensorflow.keras.models import Model
import tensorflow.keras.models
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
        self.model = tensorflow.keras.models.load_model(path)
        self.model._make_predict_function()

    def get_model(self, shape, num_forecasts, activation='tanh'):
        """
        Builds and returns a model based on LSTM using the sizes given as param.
        :param activation: activation function for the LSTM - default is 'tanh' (values must be in range (-1,1)). If
        modified, please take care of range of values.
        :return: keras LSTM model compiled
        """
        model = Sequential()
        # Shape = (Samples, Timesteps, Features)
        model.add(LSTM(units=128, input_shape=shape,
                       return_sequences=False, activation=activation))
        model.add(Dropout(0.2))

        model.add(Dense(units=num_forecasts, activation=self.activation))

        opt = optimizers.Adagrad(lr=self.learning_rate, decay=self.decay_lr)
        # opt = optimizers.rmsprop(lr=0.01)
        model.compile(optimizer=opt, loss=self.loss_fn, metrics=['mae'])
        model.summary()
        return model

    def get_model_strong(self, layers, activation='tanh'):
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
        model.add(LSTM(units=128, input_shape=(layers[1], layers[2]),
                       return_sequences=True, activation=activation))
        # model.add(Dropout(0.2))

        # model.add(LSTM(64, return_sequences=True, activation=activation))
        model.add(LSTM(256, return_sequences=True, activation=activation))
        model.add(LSTM(128, return_sequences=True, activation=activation))
        # model.add(LSTM(64, return_sequences=True, activation=activation))
        # model.add(Dropout(0.2))

        model.add(LSTM(layers[2], return_sequences=False, activation=activation))
        model.add(Dense(units=layers[3], activation=self.activation))

        opt = optimizers.Adagrad(lr=self.learning_rate, decay=self.decay_lr)
        # opt = optimizers.rmsprop(lr=0.01)
        model.compile(optimizer=opt, loss=self.loss_fn, metrics=['mse'])
        model.summary()
        return model

    def get_model_lstm_fcn(self, shape):
        main_input = Input(shape=shape, dtype='float32', name='main_input')
        # --------------------------

        lstm_out = LSTM(256, dtype=float, dropout=0.8)(main_input)
        lstm_out = Activation('relu')(lstm_out)
        # --------------------------

        conv = Convolution1D(128, 8, kernel_initializer='he_uniform')(main_input)
        conv = BatchNormalization(momentum=0.99, epsilon=0.001)(conv)
        conv = Activation('relu')(conv)

        conv = (Convolution1D(256, 5, kernel_initializer='he_uniform'))(conv)
        conv = BatchNormalization(momentum=0.99, epsilon=0.001)(conv)
        conv = Activation('relu')(conv)

        conv = (Convolution1D(128, 10, kernel_initializer='he_uniform'))(conv)
        conv = BatchNormalization(momentum=0.99, epsilon=0.001)(conv)
        conv = Activation('relu')(conv)

        conv = (GlobalAveragePooling1D())(conv)
        # --------------------------

        concatenation = concatenate([lstm_out, conv])
        out = Dense(self.num_classes, name='dense_output2')(concatenation)

        model = Model(inputs=main_input, outputs=out)
        model.summary()
        opt = optimizers.Adagrad(lr=self.learning_rate, epsilon=None, decay=self.decay_lr)
        model.compile(optimizer=opt, loss=self.loss_fn, metrics=['accuracy'])

        return model
