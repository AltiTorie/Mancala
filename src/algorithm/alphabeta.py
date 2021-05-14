import logging
from functools import lru_cache

from src.board import Board
from src.evaluator import Evaluator
from src.player import Player


class AlphaBeta:
    moves_count: int = 0

    def run(self, state: Board, depth: int, is_max: bool, player: Player):
        """
        Get next best or worst state for given state depending on specified parameters.

        :param state: Board state from which algorithm will start looking for best/worst move.
        :param depth: Maximum depth that will be visited.
        :param is_max: Whether AlphaBeta should maximize the outcome or minimize it.
        :param player: Player whose "turn" is currently.
        :return: Tuple containing information whether next move gives additional move and next move itself.
        """
        if is_max:
            big = 100 ** 100
            _, additional_move, board = self.max_value(state, None, None, depth, player)
            return additional_move, board

    @lru_cache
    def max_value(self, state: Board, alpha: int, beta: int, depth: int, player: Player):
        if depth == 0 or state.no_more_moves():
            return Evaluator.rate_board_state(state, player), False, state
        value = float('-inf')
        alpha_value = alpha
        beta_value = beta
        moves = state.calculate_possible_states(player)
        self.moves_count += len(moves)
        outer_additional_move = None
        outer_state = None
        for additional_move, move in moves:
            if additional_move:
                v_prime, _, next_state = self.max_value(move, alpha_value, beta_value, depth - 1, player.next())
            else:
                v_prime, _, next_state = self.min_value(move, alpha_value, beta_value, depth - 1, player)
            # v_prime = Evaluator.rate_board_state(next_state, player)
            # logging.info(f"Returned v` was: {v_prime}")
            if v_prime > value:
                value = v_prime
                outer_additional_move = additional_move
                outer_state = move
            if beta_value is not None and v_prime > beta_value:
                return value, outer_additional_move, outer_state
            if alpha_value is None or v_prime > alpha_value:
                alpha_value = v_prime
        return value, outer_additional_move, outer_state

    @lru_cache
    def min_value(self, state: Board, alpha: int, beta: int, depth: int, player: Player):
        if depth == 0 or state.no_more_moves():
            return Evaluator.rate_board_state(state, player), False, state
        value = float('inf')
        alpha_value = alpha
        beta_value = beta
        moves = state.calculate_possible_states(player)
        self.moves_count += len(moves)
        outer_additional_move = False
        outer_state = state
        for additional_move, move in moves:
            if additional_move:
                v_prime, _, next_state = self.min_value(move, alpha_value, beta_value, depth - 1, player.next())
            else:
                v_prime, _, next_state = self.max_value(move, alpha_value, beta_value, depth - 1, player)
            # logging.info(f"Returned v` was: {v_prime}")
            # v_prime = Evaluator.rate_board_state(next_state, player)
            if v_prime < value:
                value = v_prime
                outer_additional_move = additional_move
                outer_state = next_state
            if alpha_value is not None and v_prime < alpha_value:
                return value, outer_additional_move, outer_state
            if beta_value is None or v_prime < beta_value:
                beta_value = v_prime
        return value, outer_additional_move, outer_state
