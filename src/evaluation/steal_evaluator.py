from src.board import Board
from src.evaluation.evaluator import Evaluator
from src.player import Player


def calculate_max_stolen_beans(board, player):
    l, h = board.get_players_pits_indexes(player)
    max_beans = 0
    for i in range(l, h):
        v = board.pits[i]
        is_zero = v == 0
        last_pos = (i + v) % board.pits_len
        was_zero = board.pits[last_pos] == 0
        opposite = board.pits[board.opposite_pit_index(last_pos)]
        if not is_zero and was_zero and board.can_steal(i, last_pos):
            max_beans = max(max_beans, opposite + 1)
    return max_beans


class StealEvaluator(Evaluator):

    @staticmethod
    def rate_board_state(board: Board, player: Player):
        """
        Rate board state based empty beans opposite to empty pits.
        Otherwise return his store beans count.

        :param board: Current state of the Board to be rated.
        :param player: Player whose beans will be counted.
        :return: Number of beans in the given player pit.
        """
        b: Board = board.deep_copy()

        player_beans = calculate_max_stolen_beans(b, player)
        # enemy_beans = calculate_max_stolen_beans(b, player.next())

        return player_beans