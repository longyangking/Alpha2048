import numpy as np 
import Board

class GameEngine:
    def __init__(self,player,size=[4,4]):
        self.player = player
        self.size = size
        self.board = Board.Board(size=size)

    def getboard(self):
        return self.board.boardinfo()

    def start(self):
        self.board.init()

    def update(self):
        self.board.play(self.player.play(boardinfo=self.board.boardinfo()))

        return self.board.status()

    def score(self):
        return self.board.score()