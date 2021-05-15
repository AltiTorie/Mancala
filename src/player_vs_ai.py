import logging
import random
import time
import matplotlib.pyplot as plt

from src.algorithm.alphabeta import AlphaBeta
from src.algorithm.minmax import MinMax
from src.board import Board
from src.player import Player

logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
    # Values for configuration:
    ###
    depth = 6
    beans_per_pit = 4
    first_move_random = True
    #
    # choose player:
    player = random.choice([p for p in Player])
    # player = Player.A
    # player = Player.B
    #
    # choose algorithm:
    algorithm = AlphaBeta()
    # algorithm = MinMax()
    ###

    board = Board(beans_per_pit=beans_per_pit)
    board.print_state()
    start = time.time()
    moves = {Player.A: [], Player.B: []}
    while not board.no_more_moves():
        time.sleep(0.4)
        if player is Player.A:
            logging.info(f'Now moving: player{player}')
            pit = int(input('Choose pit: '))
            am = int(board.spread_beans(pit, player))
            board.print_state()
            if not am:
                player = player.next()
        else:
            logging.info(f'Now moving: player{player}')
            am, board = algorithm.run(board, depth, True, Player.B)
            board.print_state()
            if not am:
                player = player.next()
            moves[player].append(algorithm.moves_count)
        logging.info(algorithm.moves_count)
        algorithm.moves_count = 0
    board.clean_board()
    board.print_state()

    logging.info(f"The winner is player{board.log_winner()}")
    logging.info(f"The game took: {time.time()-start}")
    logging.info(f'b_moves: {moves[Player.B]}')
    plt.plot(moves[Player.B])
    plt.show()
