import pygame
from pygame.locals import *
class Game:
    def __init__(self, id):
        self.currentPlayer = 0
        self.id = id
        self.grid = [[None, None, None],
                    [None, None, None],
                    [None, None, None]]
        self.wins = [0, 0]
        self.ready = False
        self.winner = None
        self.players = [0, 1]

    def switchCurrentPlayer(self):
        if self.currentPlayer == 0:
            self.currentPlayer = 1
        else:
            self.currentPlayer = 0

    def getGrid(self):
        return self.grid

    def connected(self):
        return self.ready

    def isThereAFreeSpace(self):
        result = False
        for row in self.grid:
            if None in row:
                return True
            else:
                result = False
        return result

    def setValue(self, data, player):
        x = int(data[0])
        y = int(data[1])
        if self.isThereAnExactFreeSpace(x,y):
            self.grid[x][y] = self.players[player]
            self.switchCurrentPlayer()
            self.setWinner()

    def isThereAnExactFreeSpace(self, x, y):
        if self.grid[x][y] == None:
            return True
        else:
            return False

    def isThereWinner(self):
        if self.winner is None:
            return False
        else:
            return True

    def isGameNotEnded(self):
        if (self.isThereWinner() or not self.isThereAFreeSpace()):
            return False
        else:
            return True

    def setWinner(self):

        for row in range(0, 3):
            if ((self.grid[row][0] == self.grid[row][1] == self.grid[row][2]) and
                    (self.grid[row][0] is not None)):
                # this row won
                self.winner = self.grid[row][0]
                break

        # check for winning columns
        for col in range(0, 3):
            if (self.grid[0][col] == self.grid[1][col] == self.grid[2][col]) and (self.grid[0][col] is not None):
                # this column won
                self.winner = self.grid[0][col]
                break

        # check for diagonal winners
        if (self.grid[0][0] == self.grid[1][1] == self.grid[2][2]) and (self.grid[0][0] is not None):
            # game won diagonally left to right
            self.winner = self.grid[0][0]

        if (self.grid[0][2] == self.grid[1][1] == self.grid[2][0]) and (self.grid[0][2] is not None):
            # game won diagonally right to left
            self.winner = self.grid[0][2]

    def resetBoard(self, player):
        self.grid = [[None, None, None],
                    [None, None, None],
                    [None, None, None]]
        if(self.winner == player):
            self.wins[player] += 1
        self.winner = None
        self.currentPlayer = 0




