class TicTacToe:
    def __init__(self, game_state=(' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ')):
        self.game_state = game_state
        self.players = ('X', 'O')

    def get_active_player(self):
        completed_moves = 0

        for square in self.game_state:
            if square != ' ':
                completed_moves += 1
        
        if completed_moves % 2 == 0:
            return 'X'
        return 'O'

    def get_pos_moves(self):
        pos_moves = []

        for square in range(9):
            if self.game_state[square] == ' ':
                pos_moves.append(square)
        return pos_moves

    def get_winner(self):
        for player in self.players:
            
            # Check horizontal
            for row in range(3):
                for col in range(3):
                    if self.game_state[row * 3 + col] != player:
                        break
                    if col == 2:
                        return player
            
            # Check vertical
            for col in range(3):
                for row in range(3):
                    if self.game_state[row * 3 + col] != player:
                        break
                    if row == 2:
                        return player

            # Check top-left to bottom-right diagonal
            for square in [0, 4, 8]:
                if self.game_state[square] != player:
                    break
                if square == 8:
                    return player

            # Check bottom-left to top-right diagonal
            for square in [2, 4, 6]:
                if self.game_state[square] != player:
                    break
                if square == 6:
                    return player        

        # Check for draw
        for square in self.game_state:
            if square == ' ':
                return None
        return "Draw"

    def get_next_state(self, move):
        if move not in self.get_pos_moves():
            return None
        
        # Create copy of current board
        board = [' ' for _ in range(9)]
        for i in range(9):
            board[i] = self.game_state[i]
        
        # Add the move
        board[move] = self.get_active_player()
        return TicTacToe(game_state=tuple(board))

    def get_all_next_states(self):
        states = []

        for action in self.get_pos_moves():
            states.append(self.get_next_state(action))
        return states


    def print(self):
        g = self.game_state

        print()
        for row in range(3):
            print(" {} | {} | {} ".format(g[3 * row], g[3 * row + 1], g[3 * row + 2]))
            if row != 2:
                print("-----------")
        print()

    # Required functions to use class as key 
    def __eq__(self, other):
        return self.game_state == other.game_state

    def __hash__(self):
        return hash(self.game_state)