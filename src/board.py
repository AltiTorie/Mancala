import logging as log
import pickle

from src.player import Player


class Board:
    def __init__(self, beans_per_pit: int = 6, print_state_after_move=True):
        """
        :param beans_per_pit: how many beans should be in each pit
        :param print_state_after_move: if this is True board state will be printed after every move
        """
        self.pits = [beans_per_pit] * ((6 + 1) * 2)
        self.pits_len = len(self.pits)
        self.playerA_pit_index = int(self.pits_len / 2) - 1
        self.playerB_pit_index = self.pits_len - 1
        self.pits[self.playerA_pit_index] = 0
        self.pits[self.playerB_pit_index] = 0
        self.print_after_move = print_state_after_move

    def __hash__(self) -> int:
        return super().__hash__()

    def get_state(self):
        """
        :return: current board state
        """
        return self.pits

    def deep_copy(self):
        return pickle.loads(pickle.dumps(self))

    def print_state(self):
        """
        Print current state of the board.

        """
        place = [str(i).center(5) for i in self.pits]
        log.info(f'+--13-+--12-+--11-+--10-+--9--+--8--+--7--+--6--+')
        log.info(f'|     |{place[12]}|{place[11]}|{place[10]}|{place[9]}|{place[8]}|{place[7]}|     |')
        log.info(f'|{place[13]}|-----+-----+-----+-----+-----+-----|{place[6]}|')
        log.info(f'|     |{place[0]}|{place[1]}|{place[2]}|{place[3]}|{place[4]}|{place[5]}|     |')
        log.info(f'+--13-+--0--+--1--+--2--+--3--+--4--+--5--+--6--+')

    def set_value(self, index: int, value: int):
        """
        Sets value of a pit at given index.

        :param index: index of pit to be updated.
        :param value: value for updated pit.
        """
        self.pits[index] = value

    def spread_beans(self, starting_pit: int, player: Player):
        """
        Spread beans from given pit to subsequent pits.

        :param player: current player
        :param starting_pit: index of pit form which beans will be spread.
        :raise ValueError: if index points to store, empty pit or chosen pit does not belong to current player
        """
        if starting_pit == self.playerA_pit_index or starting_pit == self.playerB_pit_index:
            raise ValueError("Cannot move beans from store")
        if self.pits[starting_pit] == 0:
            raise ValueError("Cannote move from empty pit")
        if player == Player.A and starting_pit >= self.playerA_pit_index:
            raise ValueError("You can only move beans from your pits")
        if player == Player.B and starting_pit <= self.playerA_pit_index:
            raise ValueError("You can only move beans from your pits")

        beans_to_spread = self.pits[starting_pit]
        self.pits[starting_pit] = 0
        pos = starting_pit + 1
        last_pos = (starting_pit + beans_to_spread) % self.pits_len
        was_zero = self.pits[last_pos] == 0
        if self.print_after_move:
            log.info(f"Moving beans: {starting_pit} -> ... -> {last_pos}")
        for index in range(pos, starting_pit + beans_to_spread + 1):
            self.pits[index % self.pits_len] += 1

        if was_zero and self.__should_steal(pos, last_pos):
            self.__steal_beans(last_pos)

        add_move = self.__additional_move(starting_pit, last_pos)

        if self.print_after_move:
            self.print_state()
        # if add_move:
        #     log.info("Player has another move!")
        return add_move

    def __should_steal(self, starting_pit, last_pit):
        """
        Detect if last bean landed on empty players pit.

        :param starting_pit: index of a pit from which started spreading
        :param last_pit: index of a pit where last bean landed
        :return: last bin on empty players pit
        """
        opposite_pit_beans = self.pits[self.__opposite_pit_index(last_pit)]
        if starting_pit < self.playerA_pit_index and last_pit % self.pits_len < self.playerA_pit_index and opposite_pit_beans > 0:
            return True
        if starting_pit > self.playerA_pit_index and last_pit % self.pits_len > self.playerA_pit_index and opposite_pit_beans > 0:
            return True
        return False

    def __steal_beans(self, from_index):
        """
        Move beans from pit at `from_index` to corresponding player store.

        :param from_index: index of a pit from beans will be moved
        """
        opposite = self.__opposite_pit_index(from_index)
        players_pit = self.__players_pit_index(from_index)
        beans = self.pits[from_index]
        self.pits[from_index] = 0
        beans += self.pits[opposite]
        # log.info(f"stealing {beans} beans from {opposite} because {from_index} ")
        self.pits[opposite] = 0
        self.pits[players_pit] += beans

    def __additional_move(self, starting_pit, last_pit):
        """
        Detects if last bean landed on players store

        :param starting_pit: index of a pit from which started spreading
        :param last_pit: index of a pit where last bean landed
        :return: last bin on players store
        """
        if starting_pit < self.playerA_pit_index and last_pit % self.pits_len == self.playerA_pit_index:
            return True
        if starting_pit > self.playerA_pit_index and last_pit % self.pits_len == self.playerB_pit_index:
            return True
        return False

    def __players_pit_index(self, index):
        """
        Find index of a players store whose pit's `index` was given.

        :return: index of a players pit that corresponds tho given `index`
        :param index: index of a pit from which players store to be found
        """
        return self.playerA_pit_index if index <= self.playerA_pit_index else self.playerB_pit_index

    def __opposite_pit_index(self, index):
        """
        :param index: index of a pit
        :return: index of an opposing pit
        """
        pit = self.__players_pit_index(index)
        return (pit + (pit - index)) % self.pits_len

    def no_more_moves(self):
        """
        :return: whether there are any legal moves
        """
        players_pits = [
            self.pits[:self.playerA_pit_index],
            self.pits[self.playerA_pit_index + 1:self.playerB_pit_index]]

        for player_pits in players_pits:
            if not any(player_pits):
                return True
        return False

    def clean_board(self):
        """
        Places every bean from "normal" pit to players store.
        Possible to use only when there are no more moves possible.
        """
        if self.no_more_moves():
            for pi in range(self.playerA_pit_index):
                # log.info(f"{self.pits[self.playerA_pit_index]} += {self.pits[pi]}")
                self.pits[self.playerA_pit_index] += self.pits[pi]
                self.pits[pi] = 0
            for pi in range(self.playerA_pit_index + 1, self.playerB_pit_index):
                # log.info(f"{self.pits[self.playerB_pit_index]} += {self.pits[pi]}")
                self.pits[self.playerB_pit_index] += self.pits[pi]
                self.pits[pi] = 0

    def winner(self):
        """
        Winner for the current state of the board
        :return: Player who has more beans in his store
        """
        if self.pits[self.playerA_pit_index] > self.pits[self.playerB_pit_index]:
            return Player.A
        return Player.B

    def calculate_possible_states(self, player: Player):
        """
        Find all possible moves for given `player`. Each `move` contains information
        whether there is an additional move for the player and the next state of the board after the move.

        :param player: Player whose moves will be calculated
        :return: List of all possible moves for given player
        """
        cp: Board = self.deep_copy()
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
