import numpy as np 
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
            action = self.selfplay(state=self.get_state(), epsilon=epsilon)
            board.play(action)
            flag = board.status()

            self.actions.append(action)
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

    def get_selfplay_data(self, n_round):

    def update_ai(self, dataset):

    def start(self):
