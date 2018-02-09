import numpy as np
import os, time
os.environ['KERAS_BACKEND'] = 'theano'
from keras.models import load_model
from gobang.board import BoardManager
from keras import backend as K
from keras.utils.layer_utils import convert_all_kernels_in_model


class AIManager:
    def __init__(self, model_path='model.h5'):
        self.model = load_model(model_path)
        self.kill_model = load_model('gobang/judge_kill.h5')
        if K.backend() == 'theano':
            convert_all_kernels_in_model(self.model)
            convert_all_kernels_in_model(self.kill_model)

    def get_move(self, board, noise=1e-4, judge_kill=True):
        if judge_kill:
            p = self.kill_model.predict(board[:, :, :2].reshape(-1, 15, 15, 2))[0]
            if p.max() > 1e-10:
                pi = p.argmax()
                pl = pi % 20
                pi = (pi - pi % 20) / 20
                j = int(pi % 15)
                i = int((pi - j) / 15)
                # print('kill', p.argmax())
                return i, j
            rev_board = board.copy()
            rev_board[:, :, [0, 1]] = board[:, :, [1, 0]]
            p = self.kill_model.predict(rev_board[:, :, :2].reshape(-1, 15, 15, 2))[0]
            if p.max() > 1e-10:
                pi = p.argmax()
                pl = pi % 20
                pi = (pi - pi % 20) / 20
                j = int(pi % 15)
                i = int((pi - j) / 15)
                # print('antikill')
                # time.sleep(2)
                return i, j

        noise = np.random.uniform(0, noise, (15, 15))
        pre = self.model.predict(board.reshape(-1, 15, 15, 3)).reshape(15, 15)
        pre += board[:, :, 2] + noise
        pre = np.where(pre == pre.max())
        return pre[0][0], pre[1][0]
