import math
import time
import pygame
import Constants
from Button import Button 

class Backtracking:
    def __init__(self, controller, board, boolean_board, animate):
        self.controller = controller
        self.grid = board
        self.boolean_board = boolean_board
        #stores whether the backtracking algorithm is currently backtracking
        self.backtracking = False
        self.num_rows, self.num_cols = 9, 9
        #stores whether the backtracking algorithm should be animated; is changed when finish animation is clicked
        self.animate_backtracking = animate

    #returns whether the move will not break anything
    def is_safe_move(self, row_number, col_number):
        is_broken = self.controller.is_row_broken(row_number) or self.controller.is_col_broken(col_number) or self.controller.is_matrix_broken(row_number, col_number)
        return not(is_broken)

    def solve(self, row, col):
        while row >= 0 and row < self.num_rows:
            #only occurs backtracking
            if col < 0:
                row -= 1
                col = self.num_cols - 1
            #only occurs while going forward
            elif col > self.num_cols - 1:
                row += 1
                col = 0
            elif self.boolean_board[row][col] and self.backtracking:
                col -= 1
            elif self.boolean_board[row][col]:
                col += 1
            else:
                #show backtracking step if needed
                if self.animate_backtracking:
                    self.animate_backtracking_algorithm(row, col)
                #add 1 until it's a safe move or the number = 10
                self.grid[row][col] += 1
                while not(self.is_safe_move(row, col)) and self.grid[row][col] <= 9:
                    self.grid[row][col] += 1
                #if the number is = 10, have to backtrack to change previous ones
                if self.grid[row][col] > 9:
                    self.backtracking = True
                    self.grid[row][col] = 0
                    col -= 1
                else:
                    #otherwise, continue forward
                    self.backtracking = False
                    col += 1

    #The recursive version of the backtracking algorithm; unused because it causes recursion depth error/stack overflow error
    """
    def solve(self, row, col):
        if row < 0 or row > self.num_rows - 1:
            return
        #will only occur while backtracking
        if col < 0:
            self.solve(row - 1, self.num_cols - 1)
        #will only occur while going forward
        elif col > self.num_cols - 1:
            self.solve(row + 1, 0)
        #backtrack past items in the original board
        elif self.boolean_board[row][col] and self.backtracking:
            self.solve(row, col - 1)
        #go past items in the original board
        elif self.boolean_board[row][col]:
            self.solve(row, col + 1)
        else:
            self.animate_backtracking_algorithm(row, col)
            self.grid[row][col] += 1
            while not(self.is_safe_move(row, col)) and self.grid[row][col] <= 9:
                self.grid[row][col] += 1
            if self.grid[row][col] > 9:
                self.backtracking = True
                self.grid[row][col] = 0
                self.solve(row, col - 1)
            else:
                self.backtracking = False
                self.solve(row, col + 1)
    """

    def print_grid(self):
        for row in range(self.num_rows):
            print(self.grid[row])

    def animate_backtracking_algorithm(self, row, col):
        #updates timer each time it is called
        self.controller.update_timer()
        for event in pygame.event.get():
            #quits program
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            #if the user pressed finish animation, change animate_backtracking to False to just skip to the solution
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.controller.finish_animation_button.is_hovering(pygame.mouse.get_pos()):
                    self.animate_backtracking = False
            #if the user is hovering over the finish_animation button, change it to white; otherwise it is blue
            elif event.type == pygame.MOUSEMOTION:
                color = Constants.BLUE
                if self.controller.finish_animation_button.is_hovering(pygame.mouse.get_pos()):
                    color = Constants.WHITE
                self.controller.finish_animation_button = Button(color, Constants.BLACK, Constants.PADDING * 2 + Constants.BACKTRACKING_BUTTON_WIDTH,
                                                                 3 * Constants.PADDING + Constants.NUM_ROWS * Constants.RECT_HEIGHT + Constants.NEW_GAME_BUTTON_HEIGHT,
                                                                 Constants.FINISH_ANIMATION_BUTTON_WIDTH, Constants.FINISH_ANIMATION_BUTTON_HEIGHT, 'Finish Animation',
                                                                 Constants.BLACK, Constants.MENU_FONT_SIZE)
        #redraw the screen
        self.controller.redraw_screen(row, col, Constants.PURPLE)
        pygame.display.update()
        #delay 25 ms
        pygame.time.wait(25)

    #used for show solution
    def animate_solution(self, row, col):
        #updates timer every time it is called
        self.controller.update_timer()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        #redraw the screen with the additional number filled in
        self.controller.redraw_screen(row, col, Constants.PURPLE)
        pygame.display.update()
        #delay 30 ms
        pygame.time.wait(30)
