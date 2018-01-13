import numpy as np 
import sys
import Config
from PyQt5.QtWidgets import QWidget, QApplication,QDesktopWidget
from PyQt5.QtCore import * 
from PyQt5.QtGui import *

class nativeUI(QWidget):
    playsignal = pyqtSignal(tuple) 

    def __init__(self,pressaction,boardinfo,sizeunit=50):
        super(nativeUI,self).__init__(None)

        self.boardinfo = boardinfo
        self.sizeunit = sizeunit

        self.playstatus = False

        self.isgameend = False

        self.pressaction = pressaction

        self.playsignal.connect(self.pressaction) 
        self.initUI()

    def getboardinfo(self):
        return self.boardinfo

    def setboard(self,boardinfo):
        self.boardinfo = boardinfo
        self.playstatus = False
        self.update()

    def initUI(self):
        (Nx,Ny) = self.boardinfo.shape
        screen = QDesktopWidget().screenGeometry()
        size =  self.geometry()

        self.setGeometry((screen.width()-size.width())/2, 
                        (screen.height()-size.height())/2,
                        Nx*self.sizeunit, Ny*self.sizeunit)
        self.setWindowTitle("2048") 
        self.setWindowIcon(QIcon('icon.png'))

        # set Background color
        palette =  QPalette()
        palette.setColor(self.backgroundRole(), QColor(255, 255, 255))
        self.setPalette(palette)

        self.setMouseTracking(True)
        self.show()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawboard(qp)
        self.drawnumbers(qp)
        qp.end()
  
    def mousePressEvent(self,e):
        X = int(e.x()/self.sizeunit)
        Y = int(e.y()/self.sizeunit)
        if (self.chessboardinfo[X,Y] == 0) and not self.playstatus:
            self.chooseX = X
            self.chooseY = Y
            self.chessboardinfo[X,Y] = self.chessvalue
            self.playstatus = True
            self.playsignal.emit((X,Y))
            self.update()

    def chooseChess(self,qp):
        #qp.setBrush(QColor(0, 0, 0))
        qp.setPen(QColor(255, 0, 0))
        qp.setBrush(0)
        qp.drawEllipse((self.mousex+0.5)*self.sizeunit-self.R,
                (self.mousey+0.5)*self.sizeunit-self.R, 
                2*self.R, 2*self.R)

    def drawboard(self,qp):
        (Nx,Ny) = self.boardinfo.shape
        qp.setPen(QColor(0, 0, 0))
        for i in range(Nx-1):
            qp.drawLine((i+1)*self.sizeunit, 0, (i+1)*self.sizeunit,Ny*self.sizeunit)   
        for j in range(Ny-1):
            qp.drawLine(0, (j+1)*self.sizeunit, Ny*self.sizeunit, (j+1)*self.sizeunit) 

    def drawnumbers(self, qp):
        (Nx,Ny) = self.boardinfo.shape
        qp.setPen(QColor(0,0,0))
        font = qp.font()
        font.setPixelSize(self.sizeunit)
        qp.setFont(font)
        for i in range(Nx):
            for j in range(Ny):
                qrect = QRect(i*self.sizeunit, j*self.sizeunit, self.sizeunit, self.sizeunit)
                qp.drawText(qrect,0x0004|0x0080, str(self.boardinfo[i,j]))
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    boardinfo = np.array([[0,0,0,0],[0,2,0,0],[0,0,0,2],[0,0,2,0]])
    sizeunit = 100
    ex = nativeUI(pressaction=lambda x:x,boardinfo=boardinfo,sizeunit=sizeunit)
    sys.exit(app.exec_())

