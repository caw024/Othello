import random

class Bot:
    def __call__(self, board):
        self.board = board

    def bot_turn(self, color) -> None:
        print("\nBot Move")
        n = self.random_move(color)
        if n is None:
            print("No valid moves for bot")
            return None
        x,y = n
        print(f"Moved to {n}")
        self.board.update(x, y, color)


    def random_move(self, color) -> tuple:
        # maybe Optional[tuple]
        s = list(self.board.all_valid_moves(color))
        return random.choice(s) if len(s) else None


def naive_mini_max(board):
    """ mini max that foreshadows next move by points """
    pass

#mini max that foreshadows next n moves
def mini_max(board, n):
    pass


if __name__ == "__main__":
    b = Bot()
