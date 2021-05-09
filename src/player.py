from enum import Enum


class Player(Enum):
    A = 1
    B = 2

    def next(self):
        """
        Get next player.

        :return: Next player type.
        """
        if self is Player.A:
            return Player.B
        else:
            return Player.A

    def __str__(self):
        return self.name
