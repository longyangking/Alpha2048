import numpy as np 

class Computer:
    def __init__(self):
        pass

    def play(self,maze):
        pass

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