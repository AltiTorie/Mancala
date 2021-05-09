from src.board import Board
from src.player import Player


class Evaluator:

    @staticmethod
    def rate_board_state(board: Board, player: Player):
        """
        Rates board state based on how many beans there are in given players pit.

        :param board: Current state of the Board to be rated.
        :param player: Player whose beans will be counted.
        :return: Number of beans in the given player pit.
        """
        if player is Player.A:
            return board.get_state()[board.playerA_pit_index] - board.get_state()[board.playerB_pit_index]
        else:
            return board.get_state()[board.playerB_pit_index] - board.get_state()[board.playerA_pit_index]

        # if player is Player.A:
        #     return board.get_state()[board.playerA_pit_index] - board.get_state()[board.playerB_pit_index]
        # else:
        #     return board.get_state()[board.playerB_pit_index] - board.get_state()[board.playerA_pit_index]
