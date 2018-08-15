from __future__ import print_function

from keras.models import Model
from keras.layers import Input, Dense, Conv2D, Flatten, BatchNormalization, Activation, LeakyReLU, Add
from keras.optimizers import SGD, Adam
from keras import regularizers
import keras.backend as K
import tensorflow as tf

import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # Only error will be shown

def softmax_cross_entropy_with_logits(y_true, y_pred):
    '''
    Softmax Cross Entropy Function with logits
    '''
    loss = tf.nn.softmax_cross_entropy_with_logits_v2(labels=y_true, logits=y_pred)
    return loss

class NeuralNetwork:
    '''
    Deep learning neural network
    '''
    def __init__(self, 
        input_shape,
        output_dim,
        network_structure,
        learning_rate=1e-3,
        l2_const=1e-4,
        verbose
        ):

        self.input_shape = input_shape
        self.output_shape = output_dim
        self.network_structure = network_structure

        self.learning_rate = learning_rate
        self.momentum = momentum
        self.l2_const = l2_const

        self.verbose = verbose

        self.model = self.build_model()

    def build_model(self):
        state_tensor = Input(shape=self.input_shape)

        x = self.__conv_block(state_tensor, self.network_structure[0]['filters'], self.network_structure[0]['kernel_size'])
        if len(self.network_structure) > 1:
            for h in self.network_structure[1:]:
                x = self.__res_block(x, h['filters'], h['kernel_size'])
        
        action = self.__action_block(x)
        value = self.__value_block(x)
        
        model = Model(inputs=state_tensor, outputs=[action, value])
        model.compile(loss={'value': 'mse', 'action': softmax_cross_entropy_with_logits},
			optimizer=Adam(self.learning_rate),	
			loss_weights={'value': 0.5, 'action': 0.5}	
			)

        return model

    def __conv_block(self, x, filters, kernel_size=3):
        '''
        Convolutional Neural Network
        '''
        out = Conv2D(
            filters = filters,
            kernel_size = kernel_size,
            padding = 'same',
            activation='linear',
            kernel_regularizer = regularizers.l2(self.l2_const)
        )(x)
        out = BatchNormalization(axis=1)(out)
        out = LeakyReLU()(out)
        return out

    def __res_block(self, x, filters, kernel_size=3):
        '''
        Residual Convolutional Neural Network
        '''
        out = Conv2D(
            filters = filters,
            kernel_size = kernel_size,
            padding = 'same',
            activation='linear',
            kernel_regularizer = regularizers.l2(self.l2_const)
        )(x)
        out = BatchNormalization(axis=1)(out)
        out = Add()([out, x])
        out = LeakyReLU()(out)
        return out

    def __value_block(self, x):
        out = Conv2D(
            filters = 32,
            kernel_size = (3,3),
            padding = 'same',
            activation='linear',
            kernel_regularizer = regularizers.l2(self.l2_const)
        )(x)
        out = BatchNormalization(axis=1)(out)
        out = LeakyReLU()(out)

        out = Flatten()(out)
        out = Dense(
            36,
            use_bias=False,
            activation='linear',
            kernel_regularizer= regularizers.l2(self.l2_const)
		)(out)
        out = LeakyReLU()(out)

        value = Dense(
			1, 
            use_bias=False,
            activation='tanh',
            kernel_regularizer=regularizers.l2(self.l2_const),
            name = 'value'
			)(out)

        return value

    def __action_block(self, x):
        out = Conv2D(
            filters = 32,
            kernel_size = (3,3),
            padding = 'same',
            activation='linear',
            kernel_regularizer = regularizers.l2(self.l2_const)
        )(x)
        out = BatchNormalization(axis=1)(out)
        out = LeakyReLU()(out)

        out = Flatten()(out)
        out = Dense(
            36,
            use_bias=False,
            activation='linear',
            kernel_regularizer= regularizers.l2(self.l2_const)
		)(out)
        out = LeakyReLU()(out)

        action = Dense(
			self.output_shape, 
            use_bias=False,
            activation='tanh',
            kernel_regularizer=regularizers.l2(self.l2_const),
            name = 'action'
			)(out)

        return action

    def fit(self, Xs, ys, epochs, batch_size):
        history = self.model.fit(Xs, ys, epochs=epochs, batch_size=batch_size, verbose=self.verbose)
        return history

    def update(self, Xs, ys):
        loss = self.model.train_on_batch(Xs, ys)
        return loss

    def predict(self, X):
        #X = X.reshape(self.input_shape)
        action_prob, value = self.model.predict([X])
        return action_prob[0], value[0]

    def save_model(self, filename):
        self.model.save_weights(filename)

    def load_model(self, filename):
        self.model.load_weights(filename)

    def plot_model(self, filename):
        from keras.utils import plot_model
        plot_model(self.model, show_shapes=True, to_file=filename)
        
class AI:
    '''
    Artificial Intelligence Player
    '''
    def __init__(self,
        state_shape,
        action_dim,
        verbose=False):

        self.state_shape = state_shape
        self.action_dim = action_dim
        self.verbose = verbose

        network_structure = list()
        network_structure.append({'filters':64, 'kernel_size':3})
        network_structure.append({'filters':64, 'kernel_size':3})
        network_structure.append({'filters':64, 'kernel_size':3})
        network_structure.append({'filters':64, 'kernel_size':3})

        self.nnet = NeuralNetwork(
            input_shape=self.state_shape,
            output_dim=action_dim,
            network_structure=network_structure)

    def load_nnet(self, filename):
        self.nnet.load_model(filename)

    def save_nnet(self, filename):
        self.nnet.save_model(filename)

    def plot_nnet(self, filename):
        self.nnet.plot_model(filename)

    def update(self, data, epochs, batch_size):
        '''
        Update neural network
        '''
        Xs, ys = data
        return self.nnet.update(Xs, ys)

    def train(self, data, epochs=30, batch_size=128):
        '''
        Train neural network
        '''
        Xs, ys = data
        return self.nnet.fit(
            Xs, ys, 
            epochs=epochs, 
            batch_size=batch_size)

    def evaluate_function(self, state):
        '''
        Evaluate status based on current state information
        '''
        action_prob, value = self.nnet.predict(state)
        return action_prob, value

    def play(self, state):
        action_prob, value = self.nnet.predict(state)
        action = np.argmax(action_prob)
        return action