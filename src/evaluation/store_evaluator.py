from src.evaluation.evaluator import Evaluator
from src.player import Player


class StoreEvaluator(Evaluator):

    @staticmethod
    def rate_board_state(board, player):
        """
        Rate board state based on the amount of beans in the given players store.

        :param board: Current state of the Board to be rated.
        :param player: Player whose beans will be counted.
        :return: Number of beans in the given player pit.
        """
        b = board.deep_copy()
        if board.no_more_moves():
            b.clean_board()
        if player is Player.A:
            return b.get_state()[b.playerA_pit_index] - b.get_state()[b.playerB_pit_index]
        else:
            return b.get_state()[b.playerB_pit_index] - b.get_state()[b.playerA_pit_index]
