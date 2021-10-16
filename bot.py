import random
from board import Board

class Bot:
    def bot_turn(self, Board, color, change_fxn):
        print("\nBot Move")
        n = self.random_move(Board, color)
        if n is None:
            return None
        x,y = n

    def all_valid_moves(self, color):
        m = {(x,y) for x in range(8) for y in range(8) if self.is_valid_move(self.board,x,y,color)}
        print(m)
        return m

    def random_move(self, color) -> tuple:
        # maybe Optional[tuple]
        s = list(Board.all_valid_moves(color))
        return random.choice(s) if len(s) else None



def naive_mini_max(board):
    """ mini max that foreshadows next move by points """
    pass

#mini max that foreshadows next n moves
def mini_max(board, n):
    pass


if __name__ == "__main__":
    b = Bot()
