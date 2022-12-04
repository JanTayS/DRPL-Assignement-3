import numpy as np
import random as rd
from math import sqrt
from math import log

class MonteCarloTree:

    def __init__(self, exploration_parameter=1):
        self.children = {} # key -> [Node1, Node2]
        self.n = {} # visit count for each node
        self.w = {} # win count for each node, equivalent to Q in this case
        self.exploration_parameter = exploration_parameter
        self.N = 0 # represents the number of times all reachable nodes have been considered (sum of the visit count of all reachable nodes)

    # a leaf is any node that has a potential child from which no simulation (playout) has yet been initiated
    # or a node is a leaf if the state is a terminal state
    def isLeafNode(self, node):
        # Undiscovered node has no play yet so is a leaf
        if node not in self.children:
            return True

        # If discovered but has no children is also a leaf since it is a terminal state
        if not self.children[node]:
            return True
        return False

    # The root is the current game state
    def best_uct(self, root):
        max_uct = 0
        for child in self.children[root]:
            uct = child[1]/child[0] + self.exploration_parameter*sqrt(log(self.N)/child[0]) # child[1] = w_i and child[0] = n_i
            if uct >= max_uct:
                node = child
                max_uct = uct
        return node
    
    def selection(self, root):
        if self.isLeafNode(root):
            node = self.best_uct(root)
        else: 
            node = rd.choice(self.children)# random child
        return node
        
    def selection(self, root):
        path = [root]

        node = root
        while True:
            
            # selection stops until a leaf node is reached
            if self.isLeafNode(node):
                return path

            node = self.uct(node)
    
    def expansion(self, node):
        self.children[node] = []

    def simulation(self):
        pass

    def backpropogation(self):
        pass
        

# A node represents a state of the game
# class Node:

#     def __init__(self, state, reward, children):
#         self.state = state
#         self.reward = reward
#         self.children = children

#     # All possi 
#     def all_children(self)


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

    def get_actions(self):
        actions = []
        return actions


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
    tree = MonteCarloTree()
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