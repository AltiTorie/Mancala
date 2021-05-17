from abc import ABC

from src.board import Board
from src.player import Player


class Evaluator(ABC):

    @staticmethod
    def rate_board_state(board: Board, player: Player):
        """
        Rate board state.

        :param board: Current state of the Board to be rated.
        :param player: Player whose beans will be counted.
        :return: Number of beans in the given player pit.
        """
        raise NotImplementedError("Cannot call function from an abstract class")
