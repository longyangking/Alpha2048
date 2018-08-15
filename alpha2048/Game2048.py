import ui
import numpy as np 
from gameutils import Board

class Human:
    def __init__(self):
        self.direction = 0
        self.activate = False

    def setdirection(self,mode):
        if mode == 1:
            self.direction = 1
        elif mode == 2:
            self.direction = 2
        elif mode == 3:
            self.direction = 3
        elif mode == 4:
            self.direction = 4
        
        self.activate = True

    def play(self,boardinfo):
        if self.activate:
            self.activate = False
            return self.direction
        return 0

class GameEngine:
    def __init__(self,player,size=[4,4]):
        self.player = player
        self.size = size
        self.board = Board(size=size)

    def getboard(self):
        return self.board.boardinfo()

    def start(self):
        self.board.init()

    def update(self):
        self.board.play(self.player.play(boardinfo=self.board.boardinfo()))

        return self.board.status()

    def score(self):
        return self.board.score()

class Game2048:
    def __init__(self,size=[4,4]):
        self.size = size

        self.gameengine = None
        self.ui = None
        self.player = Human()

    def start(self,sizeunit=100):
        self.gameengine = GameEngine(size=self.size,player=self.player)
        self.gameengine.start()

        boardinfo = self.gameengine.getboard()
        self.ui = ui.UI(pressaction=self.player.setdirection,boardinfo=boardinfo,sizeunit=sizeunit)
        self.ui.start()
        
        
        while not self.gameengine.update():
            self.ui.setboard(boardinfo=self.gameengine.getboard())

        self.ui.gameend(self.gameengine.score())

        print('Game End')

if __name__=="__main__":
    size = [4,4]
    game2048 = Game2048(size)
    game2048.start()