from abc import ABC

from src.board import Board
from src.player import Player


class Algorithm(ABC):
    moves_count = 0

    def run(self, state: Board, depth: int, is_max: bool, player: Player):
        raise NotImplementedError("Cannot call method from abstract class")
