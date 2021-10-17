from typing import List, Set, Dict

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
        col_nums = list(map(str, (range(8))))
        s.append( ' '*3 + ' '.join(col_nums) + '\n')
        for idx, row in enumerate(self.board):
            s.append(f'{idx} |')
            for item in row:
                s.append(f"{item}|")
            s.append('\n')
        s.append('\n')
        return ''.join(s)

    
    def get_same_colored_piece_locations(self, x: int, y: int, color: str) -> List[tuple]:
        """ Get the coordinates of all same-colored chips which are horizontally, vertically, or diagonally
        can see each other (x,y)"""

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

        def _normalize(diff):
            return abs(diff)//diff if diff else 0

        piece_locs = self.get_same_colored_piece_locations(x, y, color)
        for Px, Py in piece_locs:
            dx = _normalize(Px - x)
            dy = _normalize(Py - y)
            steps = max(abs(Px-x), abs(Py-y))

            for i in range(steps):
                self.board[x + i * dx][y + i * dy] = color


    def all_valid_moves(self, color) -> Set[tuple]:
        return {(x,y) for x in range(8) for y in range(8) if self.is_valid_move(x,y,color)}
        
    def is_valid_move(self, x:int, y:int, color: str) -> bool:
        piece_locs = self.get_same_colored_piece_locations(x, y, color)
        return True if len(piece_locs) else False
        
    def is_full(self) -> bool:
        return all(i in {'b', 'w'} for row in self.board for i in row)

    def calculate_score(self) -> Dict[str, int]:
        d = {'b': 0, 'w': 0, '_': 0}
        for row in self.board:
            for i in row:
                d[i] += 1
        return d


