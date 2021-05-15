from functools import lru_cache

from src.algorithm.algorithm import Algorithm
from src.board import Board
from src.evaluator import Evaluator
from src.player import Player


class AlphaBeta(Algorithm):
    moves_count: int = 0

    def __init__(self):
        self.__player = None

    def run(self, state: Board, depth: int, is_max: bool, player: Player):
        """
        Get next best or worst state for given state depending on specified parameters.

        :param state: Board state from which algorithm will start looking for best/worst move.
        :param depth: Maximum depth that will be visited.
        :param is_max: Whether AlphaBeta should maximize the outcome or minimize it.
        :param player: Player whose "turn" is currently.
        :return: Tuple containing information whether next move gives additional move and next move itself.
        """
        self.__player = player
        if is_max:
            _, additional_move, board = self.__max_value(state, None, None, depth, player)
        else:
            _, additional_move, board = self.__min_value(state, None, None, depth, player)
        self.__player = None
        return additional_move, board

    @lru_cache
    def __max_value(self, state: Board, alpha: int, beta: int, depth: int, player: Player):
        """
        Get next best state for given state based on specified parameters.

        :param state: Board state from which algorithm will start looking for best/worst move.
        :param depth: Maximum tree depth that will be visited.
        :param player: Player for whom moves will be calculated.
        :return: Tuple containing information whether next move gives additional move and next move itself.
        """
        if depth == 0 or state.no_more_moves():
            return Evaluator.rate_board_state(state, self.__player), False, state
        value = float('-inf')
        moves = state.calculate_possible_states(player)
        self.moves_count += len(moves)
        outer_additional_move = None
        outer_state = None
        for additional_move, move in moves:
            if additional_move:
                v_prime, _, _ = self.__max_value(move, alpha, beta, depth - 1, player)
            else:
                v_prime, _, _ = self.__min_value(move, alpha, beta, depth - 1, player.next())
            if v_prime > value:
                value = v_prime
                outer_additional_move = additional_move
                outer_state = move
            if beta is not None and v_prime >= beta:
                return value, outer_additional_move, outer_state
            if alpha is None or v_prime > alpha:
                alpha = v_prime
        return value, outer_additional_move, outer_state

    @lru_cache
    def __min_value(self, state: Board, alpha: int, beta: int, depth: int, player: Player):
        """
        Get next worst state for given state based on specified parameters.

        :param state: Board state from which algorithm will start looking for best/worst move.
        :param depth: Maximum tree depth that will be visited.
        :param player: Player for whom moves will be calculated.
        :return: Tuple containing information whether next move gives additional move and next move itself.
        """
        if depth == 0 or state.no_more_moves():
            return Evaluator.rate_board_state(state, self.__player), False, state
        value = float('inf')
        moves = state.calculate_possible_states(player)
        self.moves_count += len(moves)
        outer_additional_move = False
        outer_state = state
        for additional_move, move in moves:
            if additional_move:
                v_prime, _, _ = self.__min_value(move, alpha, beta, depth - 1, player)
            else:
                v_prime, _, _ = self.__max_value(move, alpha, beta, depth - 1, player.next())
            if v_prime < value:
                value = v_prime
                outer_additional_move = additional_move
                outer_state = move
            if alpha is not None and v_prime <= alpha:
                return value, outer_additional_move, outer_state
            if beta is None or v_prime < beta:
                beta = v_prime
        return value, outer_additional_move, outer_state
