#!/usr/bin/python3
import sys, time
from bot import Bot
from board import Board
    
# incorporate enums, typing, class, __str__
# separate python file for bot, separate class for game with Bot

class Othello:
    def __init__(self, bot=None):
        self.bot = bot
        self.board = Board()
    
    def get_user_coordinate_choice(self, valid_moves: set) -> tuple:
        def _check_valid_inputs(d) -> bool:
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
                'x': input("integer x (from 0 to 7): "),
                'y': input("integer y (from 0 to 7): ")
            }
            if not _check_valid_inputs(d):
                continue
            coor = tuple(map(int, d.values()))
            return coor


    def user_turn(self, color):
        valid_moves = self.board.all_valid_moves(color)
        if not valid_moves:
            return None
        print(f"Valid moves as {color}: {valid_moves}")
        x,y = self.get_user_coordinate_choice(valid_moves)
        print("\nUser move:")
        self.board.update(x, y, color)


    def start_game(self):
        def _determine_color():
            while True:
                user_resp = input("Want to go first? [Y/n]").lower()
                if user_resp in {'y', 'n'}:
                    break
                print("Try again")      
            return ('b', 'w') if user_resp == 'y' else ('w', 'b')
        
        # black always moves first in Othello
        cur_color = 'b'
        user_color, bot_color = _determine_color()
        
        while not self.board.is_full():# or (no_valid_moves(board, 'b') and no_valid_move(board, 'w')):
            print(self.board)

            has_valid_move = any(self.board.all_valid_moves(col) for col in 'bw')
            if not has_valid_move:
                break
            if cur_color == user_color:
                self.user_turn(user_color)
            else:
                self.bot.bot_turn(self.board, bot_color) if self.bot else self.user_turn(bot_color)
            
            cur_color = 'b' if cur_color == 'w' else 'w'

        d = self.board.calculate_score()
        winner_str = "User wins" if d[user_color] > d[bot_color] else "Bot wins"
        print("\n" + winner_str)



#day 1: implement change + random_move
#day 2: implement naive mini max
#day 3: implement mini max


if __name__ == "__main__":
    o = Othello()#bot=Bot())
    o.start_game()
