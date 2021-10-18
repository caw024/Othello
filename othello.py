from typing import Tuple
from bot import Bot
from board import Board
from strategy import Random, MinMax, AlphaBetaMinMax
    

class Othello:
    """ Main class to run and start Othello game between users and/or bot"""
    def __init__(self, board_size=8, bot=None):
        self.board = Board(size=board_size)
       
        self.bot = bot
        if self.bot:
            # calls the bot with a board instance
            self.bot(self.board)
    
    def get_user_coordinate_choice(self, valid_moves: set) -> Tuple[int,int]:
        def _check_valid_inputs(d: dict) -> bool:
            if not all(d[k].isdigit() and 0 <= int(d[k]) < self.board.size for k in d):
                print("Invalid return type, try again")
                return False
            coor = tuple(map(int, d.values()))
            if coor not in valid_moves:
                print(f"({coor}) is not a valid move")
                return False
            else:
                return True

        while True:
            d = {
                'x': input(f"Integer row x (from 0 to {self.board.size-1}): "),
                'y': input(f"Integer row y (from 0 to {self.board.size-1}): ")
            }
            if not _check_valid_inputs(d):
                continue
            coor = tuple(map(int, d.values()))
            return coor


    def user_turn(self, color: str) -> None:
        valid_moves = self.board.all_valid_moves(color)
        if not valid_moves:
            print(f"No valid moves for user as {color}")
            return None
        print(f"Valid moves as {color}: {valid_moves}")
        x,y = self.get_user_coordinate_choice(valid_moves)
        print("-"*30)
        print("User move:")
        print(f"Moved to ({x}, {y})")
        self.board.update(x, y, color)


    def start_game(self) -> None:
        def _determine_color() -> tuple:
            while True:
                user_resp = input("Want to go first? [Y/n]").lower()
                if user_resp in {'y', 'n'}:
                    break
                print("Try again")      
            print()
            return ('b', 'w') if user_resp == 'y' else ('w', 'b')

        # black always moves first in Othello
        user_color, bot_color = _determine_color()
        self.game_loop(user_color, bot_color)

        eval = self.board.evaluate_position()

        if (eval > 0 and user_color == 'b') or (eval < 0 and user_color == 'w'):
            winner_str = "User wins"
        elif eval == 0:
            winner_str = "Tie"
        else:
            winner_str = "Bot wins"
        print(winner_str)


    def game_loop(self, user_color: str, bot_color: str) -> None:
        cur_color = 'b'
        while not self.board.is_full():
            print(self.board)
            print()
            scores = self.board.get_scores()
            print(f'User: {scores[user_color]}, Bot: {scores[bot_color]}')

            has_valid_move = any(self.board.all_valid_moves(col) for col in 'bw')
            if not has_valid_move:
                break
            if cur_color == user_color:
                self.user_turn(user_color)
            else:
                self.bot.bot_turn(bot_color) if self.bot else self.user_turn(bot_color)
            
            cur_color = 'b' if cur_color == 'w' else 'w'


if __name__ == "__main__":
    # initializes bot with strategy, and Othello game with the bot
    bot = Bot(strategy=AlphaBetaMinMax)
    board_size = 8
    o = Othello(board_size=board_size, bot=bot)
    o.start_game()
