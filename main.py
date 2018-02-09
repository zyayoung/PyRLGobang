#!/usr/bin/env python
#-*- coding: utf-8 -*-

from gobang.gui import ChessBoardFrame
import tkinter

if __name__ == '__main__':
    window = tkinter.Tk()
    gui_chess_board = ChessBoardFrame(window)
    gui_chess_board.pack()
    window.mainloop()
