import numpy as np
import os
os.environ['KERAS_BACKEND'] = 'theano'
from keras.models import load_model
from keras import backend as K
from keras.utils.layer_utils import convert_all_kernels_in_model

class BoardManager:
    def __init__(self, player1='none', player2='none', record=False):
        self.board = np.concatenate((np.zeros((15, 15, 2)), np.ones((15, 15, 1))), 2)
        self.history = (([], []), ([], []))
        self.record = record
        self.judge_model = load_model('gobang/judge.h5')
        if K.backend() == 'theano':
            convert_all_kernels_in_model(self.judge_model)
        self.players = [player1,player2]
        self.cur_player = 0
        self.empty = 15*15

    def move(self, player, pos):
        x = int(pos[0])
        y = int(pos[1])
        if self.board[x][y][2] == 1:
            if self.record:
                self.history[player][0].append(self.get_board(player).copy())
                y_tmp = np.zeros((15, 15), dtype='float32')
                y_tmp[x][y] = 1.0
                self.history[player][1].append(y_tmp)
            self.board[x][y][2] = 0
            self.board[x][y][player] = 1
            self.empty -= 1
            return True
        else:
            return False

    def get_board(self, reverse=False):
        if reverse:
            rev_board = self.board.copy()
            rev_board[:, :, [0, 1]] = self.board[:, :, [1, 0]]
            return rev_board
        else:
            return self.board

    def show(self, pos=(-1, -1)):
        for i in range(15):
            print(chr(ord('a') + i), end=' ')
            for j in range(15):
                if i == pos[0] and j == pos[1]:
                    print('X', end=' ')
                elif self.board[i][j][0] == 1:
                    print('x', end=' ')
                elif self.board[i][j][1] == 1:
                    print('o', end=' ')
                else:
                    print('.', end=' ')
            print()
        print(' ', end=' ')
        for j in range(15):
            print(chr(ord('a') + j), end=' ')
        print()

    def check_win(self, player=0):
        pre = self.judge_model.predict(self.board[:, :, player].reshape(-1, 15, 15, 1))[0][0]
        if pre > 1e-10:
            return True
        else:
            return False
