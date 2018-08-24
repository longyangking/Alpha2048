import numpy as np 
import threading
from . import nativeUI
from . import viewer

import sys
from PyQt5.QtWidgets import QWidget, QApplication,QDesktopWidget
from PyQt5.QtCore import * 
from PyQt5.QtGui import *

class UI(threading.Thread):
    def __init__(self,pressaction,boardinfo,sizeunit=100):
        threading.Thread.__init__(self)
        self.ui = None
        self.app = None

        self.boardinfo = boardinfo
        self.sizeunit = sizeunit
        self.pressaction = pressaction
    
    def run(self):
        self.app = QApplication(sys.argv)
        self.ui = nativeUI.nativeUI(pressaction=self.pressaction,boardinfo=self.boardinfo,sizeunit=self.sizeunit)
        self.app.exec_()

    def setboard(self,boardinfo):
        while not self.ui:
            pass
        return self.ui.setboard(boardinfo)
    
    def gameend(self,score):
        self.ui.gameend(score)

class Viewer(threading.Thread):
    def __init__(self, boards, scores,sizeunit=100):
        threading.Thread.__init__(self)
        self.ui = None
        self.app = None

        self.boards = boards
        self.scores = scores
        self.sizeunit = sizeunit
    
    def run(self):
        self.app = QApplication(sys.argv)
        self.ui = viewer.Viewer(
            boards=self.boards,
            scores=self.scores,
            sizeunit=self.sizeunit)
        self.app.exec_()