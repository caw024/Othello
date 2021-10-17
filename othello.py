#!/usr/bin/python3
import sys, time
from typing import Tuple
from bot import Bot
from board import Board
    
# incorporate enums, typing, class, __str__

class Othello:
    def __init__(self, bot=None):
        self.board = Board()
        self.bot = bot
        if bot:
            self.bot(self.board)
    
    def get_user_coordinate_choice(self, valid_moves: set) -> Tuple[int,int]:
        def _check_valid_inputs(d: dict) -> bool:
            if not all(d[k].isdigit() and 0 <= int(d[k]) < 8 for k in d):
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
                'x': input("Integer row x (from 0 to 7): "),
                'y': input("Integer row y (from 0 to 7): ")
            }
            if not _check_valid_inputs(d):
                continue
            coor = tuple(map(int, d.values()))
            return coor


    def user_turn(self, color: str) -> None:
        valid_moves = self.board.all_valid_moves(color)
        if not valid_moves:
            print("No valid moves for user")
            return None
        print(f"Valid moves as {color}: {valid_moves}")
        x,y = self.get_user_coordinate_choice(valid_moves)
        print("-"*30)
        print("\nUser move:")
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

        d = self.board.calculate_score()
        winner_str = f"User wins ({d[user_color]})" if d[user_color] > d[bot_color] \
                        else f"Bot wins ({d[bot_color]})"
        print("\n" + winner_str)


    def game_loop(self, user_color: str, bot_color: str) -> None:
        cur_color = 'b'
        while not self.board.is_full():# or (no_valid_moves(board, 'b') and no_valid_move(board, 'w')):
            print(self.board)

            has_valid_move = any(self.board.all_valid_moves(col) for col in 'bw')
            if not has_valid_move:
                break
            if cur_color == user_color:
                self.user_turn(user_color)
            else:
                self.bot.bot_turn(bot_color) if self.bot else self.user_turn(bot_color)
            
            cur_color = 'b' if cur_color == 'w' else 'w'


if __name__ == "__main__":
    o = Othello(bot=Bot())
    o.start_game()
