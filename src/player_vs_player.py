import logging
import random
import time

from src.board import Board
from src.player import Player

logging.basicConfig(level=logging.INFO)
if __name__ == '__main__':
    board = Board()
    board.print_state()
    player = random.choice([p for p in Player])
    start = time.time()
    while not board.no_more_moves():
        logging.info(f'Now moving: player{player}')
        pit = int(input('Choose pit: '))
        am = int(board.spread_beans(pit, player))
        if not am:
            player = player.next()
    board.clean_board()
    board.print_state()

    logging.info(f"The winner is player{board.winner()}")
    logging.info(f"The game took: {time.time() - start}")
