import logging
import random
import time

import matplotlib.pyplot as plt

from src.algorithm.minmax import MinMax
from src.board import Board
from src.player import Player

logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
    board = Board()
    board.print_state()
    mm = MinMax()
    player = random.choice([p for p in Player])
    start = time.time()
    moves = {Player.A: [], Player.B: []}
    depth = 6
    while not board.no_more_moves():

        if player is Player.A:
            logging.info(f'Now moving: player{player}')
            am, board = mm.run(board, depth, True, player)
            board.print_state()
            if not am:
                player = player.next()
            moves[player].append(MinMax.moves_count)
        logging.info(MinMax.moves_count)
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
