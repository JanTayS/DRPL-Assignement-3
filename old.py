import numpy as np
import random as rd
from math import sqrt
from math import log
import copy

class MonteCarloTree:

    def __init__(self, c=1):
        self.children = {} # key -> [Node1, Node2]
        self.n = {} # visit count for each node
        self.w = {} # win count for each node, equivalent to Q in this case
        self.c = c # exploration  parameter
        self.N = 0 # represents the number of times all reachable nodes have been considered (sum of the visit count of all reachable nodes)

    def choose(self, node):
        pass

    def playout(self, node):
        path = self.selection(node) # Find leaf node L
        L = path[-1]
        self.expansion(L) # If L doesn't end the game expand the tree from L
        
        # Select random action C from L's children, then simulate a full game for this action 
        C = L
        # No actions (children) means L is terminal, then pass L to simulate instead of a child
        if self.children[L]:
            C = rd.choice(self.children[L]) 
        path.append(C)
        print(path)
        reward = self.simulation(C)
        # self.backpropagation(path, reward)


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
            uct = self.w[child] / self.n[child] + self.c * sqrt(log(self.N)/self.n[child])
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
    
    # Expands a node in the tree with all actions that can be taken from that node
    def expansion(self, node):
        # Already expanded once
        if node in self.children:
            return
        self.children[node] = node.get_next_states()


    def simulation(self, state):
        state.print_game()
        while not state.winner:
            actions = state.get_actions(state.game_state)
            print(actions)
            nxt_states = state.get_next_states()
            state = rd.choice(nxt_states)
            state.print_game()

        # Return 1 if O wins
        if state.winner == 'O':
            return 1
        
        # Draw and loss return 0
        return 0

    def backpropagation(self, path, reward):
        for node in path.reverse():
            if node not in self.q:
                self.q[node] = 0
            if node not in self.n:
                self.n[node] = 0
            
            self.q[node] += 1
            self.n[node] += 1

class GameState:
    def __init__(self, game_state=((' ', ' ', ' '), (' ', ' ', ' '), (' ', ' ', ' '))):
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
        Creates a new game_state from an action for a player.
        Action is a (x, y) tuple
    '''
    def take_action(self, action):
        x, y = action
        # new_state = copy.deepcopy(self.game_state)
        new_state = np.asarray(self.game_state)
        new_state[y][x] = self.turn_player
        new_state = tuple(map(tuple, new_state))
        return GameState(game_state=new_state)

    def get_next_states(self):
        next_states = []
        if self.winner != None:
            return next_states

        for action in self.actions:
            next_states.append(self.take_action(action))


        return next_states

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

    # Required functions to use class as key 
    def __eq__(self, other):
        return self.game_state == other.game_state

    def __hash__(self):
        return hash(self.game_state)



def select_action_random(game):
    return rd.choice(game.actions)

'''
    Initializes the game and simulates it
'''
def simulate_game():
    game = GameState()
    mct = MonteCarloTree()
    mct.playout(game)




    # a = (('a', 'b'), ('a', 'c'))
    # # b = (('a', 'b'), ('a', 'c'))

    # print(np.asarray(a))
    # print(tuple(map(tuple, arr)))


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