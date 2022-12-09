from ticTacToe import TicTacToe
from mct import MonteCarloTree
import random as rd
import numpy as np

rd.seed(2)

def select_action_mct(game, mct, n_playouts):
        # Train
        for _ in range(n_playouts):
            mct.playout(game)

        # Select move
        return mct.choose(game)


def select_action_random(game):
    return rd.choice(game.get_all_next_states())

def simulate_game(n_playouts):
    game = TicTacToe(game_state=(' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' '))
    mct = MonteCarloTree()

    # game.print()

    while not game.get_winner():
        if game.get_active_player() == 'X':
            game = select_action_random(game)
        elif game.get_active_player() == 'O':
            game = select_action_mct(game, mct, n_playouts)

        # game.print()
    
    return game.get_winner()


if __name__ == "__main__":
    O_wins = 0
    X_wins = 0
    Draws = 0

    for i in range(50):
        print(str(i) + " games played")
        winner = simulate_game(1000)
        if winner == 'O':
            O_wins += 1
        elif winner == 'X':
            X_wins += 1
        elif winner == 'Draw':
            Draws += 1
    
    print("O won " + str(O_wins) + " times")
    print("X won " + str(X_wins) + " times")
    print(str(Draws) + " Draws")