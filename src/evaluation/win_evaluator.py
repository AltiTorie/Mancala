from src.board import Board
from src.evaluation.evaluator import Evaluator
from src.player import Player


class WinEvaluator(Evaluator):

    @staticmethod
    def rate_board_state(board: Board, player: Player):
        """
        Rate board state based on condition whether given player is a winner.
        Otherwise return his store beans count.

        :param board: Current state of the Board to be rated.
        :param player: Player whose beans will be counted.
        :return: Number of beans in the given player pit.
        """
        b: Board = board.deep_copy()
        if b.no_more_moves():
            b.clean_board()
            return (b.get_winner() is player) * 1000
        else:
            if player is Player.A:
                return b.get_state()[b.playerA_pit_index]
            else:
                return b.get_state()[b.playerB_pit_index]
