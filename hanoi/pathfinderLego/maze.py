import math, random, types, copy
from enum import Enum

class CellType(Enum):
    Empty = 1
    Block = 2 

class CellMark(Enum):
    No = 0
    Start = 1
    End = 2

class Cell:
    def __init__(self, type = CellType.Empty, pos = None):
        self.type = type
        self.count = 0
        self.mark = CellMark.No
        self.path_from = None
        self.pos = pos

class CellGrid:
    def __init__(self, board):
        self.board = board

    def get_size(self):
        return [len(self.board), len(self.board[0])]

    def at(self, pos):
        return self.board[pos[0]][pos[1]]

    def clone(self):
        return CellGrid(copy.deepcopy(self.board))

    def clear_count(self, count):
        for o in self.board:
            for i in o:
                i.count = count
                i.path_from = None

    def is_valid_point(self, pos):
        sz = self.get_size()
        return pos[0] >= 0 and pos[1] >= 0 and pos[0] < sz[0] and pos[1] < sz[1]

def create_maze(E):
    flag = 0
    line = E.splitlines()
    y = len(line)
    br = line[0].split(' ')
    x = len(br)
    board = [[Cell(type = CellType.Empty, pos = [ix,iy]) for iy in range(y)] for ix in range(x)]
    for j in range(0,y):
        br = line[-1 - j].split(' ')
        for i in range(0,x):
            if br[i] == 'O':
                board[i][j].type = CellType.Block
            elif br[i] == 'R':
                flag = 1 
                start_x = i
                start_y = j
                #end_x = i
                #end_y = j
            elif br[i] == 'G':
                end_x = i
                end_y = j
            else: {}

    if flag == 0:
        return None

    return types.SimpleNamespace(board = CellGrid(board),
                                start = [start_x, start_y],
                                end = [end_x, end_y])

def add_point(a,b):
    return [a[0] + b[0], a[1] + b[1]]
 