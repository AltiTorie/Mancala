from functools import lru_cache

from src.algorithm.algorithm import Algorithm
from src.board import Board
from src.evaluator import Evaluator
from src.player import Player


class MinMax(Algorithm):
    moves_count: int = 0

    @lru_cache()
    def run(self, state: Board, depth: int, is_max: bool, player: Player):
        """
        Get next best or worst state for given state depending on specified parameters.

        :param state: Board state from which algorithm will start looking for best/worst move.
        :param depth: Maximum depth that will be visited.
        :param is_max: Whether MinMax should maximize the outcome or minimize it.
        :param player: Player whose "turn" is currently.
        :return: Tuple containing information whether next move gives additional move and next move itself.
        """
        if depth == 0 or state.no_more_moves():
            return False, state
        additional_move = False
        best_board = state
        moves = state.calculate_possible_states(player)
        self.moves_count += len(moves)
        if is_max:
            value = -float('inf')
            for add_move, move in moves:
                if add_move:
                    _, deep_state = self.run(move, depth - 1, True, player)
                else:
                    _, deep_state = self.run(move, depth - 1, False, player.next())
                new_value = Evaluator.rate_board_state(deep_state, player)
                if new_value > value:
                    additional_move, value, best_board = add_move, new_value, move
            return additional_move, best_board
        else:
            value = float('inf')
            for add_move, move in moves:
                if add_move:
                    _, deep_state = self.run(move, depth - 1, False, player)
                else:
                    _, deep_state = self.run(move, depth - 1, True, player.next())
                new_value = Evaluator.rate_board_state(deep_state, player)
                if new_value < value:
                    additional_move, value, best_board = add_move, new_value, move
            return additional_move, best_board
