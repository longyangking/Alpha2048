import numpy as np 
import time
from ai import AI
from gameutils import Board

class SelfplayEngine:
    def __init__(self, state_shape, ai, verbose):
        self.state_shape = state_shape
        self.ai = ai

        self.verbose = verbose

        # train data
        self.boards = list()
        self.states = list()
        self.scores = list()
        self.actions = list()

    def update_states(self):
        channel = self.state_shape[-1]
        state = np.zeros(self.state_shape)
        n_boards = len(self.boards)
        for i in range(channel):
            if i+1 <= n_boards:
                state[:,:,-(i+1)] = self.boards[-(i+1)]

        self.states.append(state)
    
    def get_state(self):
        if len(self.states) == 0:
            state = np.zeros(self.state_shape)
        else:
            state = self.states[-1]
        return state

    def selfplay(self, state, epsilon):
        v = np.random.random()
        if v < epsilon:
            action = np.random.randint(4)
        else:
            action = self.ai.play(state=state)
        return action

    def start(self, epsilon=0.5):
        board = Board(size=self.state_shape[:2])
        board.init()

        # initiate the board
        self.boards.append(board.get_board())
        self.scores.append(board.get_score())

        # Main process
        flag = False
        while not flag:
            self.update_states()

            action = self.selfplay(state=self.get_state(), epsilon=epsilon)
            board.play(action)
            flag = board.status()

            actions = np.zeros(4)
            actions[action] = 1
            self.actions.append(actions)
            score = board.get_score()
            self.scores.append(score)
            self.boards.append(board.get_board())

        return self.states, self.actions, self.scores
    
class TrainAI:
    def __init__(self, 
        state_shape, 
        ai=None,
        verbose=False):

        self.state_shape = state_shape
        self.verbose = verbose
        
        if ai is None:
            self.ai = AI(
                state_shape=self.state_shape,
                action_dim=4,
                verbose=self.verbose)
        else:
            self.ai = ai

        self.losses = list()

    def get_losses(self):
        return self.losses

    def get_selfplay_data(self, n_round):
        states = list()
        actions = list()
        scores = list()

        if self.verbose:
            starttime = time.time()
            print("Start to self-play to get training data with rounds: [{0}]".format(n_round))

        for i in range(n_round):
            if self.verbose:
                print("{0}th self-play round...".format(i+1))

            engine = SelfplayEngine(
                state_shape=self.state_shape, 
                ai=self.ai, 
                verbose=self.verbose)
            _states, _actions, _scores = engine.start()
            
            for k in range(len(_states)):
                states.append(_states[k])
                actions.append(_actions[k])
                scores.append(_scores[k])

        if self.verbose:
            endtime = time.time()
            count = len(scores)
            print("End of selfplay with time [{0:.2f}s] and data size [{1}].".format(endtime-starttime, count))

        states = np.array(states)
        actions = np.array(actions)
        scores = np.array(scores)
        
        return states, actions, scores
            
    def update_ai(self, dataset):
        if self.verbose:
            print("Start to update network of AI model.")

        history = self.ai.train(dataset, epochs=30, batch_size=32)

        if self.verbose:
            print("End of updating network.")

        return history.history['loss']

    def start(self, filename):
        
        n_epochs = 1000
        n_round = 30
        n_checkpoint = 20

        if self.verbose:
            print("Start to train AI model with epochs [{0}], selfplay round [{1}], checkpoint [{2}]".format(n_epochs, n_round, n_checkpoint))

        for i in range(n_epochs):
            if self.verbose:
                print("{0}th epoch of training AI model.".format(i+1))

            dataset = self.get_selfplay_data(n_round)
            losses = self.update_ai(dataset)

            self.losses.extend(losses)

            if (i+1)%n_checkpoint == 0:
                if self.verbose:
                    print("Checkpoint: Saving AI model with filename [{0}]...".format(filename),end="")
                
                self.ai.save_nnet(filename)

                if self.verbose:
                    print("OK!")
