"""
Tic Tac Toe Player
"""

import math
import copy

class InvalidMoveError(Exception):
    pass

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    if x_count > o_count:
        return O
    else:
        return X

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i,j))
    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action is None:
        return board
    # Get the action
    i, j = action

    # Return error if position is occupied
    if board[i][j] != EMPTY:
        raise InvalidMoveError('Cannot pick this spot. Please select another spot.')
    
    # Create a new copy of the board
    new_board = copy.deepcopy(board)

    # Add move to the spot and return
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    columns = [[board[j][i] for j in range(3)] for i in range(3)]
    rows = [board[i] for i in range(3)]
    diag1 = [board[i][len(board) - i - 1] for i in range(len(board))]
    diag2 =[board[i][i] for i in range(len(board))]

    lines = rows + columns + [diag1] + [diag2]
    print(lines)

    for line in lines:
        if line.count(X) == 3:
            return X
        elif line.count(O) == 3:
            return O
    
    for row in board:
        for i in row:
            if i is not None:
                return None
        

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) in (X, O,) or all(all(i is not None for i in row) for row in board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    if winner(board) == None:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """ 
    if terminal(board):
        return None

    best_action = None
    if player(board) == X:
        v = -math.inf
        for action in actions(board):
            new_board = result(board, action)
            new_v = min_value(new_board)
            if new_v > v:
                v = new_v
                best_action = action
    else:
        v = math.inf
        for action in actions(board):
            new_board = result(board, action)
            new_v = max_value(new_board)
            if new_v < v:
                v = new_v
                best_action = action

    return best_action

def max_value(board):
    if terminal(board):
        return utility(board)

    v = -math.inf
    for action in actions(board):
        new_board = result(board, action)
        v = max(v, min_value(new_board))

    return v

def min_value(board):
    if terminal(board):
        return utility(board)

    v = math.inf
    for action in actions(board):
        new_board = result(board, action)
        v = min(v, max_value(new_board))

    return v