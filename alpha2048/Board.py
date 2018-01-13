import numpy as np 

class Board:
    def __init__(self,size=[4,4]):
        self.size = size
        self.board = np.zeros(size)
        self.validpositions = list(range(size[0]*size[1]))

    def play(self,direction):
        if direction not in [1,2,3,4]:
            return False

        status = self.roll(direction)
        if status:
            self.randomset()
            
        return True

    def roll(self,direction):
        board = np.zeros(self.size)
        if direction == 1:              # Move left
            for i in range(self.size[1]):
                n = 0
                for j in range(self.size[0]):
                    if self.board[i,j] != 0:
                        if self.board[i,j] == board[i,n]:
                            board[i,n] += board[i,n]
                        else:
                            if board[i,n]!=0: n += 1
                            board[i,n] = self.board[i,j]

        elif direction == 2:            # Move right
            for i in range(self.size[1]):
                n = self.size[0]-1
                for j in range(self.size[0]-1,0,-1):
                    if self.board[i,j] != 0:
                        if self.board[i,j] == board[i,n]:
                            board[i,n] += board[i,n]
                        else:
                            if board[i,n]!=0: n -= 1
                            board[i,n] = self.board[i,j]
                        
        elif direction == 3:            # Move down
            for j in range(self.size[0]):
                m = 0
                for i in range(self.size[1]):
                    if self.board[i,j] != 0:
                        if self.board[i,j] == board[m,j]:
                            board[m,j] += board[m,j]
                        else:
                            if board[m,j]!=0: m += 1
                            board[m,j] = self.board[i,j]                        

        elif direction == 4:            # Move up
            for j in range(self.size[0]):
                m = self.size[1]-1
                for i in range(self.size[1]-1,0,-1):
                    if self.board[i,j] != 0:
                        if self.board[i,j] == board[m,j]:
                            board[m,j] += board[m,j]
                        else:
                            if board[m,j]!=0: m -= 1
                            board[m,j] = self.board[i,j]

        status = np.sum((self.board-board))!=0
        self.board = board
        return status
        
    def randomset(self):
        '''
        Put number in blank grid randomly
        '''
        index = np.random.randint(len(self.validpositions))
        pos = self.validpositions[index]
        self.validpositions.remove(pos)

        x = int(pos/self.size[0])
        y = pos%self.size[0]
        self.board[x,y] = 2
    
    def boardinfo(self):
        return self.board
    
    def status(self):
        status = np.sum(self.board!=0) == self.size[0]*self.size[1]
        return status
