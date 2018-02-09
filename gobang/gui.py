# !/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter, time
import math
from gobang.point import Point
from gobang.board import BoardManager
from gobang.ai import AIManager


class Chess_Board_Canvas(tkinter.Canvas):
    # 棋盘绘图板,继承自Tkinter.Canvas类
    def __init__(self, master=None, height=0, width=0, player1='player', player2='ai'):
        '''
        棋盘类初始化
        :param master: 画到那个对象
        :param height: 棋盘的高度
        :param width: 棋盘的宽度
        '''
        self.master = master
        self.height = height
        self.width = width
        self.player1 = player1
        self.player2 = player2
        tkinter.Canvas.__init__(self, master, height=height, width=width)
        # self.step_record_chess_board = record.Step_Record_Chess_Board()
        self.board = BoardManager(player1, player2)
        self.ai = AIManager('gobang/model.h5')
        self.NOISE = 0.01
        self.init_chess_board_points()    # 画点
        self.init_chess_board_canvas()    # 绘制棋盘
        self.update()

    def init_chess_board_points(self):
        '''
        生成各个棋盘点,根据棋盘坐标生成像素表座
        并且保存到 chess_board_points 属性
        :return:
        '''
        self.chess_board_points = [[None for i in range(15)] for j in range(15)]

        for i in range(15):
            for j in range(15):
                self.chess_board_points[i][j] = Point(i, j)  # 棋盘坐标向像素坐标转化

    def init_chess_board_canvas(self):
        for i in range(15):  # 绘制竖线
            self.create_line(self.chess_board_points[i][0].pixel_x, self.chess_board_points[i][0].pixel_y, self.chess_board_points[i][14].pixel_x, self.chess_board_points[i][14].pixel_y)

        for j in range(15):  # 绘制横线
            self.create_line(self.chess_board_points[0][j].pixel_x, self.chess_board_points[0][j].pixel_y, self.chess_board_points[14][j].pixel_x, self.chess_board_points[14][j].pixel_y)

        for i in range(15):  # 绘制椭圆,但是这个功能似乎是要加强交点的视觉效果,但是效果一般,视错觉没有出现
            for j in range(15):
                r = 1
                self.create_oval(self.chess_board_points[i][j].pixel_x-r, self.chess_board_points[i][j].pixel_y-r, self.chess_board_points[i][j].pixel_x+r, self.chess_board_points[i][j].pixel_y+r);

    def auto_play(self):
        # time.sleep(0.5)
        i, j = self.ai.get_move(self.board.get_board(self.board.cur_player), self.NOISE)
        if self.board.cur_player == 0:
            self.create_oval(self.chess_board_points[i][j].pixel_x - 10, self.chess_board_points[i][j].pixel_y - 10,
                             self.chess_board_points[i][j].pixel_x + 10, self.chess_board_points[i][j].pixel_y + 10,
                             fill='white')
        else:
            self.create_oval(self.chess_board_points[i][j].pixel_x - 10, self.chess_board_points[i][j].pixel_y - 10,
                             self.chess_board_points[i][j].pixel_x + 10, self.chess_board_points[i][j].pixel_y + 10,
                             fill='black')
        self.update()
        self.board.move(self.board.cur_player, (i, j))

        result = self.board.check_win(self.board.cur_player)

        if result:
            print('Player %d win!' % (self.board.cur_player,))

        if result or self.board.empty == 0:
            self.create_text(240, 550, text='Game over!')
            print('Game over!')
            self.unbind('<Button-1>')
        else:
            self.board.cur_player = 1 - self.board.cur_player
            if self.board.players[self.board.cur_player] == 'ai':
                self.auto_play()

    def click1(self, event): # 为何是click1因为关键字重复
        if self.board.players[self.board.cur_player] != 'player':
            return
        for i in range(15):
            for j in range(15):
                square_distance = math.pow((event.x - self.chess_board_points[i][j].pixel_x), 2) + math.pow((event.y - self.chess_board_points[i][j].pixel_y), 2)
                if (square_distance <= 200) and (self.board.board[i][j][2] == 1):  # 距离小于14并且没有落子
                    if self.board.cur_player == 0:
                        self.create_oval(self.chess_board_points[i][j].pixel_x-10, self.chess_board_points[i][j].pixel_y-10, self.chess_board_points[i][j].pixel_x+10, self.chess_board_points[i][j].pixel_y+10, fill='white')
                    else:
                        self.create_oval(self.chess_board_points[i][j].pixel_x-10, self.chess_board_points[i][j].pixel_y-10, self.chess_board_points[i][j].pixel_x+10, self.chess_board_points[i][j].pixel_y+10, fill='black')

                    self.board.move(self.board.cur_player, (i, j))
                    # 插入落子数据,落子最多225,这个程序没有实现AI

                    result = self.board.check_win(self.board.cur_player)
                    # 判断是否有五子连珠
                    if result:
                        print('Player %d win!' % (self.board.cur_player,))
                    if result or self.board.empty == 0:
                        self.create_text(240, 550, text='Game over!')
                        print('Game over!')
                        # 解除鼠标左键绑定
                        self.unbind('<Button-1>')
                    else:
                        self.board.cur_player = 1 - self.board.cur_player
                        if self.board.players[self.board.cur_player] == 'ai':
                            self.auto_play()

    def restart(self):
        self.delete('all')
        self.init_chess_board_points()  # 画点
        self.init_chess_board_canvas()  # 绘制棋盘
        self.board = BoardManager(self.player1, self.player2)
        self.bind('<Button-1>', self.click1)
        if self.board.players[self.board.cur_player] == 'ai':
            self.auto_play()


class ChessBoardFrame(tkinter.Frame):
    def __init__(self, master=None, player1='player', player2='ai'):
        tkinter.Frame.__init__(self, master)
        self.player1 = player1
        self.player2 = player2
        self.create_widgets()

    def create_widgets(self):
        self.chess_board_label_frame = tkinter.LabelFrame(self, text="Chess Board", padx=5, pady=5)
        self.chess_board_canvas = Chess_Board_Canvas(self.chess_board_label_frame, height=520, width=480,
                                                     player1=self.player1, player2=self.player2)

        self.chess_board_canvas.bind('<Button-1>', self.chess_board_canvas.click1)
        self.button = tkinter.Button(self, text='重新开始', command=(self.chess_board_canvas.restart))
        self.chess_board_label_frame.pack()
        self.chess_board_canvas.pack()
        self.button.pack()

