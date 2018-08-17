import ui
import numpy as np 
from gameutils import Board

class Human:
    def __init__(self):
        self.direction = 0
        self.activate = False

    def setdirection(self,mode):
        if mode == 1:
            self.direction = 0
        elif mode == 2:
            self.direction = 1
        elif mode == 3:
            self.direction = 2
        elif mode == 4:
            self.direction = 3
        
        self.activate = True

    def play(self, state):
        if self.activate:
            self.activate = False
            return self.direction
        return -1

class GameEngine:
    def __init__(self, state_shape, player):
        self.player = player
        self.state_shape = state_shape
        self.board = Board(size=self.state_shape[:2])

        self.states = list()
        self.boards = list()

    def get_board(self):
        return self.board.get_board()

    def start(self):
        self.board.init()

    def update_state(self):
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

    def update(self):
        self.board.play(self.player.play(state=self.get_state()))

        return self.board.status()

    def get_score(self):
        return self.board.get_score()

class Game2048:
    def __init__(self, state_shape, player=None, verbose=False):
        self.state_shape = state_shape

        self.gameengine = None
        self.ui = None

        self.player = player
        self.verbose = verbose

    def start(self,sizeunit=100):
        self.gameengine = GameEngine(state_shape=self.state_shape,player=self.player)
        self.gameengine.start()

        boardinfo = self.gameengine.get_board()

        self.ui = ui.UI(pressaction=self.player.setdirection,boardinfo=boardinfo,sizeunit=sizeunit)
        self.ui.start()
        
        while not self.gameengine.update():
            self.ui.setboard(boardinfo=self.gameengine.get_board())

        self.ui.gameend(self.gameengine.get_score())

        if self.verbose:
            print('Game End with score: {0}'.format(self.gameengine.get_score()))

    def start_ai(self):
        pass