import numpy as np 

class MCTS:
    def __init__(self,model,size,L=10):
        '''
        Monte Carlo Tree Search: Self play algorithm
        '''
        self.states = list()
        self.actions = list()
        self.N = list()
        self.W = list()
        self.Q = list()
        self.P = list()
        self.model = model
        self.L = L

    def expand(self,state):
        '''
        Return values in Monte Carlo Tree:
            N(s,a), W(s,a), Q(s,a), P(s,a)

        Actions:
            a = 1: Left
            a = 2: Right
            a = 3: Up
            a = 4: Down
        '''
        actions = [1,2,3,4]
        if  len(self.states) == 0:
            self.states.append(state)
            self.N.append(0)
            self.W.append(0)
            self.Q.append(0)

            Ps,a = self.model.execute(state)
            
            self.P.append(Ps)
            self.actions.append(action)

        for i in range(self.states):


    def update(self,state,action):
