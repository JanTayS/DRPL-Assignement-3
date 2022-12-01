import numpy as np
import random as rd

# rd.seed(1)

# initialize players
X = 1
O = 2
players = (O,X)

# initialize all possible actions
dimensions = 3
actions = []
for x_dimension in range(dimensions):
    for y_dimension in range(dimensions):
        actions.append((x_dimension,y_dimension))

# initialize starting state
state = np.zeros((3,3))
state[1,1] = X
actions.remove((1,1))

# TIC TAC TOE
not_finished = True
winner = None
while not_finished:
    for player in players:
        # placement which needs to be optimized
        if player == O:
            placement = rd.choice(actions)
        # random computer actions
        if player == X:
            placement = rd.choice(actions)
        state[placement[0],placement[1]] = player
        actions.remove(placement)
    
    print(state)
    print()

    # Checks for terminal state
    for x_dimension in range(dimensions):
        if state[x_dimension,0] != 0 and state[x_dimension,0] == state[x_dimension,1] and state[x_dimension,0] == state[x_dimension,2]:
            winner = state[x_dimension,0]
            not_finished = False
    for y_dimension in range(dimensions):
        if state[0,y_dimension] != 0 and state[0,y_dimension] == state[1,y_dimension] and state[0,y_dimension] == state[2,y_dimension]:
            winner = state[0,y_dimension]
            not_finished = False
    if state[0,0] != 0 and state[0,0] == state[1,1] and state[0,0] == state[2,2]:
        winner = state[0,0]
        not_finished = False
    if state[0,2] != 0 and state[0,2] == state[1,1] and state[0,2] == state[2,0]:
        winner = state[0,2]
        not_finished = False
    if actions == [] and winner != True:
        winner = None
        not_finished = False

print(state)
print(winner)