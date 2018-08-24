import numpy as np 

class Board:
    def __init__(self,size=[4,4], board=None):
        self.size = size

        if board is not None:
            self.board = board
        else:
            self.board = np.zeros(size).astype(int)

    def init(self):
        self.board = np.zeros(self.size).astype(int)
        self.randomset()
        self.randomset()

    def play(self, direction):
        if direction not in [0,1,2,3]: # No actions
            return False

        status = self.roll(direction)
        if status:
            self.randomset()
            
        return True

    def roll(self,direction):
        board = np.zeros(self.size).astype(int)
        if direction == 0:              # Move left
            for i in range(self.size[1]):
                n = 0
                for j in range(self.size[0]):
                    if self.board[i,j] != 0:
                        if self.board[i,j] == board[i,n]:
                            board[i,n] += board[i,n]
                        else:
                            if board[i,n]!=0: n += 1
                            board[i,n] = self.board[i,j]

        elif direction == 1:            # Move right
            for i in range(self.size[1]):
                n = self.size[0]-1
                for j in range(self.size[0]-1,-1,-1):
                    if self.board[i,j] != 0:
                        if self.board[i,j] == board[i,n]:
                            board[i,n] += board[i,n]
                        else:
                            if board[i,n]!=0: n -= 1
                            board[i,n] = self.board[i,j]
                        
        elif direction == 2:            # Move down
            for j in range(self.size[0]):
                m = self.size[1]-1
                for i in range(self.size[1]-1,-1,-1):
                    if self.board[i,j] != 0:
                        if self.board[i,j] == board[m,j]:
                            board[m,j] += board[m,j]
                        else:
                            if board[m,j]!=0: m -= 1
                            board[m,j] = self.board[i,j]                      

        elif direction == 3:            # Move up
            for j in range(self.size[0]):
                m = 0
                for i in range(self.size[1]):
                    if self.board[i,j] != 0:
                        if self.board[i,j] == board[m,j]:
                            board[m,j] += board[m,j]
                        else:
                            if board[m,j]!=0: m += 1
                            board[m,j] = self.board[i,j] 

        status = (np.sum(np.square(self.board-board))!=0)
        self.board = board.copy()
        return status
        
    def randomset(self):
        '''
        Put number in blank grid randomly
        '''
        validpositions = list()
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.board[i,j] == 0:
                    validpositions.append(i*self.size[1]+j)
        index = np.random.randint(len(validpositions))
        pos = validpositions[index]
        validpositions.remove(pos)

        x = int(pos/self.size[0])
        y = pos%self.size[0]
        self.board[x,y] = 2

    def get_availables(self):
        availables = list()
        for action in np.arange(4):
            if self.play_virtual(action):
                availables.append(action)

        return availables

    def play_virtual(self, direction):
        flag = True

        _board = np.copy(self.board)

        self.roll(direction)
        if (_board == self.board).all():
            flag = False

        self.board = _board
        return flag

    def get_board(self):
        return np.copy(self.board)

    def get_score(self):
        return np.max(self.board)
    
    def status(self):
        status = np.sum(self.board!=0) == self.size[0]*self.size[1]
        return status
