#!/usr/bin/python3
import sys, time
from typing import List, Set
import random
    
# incorporate enums, typing, class, __str__
# separate python file for bot, separate class for game with Bot
DIRECTIONS = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,-1),(-1,1)]

def print_board(board: List[List[str]]):
    for row in board:
        for item in row:
            print(item, end="|")
        print()
    print()

def random_move(board, color) -> tuple:
    # maybe Optional[tuple]
    s = all_valid_moves(board, color)
    return random.choice(s) if len(s) else None

def change(board,x:int,y:int,cur_color:str) -> None:
    """changes a board based on moved position"""

    for dx,dy in DIRECTIONS:

        # search for first occurence of opposite color:
        for i in range(8):
            x_, y_ = x + i * dx, y + i * dy
            boundary = 0 <= x_ < 8 and 0 <= y_ < 8
            if not boundary:
                break
            color = board[x_][y_]
            no_color = color != "_"
            if no_color:
                break

            same_color = (color == cur_color)
            # opposite_color = (color != cur_color)

            if same_color:
                for j in range(1,i):
                    board[x + j * dx][y + j * dy] = cur_color
                break
           
def naive_mini_max(board):
    """ mini max that foreshadows next move by points """
    pass

#mini max that foreshadows next n moves
def mini_max(board, n):
    pass

def all_valid_moves(board, color) -> Set[tuple]:
    return {(x,y) for x in range(8) for y in range(8) if is_valid_move(board,x,y,color)}

def is_valid_move(board, x:int, y:int, color: str) -> bool:
    if board[x][y] in {'b', 'w'}:
        return False

    for dx,dy in DIRECTIONS:
        # search for first occurence of opposite color in each direction
        for i in range(8):
            x_, y_ = x + i * dx, y + i * dy
            boundary = 0 <= x_ < 8 and 0 <= y_ < 8
            if not boundary:
                break

            cur_color = board[x_][y_]
            no_color = cur_color != "_"
            if no_color:
                break

            same_color = (color == cur_color)
            if same_color:
                return True
    return False


def is_full(board) -> bool:
    return all(i in {'b', 'w'} for row in board for i in row)

#othello takes a string of 64 characters, b -> black, w -> white
#index 0 to 63, from top left to bottom right
def othello(board):
    while True:
        s = input("Want to go first? [Y/n]")
        if s.lower() not in {'y', 'n'}:
            print("Try again")
        else:
            break

    turn = 0
    user_color = "b" if s.lower() == 'y' else 'w'
    bot_color = "w" if user_color == 'b' else 'b'

    # turn = 0 is user turn
    while not is_full(board) or (no_valid_moves(board, 'b') and no_valid_move(board, 'w')):
        if turn == 0:
            user_turn(board, user_color)
            turn = 1
        else:
            bot_turn(board, bot_color)
            turn = 0
        print_board(board)


def get_valid_user_coordinate_input(valid_moves):
    while True:
        print('yolo', flush=True)
        d = {
            'x': input("x coordinate (0 to 7)"),
            'y': input("y coordinate (0 to 7)")
        }

        if all(d[k].isdigit() and 0 <= int(d[k]) < 8 for k in d):
            if (d['x'], d['y']) in all_valid_moves:
                return tuple(d.values())
            else:
                print(f"({d['x'], d['y']}) is not a valid move")

        for k in d:
            if not (d[k].isdigit() and 0 <= int(d[k]) < 8):
                print(f"{k} value of {d[k]} is not integer between 0 and 7")
        

def user_turn(board, color):
    s = all_valid_moves(board, color)
    if not s:
        return None

    x,y = get_valid_user_coordinate_input(s)
    change(board, x, y, color)


def bot_turn(board, color):
    n = random_move(board, color)
    if n is None:
        return None
    x,y = n
    change(board, x, y, color)

#day 1: implement change + random_move
#day 2: implement naive mini max
#day 3: implement mini max


if __name__ == "__main__":
    board = [['_']*8 for _ in range(8)]
    board[3][3] = board[4][4] = 'w'
    board[4][3] = board[3][4] = 'b'
    othello(board)
