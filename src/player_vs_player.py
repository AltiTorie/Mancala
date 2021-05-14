import logging
import random
import time

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
    start = time.time()
    while not board.no_more_moves():
        logging.info(f'Now moving: player{player}')
        pit = int(input('Choose pit: '))
        am = int(board.spread_beans(pit, player))
        if not am:
            player = player.next()
    board.clean_board()
    board.print_state()

    logging.info(f"The winner is player{board.log_winner()}")
    logging.info(f"The game took: {time.time() - start}")
