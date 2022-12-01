import numpy as np
import random as rd

class Game:
    def __init__(self):
        # Game setup
        self.players = ('X', 'O')
        self.turn_player = 'X'
        self.actions = [(x, y) for x in range(3) for y in range(3)]
        self.winner = None
        self.game_state = [[' ', ' ', ' '], 
                           [' ', ' ', ' '],
                           [' ', ' ', ' ']]

    '''
        Updates the game-state by taking an action for a player.
        Removes the action from the list of possible actions
        Action is a (x, y) tuple
    '''
    def take_action(self, action):
        # Update game
        x, y = action
        self.game_state[y][x] = self.turn_player
        self.actions.remove(action)
        self.pass_turn()

        # Check if game is over
        self.determine_winner()

    '''
        Updates the state of active player
    '''
    def pass_turn(self):
        if self.turn_player == 'X':
            self.turn_player = 'O'
        else:
            self.turn_player = 'X'

    '''
        After each action this function checks if a player has won the game
    '''
    def determine_winner(self):
        for player in self.players:
            # Check horizontal
            for row in self.game_state:
                for i in range(3):
                    if row[i] != player:
                        break
                    if i == 2:
                        self.winner = player
                        return

            # Check vertical
            for col in range(3):
                for row in range(3):
                    if self.game_state[row][col] != player:
                        break
                    if row == 2:
                        self.winner = player
                        return

            # Check top-left to bottom-right diagonal
            for i in range(3):
                if self.game_state[i][i] != player:
                    break
                if i == 2:
                    self.winner = player
                    return

            # Check bottom-left to top-right diagonal
            for i in range(3):
                if self.game_state[2 - i][i] != player:
                    break
                if i == 2:
                    self.winner = player
                    return
        
        # Check for draw
        for row in self.game_state:
            for col in row:
                if col == ' ':
                    return
        self.winner = "Draw"



    '''
        Prints the current game state
    '''
    def print_game(self):
        print()
        for i in range(3):
            row = self.game_state[i]
            print(" {} | {} | {} ".format(row[0], row[1], row[2]))
            if i != 2:
                print("------------")
        print()

def select_action_random(game):
    return rd.choice(game.actions)

'''
    Initializes the game and simulates it
'''
def simulate_game():
    game = Game() # The "X" player always starts the game

    # Initial action is always a 'X' in the center
    game.take_action((1, 1))
    game.print_game()

    while game.winner == None:
        
        if game.turn_player == 'X':
            action = select_action_random(game)
        if game.turn_player == 'O':
            # Should create a smart function for this one
            action = select_action_random(game)

        game.take_action(action)
        game.print_game()
    
    print("Winner: " + game.winner)

if __name__ == "__main__":
    simulate_game()