import logging
from functools import lru_cache

from src.board import Board
from src.evaluator import Evaluator
from src.player import Player


class MinMax:
    moves_count: int = 0

    def __init__(self):
        self.moves = []

    @lru_cache()
    def run(self, state: Board, depth, is_max, player):
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
        moves = self.calculate_possible_states(state, player)
        MinMax.moves_count += len(moves)
        if is_max:
            value = -float('inf')
            for add_move, move in moves:
                if add_move:
                    _, deep_state = self.run(move, depth - 1, True, player)
                else:
                    _, deep_state = self.run(move, depth - 1, False, player.next())
                if new_value := Evaluator.rate_board_state(deep_state, player) > value:
                    additional_move, value, best_board = add_move, new_value, move
            return additional_move, best_board
        else:
            value = float('inf')
            for add_move, move in moves:
                if add_move:
                    _, deep_state = self.run(move, depth - 1, False, player)
                else:
                    _, deep_state = self.run(move, depth - 1, True, player.next())
                if new_value := Evaluator.rate_board_state(deep_state, player) < value:
                    additional_move, value, best_board = add_move, new_value, move
            return additional_move, best_board

    @staticmethod
    def calculate_possible_states(state: Board, player: Player):
        """
        Find all possible moves for current `state` and `player`

        :param state: State for which next moves will be calculated
        :param player: Player whose moves will be calculated
        :return: All possible moves for given player
        """
        cp: Board = state.deep_copy()
        cp.print_after_move = False
        moves = []
        if player is Player.A:
            for i, pit in enumerate(cp.pits[:cp.playerA_pit_index]):
                next_move: Board = cp.deep_copy()
                if pit > 0:
                    am = next_move.spread_beans(i, player)
                    moves.append((am, next_move))
        else:
            for i, pit in enumerate(cp.pits[cp.playerA_pit_index + 1:cp.playerB_pit_index]):
                next_move = cp.deep_copy()
                if pit > 0:
                    am = next_move.spread_beans(i + cp.playerA_pit_index + 1, player)
                    moves.append((am, next_move))
        return moves
