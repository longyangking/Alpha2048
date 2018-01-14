import ui
import GameEngine
import Player

class Game2048:
    def __init__(self,size=[4,4]):
        self.size = size

        self.gameengine = None
        self.ui = None
        self.player = Player.Human()

    def start(self,sizeunit=100):
        self.gameengine = GameEngine.GameEngine(size=self.size,player=self.player)
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