from tkinter import *
from PIL import Image, ImageTk


class Sudoku:
    def __init__(self):
        self.board = self.boards()

    def boards(self):
        board1 = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 3, 6, 0, 0, 0, 0, 0],
                  [0, 7, 0, 0, 9, 0, 2, 0, 0],
                  [0, 5, 0, 0, 0, 7, 0, 0, 0],
                  [0, 0, 0, 0, 4, 5, 7, 0, 0],
                  [0, 0, 0, 1, 0, 0, 0, 3, 0],
                  [0, 0, 1, 0, 0, 0, 0, 6, 8],
                  [0, 0, 8, 5, 0, 0, 0, 1, 0],
                  [0, 9, 0, 0, 0, 0, 4, 0, 0]]
        return board1

    # finds nearest empty square searching from top left to bottom right, row by row
    def find_empty(self):
        """
            :param board: 2d list of ints
            :return: (int, int) row col
        """
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 0:
                    return i, j
        return None

    # checks if attempted board entry is valid
    def valid(self, position, number):
        """
        :param board: 2d list of ints
        :param position: (int, int) row col
        :param number: int
        :return: boolean
        """

        # Check row
        for i in range(len(self.board)):
            if self.board[position[0]][i] == number:
                return False

        # Check col
        for i in range(len(self.board)):
            if self.board[i][position[1]] == number:
                return False

        # Checks box
        box_row = int(position[0] / 3) * 3
        box_col = int(position[1] / 3) * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == number and (i, j) != position:
                    return False

        # Value is valid
        return True

    # Solves board
    def solve(self):
        """
        :param self:
        :return: boolean
        """

        # find next empty space.
        empty = self.find_empty()
        if empty:  # if empty space was found, set (row, col) = empty space.
            (row, col) = empty
        else:  # if no empty space found the board is solved.
            return True

        # fill empty space and check if value is valid
        for i in range(1, 10):
            if self.valid((row, col), i):  # if value is valid, add it to the board
                self.board[row][col] = i
                if self.solve():  # if new board is valid continue
                    return True
                self.board[row][col] = 0  # backtrack
        return False

    # Prints board.
    def print_board(self):
        """
        :param self:
        :return: none
        """
        for i in range(len(self.board)):
            if i % 3 == 0 and i != 0:
                print("- - -" + "    " + "- - -" + "    " + "- - -")
            for j in range(len(self.board)):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")
                if j == 8:
                    print(self.board[i][j], end="\n")
                else:
                    print(str(self.board[i][j]) + " ", end="")


# class GUI sets up the sudoku board and displays it
class GUI:
    def __init__(self):
        self.main_frame = Frame(bg="white")
        self.sudoku = Sudoku()
        self.solved = [[8, 1, 2, 7, 5, 3, 6, 4, 9],
                       [9, 4, 3, 6, 8, 2, 1, 7, 5],
                       [6, 7, 5, 4, 9, 1, 2, 8, 3],
                       [1, 5, 4, 2, 3, 7, 8, 9, 6],
                       [3, 6, 9, 8, 4, 5, 7, 2, 1],
                       [2, 8, 7, 1, 6, 9, 5, 3, 4],
                       [5, 2, 1, 9, 7, 4, 3, 6, 8],
                       [4, 3, 8, 5, 2, 6, 9, 1, 7],
                       [7, 9, 6, 3, 1, 8, 4, 5, 2]]
        self.board_image = ImageTk.PhotoImage(Image.open("sudokublankgrid.png"))
        self.col_positions = [0.032, 0.14, 0.243, 0.355, 0.4625, 0.57, 0.6815, 0.787, 0.895]
        self.row_positions = [0.0355, 0.141, 0.246, 0.3575, 0.462, 0.5675, 0.678, 0.784, 0.888]
        self.cell_dimension = 0.075
        self.cell_labels = []
        self.cell_entries = []
        self.str_vars = []

        # main containers for board and buttons
        buttons_container = Frame(self.main_frame, bg="white")
        buttons_container.place(relx=0.2, rely=0.85, relwidth=0.6, relheight=0.1)
        self.board_container = Frame(self.main_frame, bg="white")
        self.board_container.place(relx=0.125, rely=0.05, relwidth=0.75, relheight=0.75)

        # setup buttons
        button_reset = Button(buttons_container, text="Reset Game", command=lambda: self.reset())
        button_reset.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.8)
        button_solve = Button(buttons_container, text="Solve Game", command=lambda: self.solve())
        button_solve.place(relx=0.4, rely=0.1, relwidth=0.2, relheight=0.8)
        button_enter = Button(buttons_container, text="Enter Value", command=lambda: self.entry())
        button_enter.place(relx=0.7, rely=0.1, relwidth=0.2, relheight=0.8)

        # setup board
        background_label = Label(self.board_container, image=self.board_image)
        background_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.setup_cells()

    def setup_cells(self):
        # sets up StringVars for each cell
        for i in range(9):
            self.str_vars.append([])
            for j in range(9):
                self.str_vars[i].append(StringVar())
                if self.sudoku.board[i][j] != 0:
                    self.str_vars[i][j].set(self.sudoku.board[i][j])

        # creates label and entry widgets
        for i in range(9):
            self.cell_labels.append([])
            self.cell_entries.append([])
            for j in range(9):
                self.cell_labels[i].append(Label(self.board_container, textvariable=self.str_vars[i][j], bg="white", font=30))
                self.cell_entries[i].append(Entry(self.board_container, bg="white"))

        # places all label and entry widgets
        for i in range(len(self.row_positions)):
            for j in range(len(self.col_positions)):
                if self.sudoku.board[i][j] != 0:
                    self.cell_labels[i][j].place(relx=self.col_positions[j], rely=self.row_positions[i], relwidth=self.cell_dimension, relheight=self.cell_dimension)
                else:
                    self.cell_entries[i][j].place(relx=self.col_positions[j], rely=self.row_positions[i], relwidth=self.cell_dimension, relheight=self.cell_dimension)

    def solve(self):
        self.sudoku.solve()
        self.forget_widgets()

        # place all cell label widgets
        for i in range(9):
            for j in range(9):
                self.cell_labels[i][j].place(relx=self.col_positions[j], rely=self.row_positions[i], relwidth=self.cell_dimension, relheight=self.cell_dimension)

        # updates label widget values
        for i in range(9):
            for j in range(9):
                if self.sudoku.board[i][j] != 0:
                    self.str_vars[i][j].set(self.sudoku.board[i][j])

    def reset(self):
        self.sudoku.board = self.sudoku.boards()
        self.forget_widgets()

        # places all label and entry widgets
        for i in range(len(self.row_positions)):
            for j in range(len(self.col_positions)):
                if self.sudoku.board[i][j] != 0:
                    self.cell_labels[i][j].place(relx=self.col_positions[j], rely=self.row_positions[i],
                                                 relwidth=self.cell_dimension, relheight=self.cell_dimension)
                else:
                    self.cell_entries[i][j].place(relx=self.col_positions[j], rely=self.row_positions[i],
                                                  relwidth=self.cell_dimension, relheight=self.cell_dimension)

        # resets all StringVars
        for i in range(9):
            for j in range(9):
                if self.sudoku.board[i][j] != 0:
                    self.str_vars[i][j].set(self.sudoku.board[i][j])
                else:
                    self.str_vars[i][j].set("")

    def forget_widgets(self):
        # remove all cell entry and label widgets
        for i in range(9):
            for j in range(9):
                self.cell_labels[i][j].place_forget()
                self.cell_entries[i][j].place_forget()

    def entry(self):
        # get entries and try putting them on board
        for i in range(9):
            for j in range(9):
                if self.cell_entries[i][j].get() != "":
                    if self.cell_entries[i][j].get() == str(self.solved[i][j]):
                        self.sudoku.board[i][j] = self.solved[i][j]
                else:
                    pass

        # update all StringVar variables
        for i in range(9):
            for j in range(9):
                if self.sudoku.board[i][j] != 0:
                    self.str_vars[i][j].set(self.sudoku.board[i][j])

        # show updated board
        self.forget_widgets()
        for i in range(len(self.row_positions)):
            for j in range(len(self.col_positions)):
                if self.sudoku.board[i][j] != 0:
                    self.cell_labels[i][j].place(relx=self.col_positions[j], rely=self.row_positions[i],
                                                 relwidth=self.cell_dimension, relheight=self.cell_dimension)
                else:
                    self.cell_entries[i][j].place(relx=self.col_positions[j], rely=self.row_positions[i],
                                                  relwidth=self.cell_dimension, relheight=self.cell_dimension)


# main loop
root = Tk()
root.geometry("605x585")
root.title("Sudoku Solver")
root.resizable(0, 0)
main = GUI()
main.main_frame.place(relx=0., rely=0, relwidth=1, relheight=1)
root.mainloop()
