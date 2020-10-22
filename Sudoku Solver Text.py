# This script solves a game of Suduko using the backtrack algorithm.

# Solves game.
def solve(board):
    """
    :param board: 2d list of ints
    :return: solved board
    """

    # find next empty space.
    empty = find_empty(board)
    if empty:  # if empty space was found, set (row, col) = empty space.
        (row, col) = empty
    else:  # if no empty space found the board is solved.
        return True

    # fill empty space and check if value is valid
    for i in range(1, 10):
        if valid(board, (row, col), i):  # if value is valid, add it to the board
            board[row][col] = i
            if solve(board):  # if new board is valid continue
                return True
            board[row][col] = 0  # backtrack
    return False


# Finds empty space on board (empty spaces are represented with value '0').
def find_empty(board):
    """
    :param board: 2d list of ints
    :return: (int, int) row col
    """
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 0:
                return (i, j)
    return None


# Checks if value is valid.
def valid(board, position, number):
    """
    :param board: 2d list of ints
    :param position: (int, int) row col
    :param number: int
    :return: boolean
    """

    # Check row
    for i in range(len(board)):
        if board[position[0]][i] == number:
            return False

    # Check col
    for i in range(len(board)):
        if board[i][position[1]] == number:
            return False

    # Checks box
    box_row = int(position[0] / 3) * 3
    box_col = int(position[1] / 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == number and (i, j) != position:
                return False

    # Value is valid
    return True


# Prints board.
def print_board(board):
    """
    :param board: 2d list of ints
    :return: none
    """
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - -" + "    " + "- - -" + "    " + "- - -")
        for j in range(len(board)):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(board[i][j], end="\n")
            else:
                print(str(board[i][j]) + " ", end="")


# Board.
board1 = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 3, 6, 0, 0, 0, 0, 0],
          [0, 7, 0, 0, 9, 0, 2, 0, 0],
          [0, 5, 0, 0, 0, 7, 0, 0, 0],
          [0, 0, 0, 0, 4, 5, 7, 0, 0],
          [0, 0, 0, 1, 0, 0, 0, 3, 0],
          [0, 0, 1, 0, 0, 0, 0, 6, 8],
          [0, 0, 8, 5, 0, 0, 0, 1, 0],
          [0, 9, 0, 0, 0, 0, 4, 0, 0]]

solve(board1)
print_board(board1)
