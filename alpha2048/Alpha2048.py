import os
import numpy as np
import GameEngine 
import AlphaModel
import sys, getopt

class Alpha2048:
    def __init__(self,size,groupsize):
        self.models = list()
        self.size = size
        for _ in range(groupsize):
            model = AlphaModel.Model(size=self.size)
            self.models.append(model)            

    def init(self,verbose=False):
        '''
        Initiate Game Engine and Learning Pre-Process
        '''
        for i in range(len(self.models)):
            if verbose:
                print('Alpha Models: Initiating {num}th...'.format(num=i+1))
            self.models[i].init()  
        if verbose:
            print('Alpha Models: Initiation successful!')

    def train(self,verbose=False):
        '''
        Train Models
        '''
        
        
    def selfplay(self,model,depth=5):
        '''
        
        
        

        

    def savemodels(self,path,fileformat='.h5'):
        '''
        Save models
        '''
        path = path.strip()
        path = path.rstrip()

        if not os.path.exists(path):
            os.makedirs(path)
        
        for i in range(len(self.models)):
            filename = path + '\\' + str(i) + fileformat
            self.models[i].save(filename)
        
    def loadmodels(self,path,fileformat='.h5'):
        '''
        Load models
        '''
        models = list()
        filelist = os.listdir(path)
        for f in filelist:
            if os.path.splitext(f)[1] == fileformat:
                filename = path + '\\' + f
                model = AlphaModel.Model(size=self.size) # Bug here
                model.load(filename)
                models.append(model)
        self.models = models

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "s:h",["help","train","retrain","test"])
    groupsize=10
    size = [4,4]
    models = None
    for op, value in opts:
        if op in ('--help','-h'):
            print('''
            Parameters:
                -h/--help:  show help information
                --train:    train model on batches
                --test:     test models and show test results
                --retrain:  retrain model
            ''')
            
        if op == '-s':
            groupsize = value
            
        if op == '--retrain':
            models = Alpha2048(size=size,groupsize=groupsize)
            models.init(verbose=True)
            