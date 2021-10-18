import random
from typing import Tuple
from math import inf

class Random:
    """ Most simple bot. Randomly picks move """
    def __init__(self):
        pass

    def __call__(self, board):
        self.board = board

    def run_strategy(self, color) -> Tuple[int, int]:
        return self.random_move(color)

    def random_move(self, color) -> Tuple[int,int]:
        # maybe Optional[tuple]
        s = list(self.board.all_valid_moves(color))
        return random.choice(s) if len(s) else None


class MinMax:
    """ Mini Max Algorithm bot. Will recursively search over game decision
    tree for best possible move, while accounting for opponent's reactions."""
    def __init__(self, depth=7):
        self.depth = depth

    def __call__(self, board):
        self.board = board

    def run_strategy(self, color: str) -> Tuple[int,int]:
        return self.mini_max(color, self.depth)[1]

    def mini_max(self, color: str, depth: int) -> Tuple[float, Tuple[int,int]]:
        """ At black, maximize value. As white, minimize value """
        if depth == 0 or self.board.no_valid_moves(color):
            return (self.board.evaluate_position(), None)

        if color == 'b':
            agg_fxn, ans, opposite = max, (-inf, None), 'w'
        else:
            agg_fxn, ans, opposite = min, (inf, None), 'b'
        
        for x,y in self.board.all_valid_moves(color):
            piece_locs = self.board.get_same_colored_piece_locations(x,y,color)
            self.board.update(x,y,color)
            val, _ = self.mini_max(opposite, depth-1)
            ans = agg_fxn(ans, (val, (x,y)))
            self.board.undo(x,y,color,piece_locs)
        return ans


class AlphaBetaMinMax:
    """ Utilizes Alpha Beta pruning to speed up the Min Max Algorithm.
    Takes around 8x faster to decide bot's move, and can process higher depths more quickly. """
    def __init__(self, depth=7):
        self.depth = depth

    def __call__(self, board):
        self.board = board

    def run_strategy(self, color: str) -> Tuple[int,int]:
        return self.ab_mini_max(color, self.depth, -inf, inf)[1]

    def ab_mini_max(self, color: str, depth: int, 
                    alpha: int, beta: int) -> Tuple[float, Tuple[int,int]]:
        """ At black, maximize value. As white, minimize value """
        if depth == 0 or self.board.no_valid_moves(color):
            return (self.board.evaluate_position(), None)

        if color == 'b':
            agg_fxn, ans, opposite = max, (-inf, None), 'w'
        else:
            agg_fxn, ans, opposite = min, (inf, None), 'b'
        
        for x,y in self.board.all_valid_moves(color):
            piece_locs = self.board.get_same_colored_piece_locations(x,y,color)
            self.board.update(x,y,color)
            val, _ = self.ab_mini_max(opposite, depth-1, alpha, beta)
            ans = agg_fxn(ans, (val, (x,y)))
            self.board.undo(x,y,color,piece_locs)

            if color == 'b':
                alpha = max(alpha, val)
            else:
                beta = min(beta, val)
            if beta <= alpha:
                break
        return ans