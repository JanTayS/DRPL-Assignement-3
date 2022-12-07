import random as rd

from math import sqrt
from math import log

from ticTacToe import TicTacToe

class MonteCarloTree:

    def __init__(self, c=1):
        self.children = {} # key -> [Node1, Node2]
        self.n = {} # visit count for each node
        self.q = {} # win count for each node, equivalent to Q in this case
        self.c = c # exploration  parameter
        self.N = 0 # represents the number of times all reachable nodes have been considered (sum of the visit count of all reachable nodes)

    # The root is the current game state
    def uct(self, node):
        max = 0
        best = None

        for child in self.children[node]:
            uct = self.q[child] / self.n[child] + self.c * sqrt(log(self.N) / self.n[child])
            if uct >= max:
                best = child
                max = uct
        
        return best
    
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

    # Returns all moves which have not been tried yet for a given state
    def find_undiscovered(self, node):
        undiscovered = []
        children = self.children[node]
        for child in children:
            if child not in self.children.keys():
                undiscovered.append(child)
        return undiscovered

    def playout(self, node):
        # Find leaf node L with the most potential
        path = self.selection(node) 
        L = path[-1]
        
        # If L doesn't end the game expand the tree from L
        self.expansion(L)

        # Select random action C from L's children, then simulate a full game for this action 
        C = L
        # No actions (children) means L is terminal, then pass L to simulate instead of a child
        if self.children[L]:
            C = rd.choice(self.children[L]) 
        path.append(C)
        reward = self.simulation(C)

        self.backpropagation(path, reward)


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
        # We expand everything so only one expansion for each node
        if node in self.children:
            return
        self.children[node] = node.get_all_next_states()

    def simulation(self, state):
        while not state.get_winner():
            nxt_states = state.get_all_next_states()
            state = rd.choice(nxt_states)

        # Return 1 if O wins, 0.5 for Draw, 0 if X wins
        if state.get_winner() == 'O':
            return 1
        if state.get_winner() == "Draw":
            return 0.5
        return 0

    def backpropagation(self, path, reward):
        for node in path:
            if node not in self.q:
                self.q[node] = 0
            if node not in self.n:
                self.n[node] = 0
            
            self.q[node] += reward
            self.n[node] += 1
        
        self.N += 1

    def choose(self, node):
        max = 0
        best = None

        for child in self.children[node]:
            score = self.q[child] / self.n[child]
            if score >= max:
                best = child
                max = score
        
        return best