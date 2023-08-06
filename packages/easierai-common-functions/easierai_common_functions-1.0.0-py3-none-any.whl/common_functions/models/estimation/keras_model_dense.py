from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras import optimizers
import tensorflow.keras.models


class Predictor:
    learning_rate = 0.01

    decay_lr = 0

    loss_fn = 'mse'

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

    def get_model(self, shape, num_forecasts, activation='relu'):
        model = Sequential()
        # Input arrays of shape (*, layers[1])
        # Output = arrays of shape (*, layers[1] * 16)
        # model.add(Dense(units=int(120), input_shape=(layers[1],), activation=activation))
        # model.add(Dropout(0.2))
        model.add(Dense(units=int(64), input_shape=shape, activation=activation))
        model.add(Dense(units=int(64), activation=activation))
        # model.add(Dropout(0.2))
        model.add(Flatten())
        model.add(Dense(units=num_forecasts, activation=self.activation))
        # activation=activation))

        # opt = optimizers.Adagrad(lr=self.learning_rate, epsilon=None, decay=self.decay_lr)
        opt = optimizers.RMSprop(lr=0.001)
        model.compile(optimizer=opt, loss=self.loss_fn, metrics=['mae'])
        model.summary()
        self.model = model
        return model
