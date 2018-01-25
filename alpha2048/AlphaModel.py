import numpy as np 

from keras.models import Sequential,load_model
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras import optimizers

class Model:
    def __init__(self,size):
        self.size = size
        self.model = None
    
    def init(self,blocksize=9):
        self.model = Sequential()
        
        self.model.add(Conv2D(
            filters=128,
            kernel_size=3,
            input_shape=(self.size[0],self.size[1],1)))
        self.model.add(BatchNormalization())
        self.model.add(Activation('relu'))

        #for i in range(blocksize-1):
        #    self.model.add(Conv2D(filters=64,kernel_size=3))
        #    self.model.add(BatchNormalization())
        #    self.model.add(Activation('relu'))
        
        self.model.add(Conv2D(filters=64,kernel_size=2))
        self.model.add(BatchNormalization())
        self.model.add(Activation('relu'))

        self.model.add(Flatten())
        self.model.add(Dense(64))
        self.model.add(Activation('relu'))
        self.model.add(Dense(32))
        self.model.add(Activation('relu'))
        self.model.add(Dense(4))
        self.model.add(Activation('relu'))

        adam = optimizers.Adam(lr=1e-6)
        self.model.compile(loss='mse',optimizer=adam)

    def learn(self,x,y):
        loss = self.model.train_on_batch(x,y)
        return loss

    def execute(self,x):
        return self.model.predict(x)

    def evaluate(self):
        return self.model.evaluate()

    def save(self,filename):
        if self.mode is None:
            return False
        self.model.save(filename)
        return True

    def load(self,filename):
        self.model = load_model(filename)

if __name__=='__main__':
    model = Model(size=(4,4))
    model.init()