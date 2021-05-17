import logging
import random
import time

import matplotlib.pyplot as plt

from src.algorithm.alphabeta import AlphaBeta
from src.algorithm.minmax import MinMax
from src.board import Board
from src.evaluation.store_evaluator import StoreEvaluator
from src.player import Player

logging.basicConfig(level=logging.INFO)


def show_plt_for(x, y, xlabel, ylabel, save_file, title, save=False, show=True):
    colors = {AlphaBeta: 'red', MinMax: 'blue'}
    for alg in algorithms:
        plt.plot(x, y[type(alg)], color=colors[type(alg)],
                 label=alg.__class__.__name__)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.legend()
    if save:
        plt.savefig(save_file)
    if show:
        plt.show()
    plt.close()


if __name__ == '__main__':
    # Values for configuration:
    depth = 9
    beans_per_pit = 4
    first_move_random = True
    how_many_times = 10

    evaluators = [StoreEvaluator()]  # TODO: Add for loop for different evaluators
    algorithms = [AlphaBeta(evaluators[0]), MinMax(evaluators[0])]
    depths = [i for i in range(1, depth)]
    all_winner_moves = {AlphaBeta: [], MinMax: []}
    all_visited_states = {AlphaBeta: [], MinMax: []}
    times = {AlphaBeta: [], MinMax: []}
    for depth in depths:
        for algorithm in algorithms:
            logging.info(f"[RUN] -Now running {algorithm.__class__.__name__} at depth {depth}")
            avg_time = 0
            avg_moves = 0
            avg_visited_nodes = 0
            for i in range(how_many_times):
                logging.info(f"[RUN] --{i}")
                start = time.time()
                board = Board(beans_per_pit=beans_per_pit)
                player = random.choice([p for p in Player])

                player_moves = {Player.A: 0, Player.B: 0}
                visited_states = {Player.A: [], Player.B: []}

                # first move random
                if first_move_random:
                    am, board = random.choice(board.calculate_possible_states(player))
                    player_moves[player] += 1
                    logging.debug(f'Now moving: player{player}')
                    if not am:
                        player = player.next()

                while not board.no_more_moves():
                    logging.debug(f'Now moving: player{player}')
                    am, board = algorithm.run(board, depth, True, player)
                    player_moves[player] += 1
                    if not am:
                        player = player.next()
                    visited_states[player].append(algorithm.moves_count)
                    algorithm.moves_count = 0
                    # if time.time() - start > 500:
                    #     break

                board.clean_board()
                logging.info(f"[RUN] --The game took: {time.time() - start}")
                logging.debug(f'a_moves: {visited_states[Player.A]}')
                logging.debug(f'b_moves: {visited_states[Player.B]}')

                avg_time += time.time() - start

                winner = board.get_winner()
                if winner:
                    avg_moves += player_moves[winner]
                else:
                    avg = (player_moves[Player.A] + player_moves[Player.B]) / 2
                    avg_moves += avg
                    # all_winner_moves[type(algorithm)].append(avg)

                avg_visited_states = (sum(visited_states[Player.A]) + sum(visited_states[Player.B])) / (
                    len((visited_states[Player.A]) + (visited_states[Player.B])))
                avg_visited_nodes += avg_visited_states

            times[type(algorithm)].append(avg_time / how_many_times)
            all_winner_moves[type(algorithm)].append(avg_moves / how_many_times)
            all_visited_states[type(algorithm)].append(avg_visited_nodes / how_many_times)

            # plt.show()
            # plt.savefig(f'charts/{algorithm.__class__.__name__}_{depth}')
            # plt.close()

    # _AlphaBeta = sum([19.126529216766357,
    #                   4.530384540557861,
    #                   19.723633766174316,
    #                   20.59429430961609,
    #                   15.665140628814697,
    #                   20.264402151107788,
    #                   5.149595022201538,
    #                   14.809540748596191,
    #                   21.368651390075684,
    #                   5.478537321090698]) / 10
    # _MinMax = sum([176.10888624191284,
    #                180.5201985836029,
    #                182.27369856834412,
    #                186.54761052131653,
    #                182.63640761375427,
    #                190.21075248718262,
    #                106.75149655342102,
    #                107.70297908782959,
    #                139.1371922492981,
    #                123.15704870223999]) / 10
    # times[AlphaBeta].append(_AlphaBeta)
    # times[MinMax].append(_MinMax)
    show_plt_for(x=depths,
                 y=times,
                 xlabel='',
                 ylabel='',
                 title='Times',
                 save_file='charts/avg_times',
                 save=True,
                 show=True)
    show_plt_for(x=depths,
                 y=all_visited_states,
                 xlabel='',
                 ylabel='',
                 title='Visited states',
                 save_file='charts/visited_states',
                 save=True,
                 show=True)
    show_plt_for(x=depths,
                 y=all_winner_moves,
                 xlabel='',
                 ylabel='',
                 title='Winner moves',
                 save_file='charts/winner_moves',
                 save=True,
                 show=True)

    logging.info(times)
    logging.info(all_visited_states)
    logging.info(all_winner_moves)
