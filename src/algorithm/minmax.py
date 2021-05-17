from functools import lru_cache

from src.algorithm.algorithm import Algorithm
from src.board import Board
from src.evaluation.evaluator import Evaluator
from src.player import Player


class MinMax(Algorithm):
    moves_count: int = 0

    def __init__(self, evaluator: Evaluator):
        self.__player = None
        self.evaluator = evaluator

    def run(self, state: Board, depth: int, is_max: bool, player: Player):
        """
        Get next best or worst state for given state based on specified parameters.

        :param state: Board state from which algorithm will start looking for best/worst move.
        :param depth: Maximum depth that will be visited.
        :param is_max: Whether MinMax should maximize the outcome or minimize it.
        :param player: Player whose "turn" is currently.
        :return: Tuple containing information whether next move gives additional move and next move itself.
        """
        self.__player = player
        _, additional_move, board = self.__calculate(state, depth, is_max, player)
        return additional_move, board

    @lru_cache()
    def __calculate(self, state: Board, depth: int, is_max: bool, player: Player):
        """
        Helper function to get next best or worst state for given state based on specified parameters.

        :param state: Board state from which algorithm will start looking for best/worst move.
        :param depth: Maximum depth that will be visited.
        :param is_max: Whether MinMax should maximize the outcome or minimize it.
        :param player: Player whose "turn" is currently.
        :return: Tuple containing information whether next move gives additional move and next move itself.
        """
        if depth == 0 or state.no_more_moves():
            return self.evaluator.rate_board_state(state, self.__player), False, state
        additional_move = False
        best_board = state
        moves = state.calculate_possible_states(player)
        self.moves_count += len(moves)
        if is_max:
            value = -float('inf')
            for add_move, move in moves:
                if add_move:
                    new_value, _, _ = self.__calculate(move, depth - 1, True, player)
                else:
                    new_value, _, _ = self.__calculate(move, depth - 1, False, player.next())
                if new_value > value:
                    additional_move, value, best_board = add_move, new_value, move
            return value, additional_move, best_board
        else:
            value = float('inf')
            for add_move, move in moves:
                if add_move:
                    new_value, _, _ = self.__calculate(move, depth - 1, False, player)
                else:
                    new_value, _, _ = self.__calculate(move, depth - 1, True, player.next())
                if new_value < value:
                    additional_move, value, best_board = add_move, new_value, move
            return value, additional_move, best_board
