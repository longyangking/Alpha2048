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

    def update(self, is_ai=False):
        if is_ai:
            actions = np.zeros(4)
            action_prob, value = self.player.evaluate_function(state=self.get_state())
            availables = self.board.get_availables()
            actions[availables] = action_prob[availables]
            action = np.argmax(actions)
        else:
            action = self.player.play(state=self.get_state())
            
        self.board.play(action)
        return self.board.status()

    def get_score(self):
        return self.board.get_score()

class Game2048:
    def __init__(self, state_shape, player, verbose=False):
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

class VisualizeAI:
    def __init__(self, state_shape, ai, verbose=False):
        self.state_shape = state_shape
        self.ai = ai
        self.verbose = verbose

        self.boards = list()
        self.scores = list()

    def start(self):
        if self.verbose:
            print("Start to run a new game to get result...")

        gameengine = GameEngine(state_shape=self.state_shape, player=self.ai)
        gameengine.start()

        self.boards.append(gameengine.get_board())
        self.scores.append(gameengine.get_score())

        while not gameengine.update(is_ai=True):
            self.boards.append(gameengine.get_board())
            self.scores.append(gameengine.get_score())

        if self.verbose:
            print("End of runing game with final score: [{0}]".format(self.scores[-1]))

    def view(self, sizeunit=100):
        viewer = ui.Viewer(
            boards=self.boards,
            scores=self.scores,
            sizeunit=sizeunit
            )

        viewer.start()