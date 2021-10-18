from strategy import Random, MinMax, AlphaBetaMinMax

class Bot:
    """ Stores bot related activities """
    def __init__(self, strategy=Random):
        self.strategy = strategy()

    def __call__(self, board):
        self.board = board
        self.strategy(self.board)

    def bot_turn(self, color: str) -> None:
        print("Bot Move")
        print(f"All valid moves: {self.board.all_valid_moves(color)}")

        n = self.strategy.run_strategy(color)
        if n is None:
            print(f"No valid moves for bot as {color}")
            return None
        x,y = n
        print(f"Moved to {n}")
        self.board.update(x, y, color)


if __name__ == "__main__":
    strategy = MinMax()
    b = Bot()
    b(strategy)
