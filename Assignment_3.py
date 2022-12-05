import numpy as np
import random as rd
from math import sqrt
from math import log
import copy

class MonteCarloTree:

    def __init__(self, exploration_parameter=1):
        self.children = {} # key -> [Node1, Node2]
        self.n = {} # visit count for each node
        self.w = {} # win count for each node, equivalent to Q in this case
        self.exploration_parameter = exploration_parameter
        self.N = 0 # represents the number of times all reachable nodes have been considered (sum of the visit count of all reachable nodes)

    def choose(self, node):
        pass

    def playout(self, node):
        path = self.selection(node)
        leaf = path[-1]
        leaf.print_game()
        self.expansion(leaf)

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
    def uct(self, root):
        max_uct = 0
        for child in self.children[root]:
            uct = child[1]/child[0] + self.exploration_parameter*sqrt(log(self.N)/child[0]) # child[1] = w_i and child[0] = n_i
            if uct >= max_uct:
                node = child
                max_uct = uct
        return node

    # Returns all moves which have not been tried yet for a given state
    def find_undiscovered(self, node):
        undiscovered = []
        children = self.children[node]
        for child in children:
            if child not in self.children.keys():
                undiscovered.append(child)
        return undiscovered

    
    def selection(self, root):
        path = [root]

        node = root
        while True:
            
            # selection stops until a leaf node is reached
            if self.isLeafNode(node):
                return path

            # If not a leaf node prioritize undiscovered children
            undiscovered = self.find_undiscovered(node)
            if undiscovered:
                node = rd.choice(undiscovered)
                path.append(node)
                return path

            # uct is only applied if all children are discovered
            node = self.uct(node)
            path.append(node)
    
    def expansion(self, node):
        # Already expanded once
        if node in self.children:
            return
        self.children[node] = node.get_next_states()
        for child in self.children[node]:
            child.print_game()


    def simulation(self):
        pass

    def backpropogation(self):
        pass

class GameState:
    def __init__(self, game_state=[[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]):
        # Game setup
        self.players = ('X', 'O')
        self.game_state = game_state

        self.turn_player = self.get_turn_player(game_state)
        self.actions = self.get_actions(game_state)

        self.winner = self.determine_winner(self.game_state)

    def get_turn_player(self, game_state):
        actions_taken = 0

        for row in game_state:
            for state in row:
                if state != ' ':
                    actions_taken += 1

        if actions_taken % 2 == 0:
            return 'X'
        return 'O'

    def get_actions(self, game_state):
        actions = []

        for row in range(3):
            for col in range(3):
                if game_state[row][col] == ' ':
                    actions.append((row, col))
        
        return actions

    '''
        Updates the game-state by taking an action for a player.
        Action is a (x, y) tuple
    '''
    def take_action(self, action):
        x, y = action
        new_state = copy.deepcopy(self.game_state)
        new_state[y][x] = self.turn_player
        return GameState(game_state=new_state)

    def get_next_states(self):
        next_states = []
        if self.winner != None:
            return next_states

        for action in self.actions:
            next_states.append(self.take_action(action))


        return next_states

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
    def determine_winner(self, game_state):
        for player in self.players:
            # Check horizontal
            for row in game_state:
                for i in range(3):
                    if row[i] != player:
                        break
                    if i == 2:
                        return player

            # Check vertical
            for col in range(3):
                for row in range(3):
                    if game_state[row][col] != player:
                        break
                    if row == 2:
                        return player

            # Check top-left to bottom-right diagonal
            for i in range(3):
                if game_state[i][i] != player:
                    break
                if i == 2:
                    return player

            # Check bottom-left to top-right diagonal
            for i in range(3):
                if game_state[2 - i][i] != player:
                    break
                if i == 2:
                    return player
        
        # Check for draw
        for row in game_state:
            for col in row:
                if col == ' ':
                    return None
        return "Draw"

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
    # tree = MonteCarloTree()
    game = GameState(game_state= [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']])
    mct = MonteCarloTree()
    mct.playout(game)

    # # Initial action is always a 'X' in the center
    # game.take_action((1, 1))
    # game.print_game()

    # while game.winner == None:
        
    #     if game.turn_player == 'X':
    #         action = select_action_random(game)
    #     if game.turn_player == 'O':
    #         # Should create a smart function for this one
    #         action = select_action_random(game)

    #     game.take_action(action)
    #     game.print_game()
    
    # print("Winner: " + game.winner)

if __name__ == "__main__":
    simulate_game()