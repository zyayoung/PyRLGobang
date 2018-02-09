class PlayerManager:
    def get_move(self, board):
        ipt = input()
        while board[ord(ipt[0])-ord('a')][ord(ipt[1])-ord('a')][2] != 1:
            ipt = input('invalid place\n')
        return ord(ipt[0])-ord('a'), ord(ipt[1])-ord('a')
