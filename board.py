from typing import List, Set

DIRECTIONS = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,-1),(-1,1)]
BOARD_SIZE = 8

class Board:
    def __init__(self):
        board = [['_']*8 for _ in range(8)]
        board[3][3] = board[4][4] = 'w'
        board[4][3] = board[3][4] = 'b'
        self.board = board

    def __str__(self):
        s = []
        for row in self.board:
            s.append('|')
            for item in row:
                s.append(f"{item}|")
            s.append('\n')
        s.append('\n')
        return ''.join(s)

    
    def get_same_colored_piece_locations(self, x: int, y: int, color: str) -> List[tuple]:

        def _search_direction(dx, dy, opposite_pieces: list) -> None:
            # search for first occurence of same color in a specific direction
            # start at 1 because current board color will be null ("_")
            for i in range(1, 8):
                x_, y_ = x + i * dx, y + i * dy
                boundary = (0 <= x_ < 8 and 0 <= y_ < 8)
                if not boundary:
                    return

                cur_color = self.board[x_][y_]
                if (cur_color == "_"):
                    return
                if (cur_color == color):
                    # if not directly adjacent pieces
                    if i != 1:
                        opposite_pieces.append((x_, y_))
                    return

        if self.board[x][y] != "_":
            return []

        opposite_pieces = []
        for dx,dy in DIRECTIONS:
            _search_direction(dx, dy, opposite_pieces)

        return opposite_pieces


    def update(self, x:int, y:int, color:str) -> None:
        """updates a board based on moved position"""

        for dx,dy in DIRECTIONS:

            # search for first occurence of opposite color:
            for i in range(1,8):
                x_, y_ = x + i * dx, y + i * dy
                boundary = (0 <= x_ < 8 and 0 <= y_ < 8)
                if not boundary:
                    break

                cur_color = self.board[x_][y_]
                if (cur_color == "_"):
                    break
                if (cur_color == color):
                    for j in range(i):
                        self.board[x + j * dx][y + j * dy] = color
                    break

    def all_valid_moves(self, color) -> Set[tuple]:
        return {(x,y) for x in range(8) for y in range(8) if self.is_valid_move(x,y,color)}
        
    def is_valid_move(self, x:int, y:int, color: str) -> bool:
        if self.board[x][y] != "_":
            return False
        for dx,dy in DIRECTIONS:
            # search for first occurence of opposite color in each direction
            # start at 1 because current board color is null
            for i in range(1, 8):
                x_, y_ = x + i * dx, y + i * dy
                boundary = (0 <= x_ < 8 and 0 <= y_ < 8)
                if not boundary:
                    break

                # at the start, cur_color will always be _
                cur_color = self.board[x_][y_]
                if (cur_color == "_"):
                    break
                if (cur_color == color):
                    if i == 1:
                        break
                    return True
        return False

    def is_full(self) -> bool:
        return all(i in {'b', 'w'} for row in self.board for i in row)

    def calculate_score(self):
        d = {'b': 0, 'w': 0, '_': 0}
        for row in self.board:
            for i in row:
                d[i] += 1
        return d


