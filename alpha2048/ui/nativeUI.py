import numpy as np 
import sys
import Config
from PyQt5.QtWidgets import QWidget, QApplication,QDesktopWidget
from PyQt5.QtCore import * 
from PyQt5.QtGui import *

class nativeUI(QWidget):
    playsignal = pyqtSignal(int) 

    def __init__(self,pressaction,boardinfo,sizeunit=50):
        super(nativeUI,self).__init__(None)

        self.boardinfo = boardinfo
        self.sizeunit = sizeunit

        self.ax = sizeunit
        self.ay = sizeunit

        self.playstatus = False

        self.isgameend = False

        self.pressaction = pressaction

        self.score = 0
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
        self.setWindowIcon(QIcon('./ui/icon.png'))

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
        if self.isgameend:
            self.drawgameend(qp)
        qp.end()
  
    def keyPressEvent(self,e):
        mode = 0
        if e.key() == Qt.Key_Up:
            mode = 4
        elif e.key() == Qt.Key_Down:
            mode = 3
        elif e.key() == Qt.Key_Left:
            mode = 1
        elif e.key() == Qt.Key_Right:
            mode = 2
            
        if mode != 0:
            self.playsignal.emit(mode)

    def gameend(self,score):
        self.isgameend = True
        self.score = score

    def drawgameend(self,qp):
        size =  self.geometry()
        qp.setPen(0)
        qp.setBrush(QColor(200, 200, 200, 180))
        width = size.width()/5*4
        height = size.height()/3
        qp.drawRect(size.width()/2-width/2, size.height()/2-height/2, width, height)

        qp.setPen(QColor(0,0,0))
        font = qp.font()
        font.setPixelSize(self.sizeunit/2)
        qp.setFont(font)
        qp.drawText(QRect(size.width()/2-width/2, size.height()/2-height/2, width, height),	
                    0x0004|0x0080,str("Score: " + str(self.score)))

    def resizeEvent(self,e):
        (Nx,Ny) = self.boardinfo.shape
        size =  self.geometry()
        width = size.width()
        height = size.height()
        self.ax = width/Nx
        self.ay = height/Ny

    def drawboard(self,qp):
        (Nx,Ny) = self.boardinfo.shape
        qp.setPen(QColor(0, 0, 0))
        for i in range(Nx-1):
            qp.drawLine((i+1)*self.ax, 0, (i+1)*self.ax, Ny*self.ay)   
        for j in range(Ny-1):
            qp.drawLine(0, (j+1)*self.ay, Nx*self.ax, (j+1)*self.ay) 

    def drawnumbers(self, qp):
        (Nx,Ny) = self.boardinfo.shape
        font = qp.font()
        font.setPixelSize(self.sizeunit/2)
        qp.setFont(font)
        for i in range(Nx):
            for j in range(Ny):
                if self.boardinfo[i,j]==0:
                    qp.setPen(QColor(100,100,100,127))
                else:
                    qp.setPen(QColor(0,0,0))
                qrect = QRect(j*self.ax, i*self.ay, self.ax, self.ay)
                qp.drawText(qrect,0x0004|0x0080, str(self.boardinfo[i,j]))
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    boardinfo = np.array([[0,0,0,0],[0,2,0,0],[0,0,0,2],[0,0,2,0]])
    sizeunit = 100
    ex = nativeUI(pressaction=lambda x:x,boardinfo=boardinfo,sizeunit=sizeunit)
    sys.exit(app.exec_())

