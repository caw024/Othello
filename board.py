from typing import List, Set, Dict
from collections import deque

ADJACENT = [(1,0),(-1,0),(0,1),(0,-1)]
DIAGONAL = [(1,1),(1,-1),(-1,-1),(-1,1)]
DIRECTIONS = ADJACENT + DIAGONAL

class Board:
    """ Board class with several methods to modify states 
    and evaluate positions."""
    def __init__(self, size=8):
        self.size = size if size % 2 == 0 else 8
        
        board = [['_']*size for _ in range(size)]
        mid = (size - 1)//2

        board[mid][mid] = board[mid+1][mid+1] = 'w'
        board[mid+1][mid] = board[mid][mid+1] = 'b'
        self.board = board

        self.heuristic_grid_values = self.bfs_grid_values()

    def __str__(self):
        s = []
        col_nums = list(map(str, (range(self.size))))
        s.append( ' '*3 + ' '.join(col_nums) + '\n')
        for idx, row in enumerate(self.board):
            s.append(f'{idx} |')
            for item in row:
                s.append(f"{item}|")
            s.append('\n')
        s.append('\n')
        return ''.join(s)

    def bfs_grid_values(self) -> List[List[float]]:
        grid_values = [[0]*self.size for _ in range(self.size)]
        mid = (self.size - 1)//2
        visited = set()
        q = deque([])
        for x,y in [(mid,mid), (mid,mid+1), (mid+1,mid), (mid+1,mid+1)]:
            grid_values[x][y] = 1
            visited.add((x,y))
            q.append((x,y,1))

        while q:
            for _ in range(len(q)):
                x,y,dist = q.popleft()
                for dx, dy in ADJACENT:
                    x_, y_ = x+dx, y+dy
                    if not self.is_boundary_safe(x_,y_) or (x_, y_) in visited:
                        continue
                    grid_values[x_][y_] = dist
                    visited.add((x_,y_))
                    q.append((x_,y_,dist+0.5))
        return grid_values


    def is_boundary_safe(self, x, y):
        return (0 <= x < self.size and 0 <= y < self.size)
    
    def get_same_colored_piece_locations(self, x: int, y: int, color: str) -> List[tuple]:
        """ Get the coordinates of all same-colored chips which are horizontally, vertically, or diagonally
        can see each other (x,y)"""

        def _search_direction(dx, dy, opposite_pieces: list) -> None:
            # search for first occurence of same color in a specific direction
            # start at 1 because current board color will be null ("_")
            for i in range(1, self.size):
                x_, y_ = x + i * dx, y + i * dy
                if not self.is_boundary_safe(x_, y_):
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


    def normalize(self, diff):
        return abs(diff)//diff if diff else 0


    def update(self, x:int, y:int, color:str) -> None:
        """updates a board based on moved position"""
        piece_locs = self.get_same_colored_piece_locations(x, y, color)
        for Px, Py in piece_locs:
            dx = self.normalize(Px - x)
            dy = self.normalize(Py - y)
            steps = max(abs(Px-x), abs(Py-y))

            for i in range(steps):
                self.board[x + i * dx][y + i * dy] = color

    def undo(self, x, y, color, piece_locs):
        """undoes a move with same-colored piece locations"""
        opposite = 'b' if color == 'w' else 'w'
        self.board[x][y] = "_"
        for Px, Py in piece_locs:
            dx = self.normalize(Px - x)
            dy = self.normalize(Py - y)
            steps = max(abs(Px-x), abs(Py-y))
            for i in range(1, steps):
                self.board[x + i * dx][y + i * dy] = opposite

    def all_valid_moves(self, color) -> Set[tuple]:
        return {(x,y) for x in range(self.size) for y in range(self.size) if self.is_valid_move(x,y,color)}
        
    def is_valid_move(self, x:int, y:int, color: str) -> bool:
        piece_locs = self.get_same_colored_piece_locations(x, y, color)
        return True if len(piece_locs) else False
        
    def is_full(self) -> bool:
        return all(i in {'b', 'w'} for row in self.board for i in row)

    def no_valid_moves(self, color) -> bool:
        return len(self.all_valid_moves(color)) == 0

    def get_scores(self) -> Dict[str, int]:
        d = {'b': 0, 'w': 0, '_': 0}
        for row in self.board:
            for color in row:
                d[color] += 1
        return d

    def heuristic_scores(self) -> Dict[str, int]:
        """ The farther a piece is from the center, the more it's worth. 
        Score grows linearly from the center. """

        grid_values = self.heuristic_grid_values
        d = {'b': 0, 'w': 0, '_': 0}
        for x, row in enumerate(self.board):
            for y, color in enumerate(row):
                d[color] += grid_values[x][y]
        return d

    def evaluate_position(self) -> float:
        """ Returns positive number if there are more black pieces than white"""
        #d = self.get_scores()
        d = self.heuristic_scores()
        return d['b'] - d['w']