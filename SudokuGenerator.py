from Backtracking import Backtracking
import random
from copy import copy, deepcopy

class SudokuGenerator:
    def __init__(self, controller):
        self.controller = controller
        self.num_rows = 9
        self.num_cols = 9


    def generate_matrices(self):
        #the number of missing elements from the board
        self.num_missing = random.randint(51, 58)
        #initial board is all 0's
        self.board = [[0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0]]
        #fills diagonal matrices because they will not overlap rows or cols
        self.fill_in_diagonal_matrix(0, 0)
        self.fill_in_diagonal_matrix(3, 3)
        self.fill_in_diagonal_matrix(6, 6)
        #the figures coming with the original board
        self.boolean_board = [[True,True,True,0,0,0,0,0,0],
                              [True,True,True,0,0,0,0,0,0],
                              [True,True,True,0,0,0,0,0,0],
                              [0,0,0,True,True,True,0,0,0],
                              [0,0,0,True,True,True,0,0,0],
                              [0,0,0,True,True,True,0,0,0],
                              [0,0,0,0,0,0,True,True,True],
                              [0,0,0,0,0,0,True,True,True],
                              [0,0,0,0,0,0,True,True,True]]
        #returns the board with 3 matrices filled in
        return self.board

    def fill_in_puzzle(self):
        #creates backtracker to fill in the rest of the squares in the puzzle
        self.backtracker = Backtracking(self.controller, self.board, self.boolean_board, False)
        self.backtracker.solve(0,0)
        #saves a copy of teh solution to the controller in case the user wants to instantly see the solution
        self.controller.solution = deepcopy(self.board)
        #self.print_grid()
        #removes a random number of elements from the board randomly
        self.remove_elements()
        return self.board

    def remove_elements(self):
        counter = 0
        while counter < self.num_missing:
            row = random.randint(0, self.num_rows - 1)
            col = random.randint(0, self.num_cols - 1)
            #removes random row, col that aren't already missing
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                counter += 1

    #fills in the matrices starting at row, col
    #no safe move detection is needed because none of these matrices overlap rows or cols
    def fill_in_diagonal_matrix(self, row, col):
        number_list = [1,2,3,4,5,6,7,8,9]
        random.shuffle(number_list)
        counter = 0
        for row_num in range(row, row + 3):
            for col_num in range(col, col + 3):
                self.board[row_num][col_num] = number_list[counter]
                counter += 1

    #prints the grid
    def print_grid(self):
        for row in range(self.num_rows):
            print(self.board[row])
            #extra line
            print('')
