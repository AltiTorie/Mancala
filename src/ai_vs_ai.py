import logging
import random
import time

import matplotlib.pyplot as plt

from src.algorithm.minmax import MinMax
from src.board import Board
from src.player import Player

logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
    # Values for configuration:
    depth = 6
    beans_per_pit = 4
    first_move_random = True
    player = random.choice([p for p in Player])
    # player = Player.A
    # player = Player.B

    board = Board(beans_per_pit=beans_per_pit)
    board.print_state()
    mm = MinMax()
    start = time.time()
    moves = {Player.A: [], Player.B: []}
    # first move random
    if first_move_random:
        am, board = random.choice(mm.calculate_possible_states(board, player))
        board.print_state()
        if not am:
            player = player.next()

    while not board.no_more_moves():
        logging.info(f'Now moving: player{player}')
        am, board = mm.run(board, depth, True, player)
        board.print_state()
        if not am:
            player = player.next()
        moves[player].append(MinMax.moves_count)
        # logging.info(MinMax.moves_count)
        MinMax.moves_count = 0
    board.clean_board()
    board.print_state()

    logging.info(f"The winner is player{board.winner()}")
    logging.info(f"The game took: {time.time() - start}")
    logging.info(f'a_moves: {moves[Player.A]}')
    logging.info(f'b_moves: {moves[Player.B]}')
    plt.plot(moves[Player.A])
    plt.plot(moves[Player.B])
    plt.show()