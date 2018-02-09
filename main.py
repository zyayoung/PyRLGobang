#!/usr/bin/env python
#-*- coding: utf-8 -*-

from gobang.gui import ChessBoardFrame
import tkinter, sys
if __name__ == '__main__':
    window = tkinter.Tk()
    if len(sys.argv) == 1:
        gui_chess_board = ChessBoardFrame(window)
        gui_chess_board.pack()
        window.mainloop()
    elif len(sys.argv) == 3:
        gui_chess_board = ChessBoardFrame(window, player1=sys.argv[1], player2=sys.argv[2])
        gui_chess_board.pack()
        window.mainloop()
    else:
        print('usage: python main.py [player|ai] [player|ai]')
