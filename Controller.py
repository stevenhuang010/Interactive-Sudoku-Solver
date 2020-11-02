from Backtracking import Backtracking
import pygame
import math
from Button import Button
from SudokuGenerator import SudokuGenerator
import Constants

class Controller:
    def __init__(self):
        self.sudoku_generator = SudokuGenerator(self)
        #creates a new sudoku board
        self.create_new_board()
        #creates a 9 x 9 boolean grid where True means that the row, col position was filled in with the original board
        self.initialize_boolean_board()
        #used for backtracking solving algorithm
        self.backtracker = Backtracking(self, self.board, self.boolean_board, True)

        #used for highlighting rows, cols, and matrices that are invalid once a user puts a number in the grid
        self.invalid_rows = []
        self.invalid_cols = []
        self.invalid_matrices = []

        pygame.init()

        self.scene = pygame.display.set_mode([Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT])

        pygame.display.set_caption("Sudoku")

        #start time for clock
        self.start_time = 0

        #font used for numbers in the grid, the clock, and the finished screen
        self.grid_font = pygame.font.SysFont('segoescript', 33)

        #font used for the time
        self.time_font = pygame.font.SysFont('segoescript', 11)

        #font used for notes in numbers in the grid
        self.note_font = pygame.font.SysFont('segoescript', Constants.NOTE_FONT_SIZE)

        #needed for centering
        self.number_width, self.number_height = self.grid_font.size("1")

        self.create_blank_note_board()
        #stores whether the notes button is pressed
        self.notes_pressed = False
        #initialize all of the buttons at the bottom of the window
        #creates new game
        self.new_game_button = Button(Constants.BLUE, Constants.BLACK,
                                      Constants.PADDING * 3 + Constants.CLEAR_BOARD_BUTTON_WIDTH + Constants.SOLVE_BUTTON_WIDTH,
                                      Constants.PADDING + Constants.NUM_ROWS * Constants.RECT_HEIGHT + Constants.PADDING ,
                                      Constants.NEW_GAME_BUTTON_WIDTH, Constants.NEW_GAME_BUTTON_HEIGHT, 'New Puzzle',
                                      Constants.BLACK, Constants.MENU_FONT_SIZE)
        #solves puzzle instantly
        self.solve_button = Button(Constants.BLUE, Constants.BLACK, Constants.PADDING * 2 + Constants.CLEAR_BOARD_BUTTON_WIDTH,
                                   Constants.PADDING + Constants.NUM_ROWS * Constants.RECT_HEIGHT + Constants.PADDING,
                                   Constants.SOLVE_BUTTON_WIDTH, Constants.SOLVE_BUTTON_HEIGHT, 'Show Solution', Constants.BLACK,
                                   Constants.MENU_FONT_SIZE)
        #clears the board of user markings
        self.clear_board_button = Button(Constants.BLUE, Constants.BLACK, Constants.PADDING,
                                         Constants.PADDING + Constants.NUM_ROWS * Constants.RECT_HEIGHT + Constants.PADDING,
                                         Constants.CLEAR_BOARD_BUTTON_WIDTH, Constants.CLEAR_BOARD_BUTTON_HEIGHT, 'Clear Board',
                                         Constants.BLACK, Constants.MENU_FONT_SIZE)
        #allows users to draw notes
        self.notes_button = Button(Constants.BLUE, Constants.BLACK,
                                   Constants.PADDING * 4 + Constants.CLEAR_BOARD_BUTTON_WIDTH + Constants.SOLVE_BUTTON_WIDTH + Constants.NEW_GAME_BUTTON_WIDTH,
                                   Constants.PADDING + Constants.NUM_ROWS * Constants.RECT_HEIGHT + Constants.PADDING,
                                   Constants.NOTES_BUTTON_WIDTH, Constants.NOTES_BUTTON_HEIGHT, "Notes",
                                   Constants.BLACK, Constants.MENU_FONT_SIZE)

        #show backtracking animation button
        self.backtracking_button = Button(Constants.BLUE, Constants.BLACK, Constants.PADDING,
                                          3 * Constants.PADDING + Constants.NUM_ROWS * Constants.RECT_HEIGHT + Constants.NEW_GAME_BUTTON_HEIGHT,
                                          Constants.BACKTRACKING_BUTTON_WIDTH, Constants.BACKTRACKING_BUTTON_HEIGHT,
                                          'Solve with Backtracking Animation', Constants.BLACK, Constants.MENU_FONT_SIZE)
        #finish backtracking animation button
        self.finish_animation_button = Button(Constants.BLUE, Constants.BLACK, Constants.PADDING * 2 + Constants.BACKTRACKING_BUTTON_WIDTH,
                                              3 * Constants.PADDING + Constants.NUM_ROWS * Constants.RECT_HEIGHT + Constants.NEW_GAME_BUTTON_HEIGHT,
                                              Constants.FINISH_ANIMATION_BUTTON_WIDTH, Constants.FINISH_ANIMATION_BUTTON_HEIGHT, 'Finish Animation',
                                              Constants.BLACK, Constants.MENU_FONT_SIZE)
        #button that displays "new puzzle" after completing the old puzzle
        self.finish_button = Button(Constants.BLUE, Constants.BLACK,
                                    Constants.WINDOW_WIDTH // 2 - Constants.FINISHED_BUTTON_WIDTH // 2,
                                    Constants.WINDOW_HEIGHT // 2 - Constants.FINISHED_BUTTON_HEIGHT // 2, Constants.FINISHED_BUTTON_WIDTH,
                                    Constants.FINISHED_BUTTON_HEIGHT, 'New Puzzle', Constants.BLACK, 15)
        #once curr_time_seconds is 1 or more greater than prev_time_seconds, clock will update
        self.curr_time_seconds = 0
        self.prev_time_seconds = -1
        #draws the time in the bottom right corner
        self.draw_time_label()
        #draws the screen
        self.redraw_screen(-1, -1, Constants.BLUE)

        pygame.display.update()

        #stores if the user cancels the window
        finished = False
        #stores the part of the grid that is now being focused on by the user when the user clicks a grid position
        self.curr_cell = [-1, -1]

        #stores whether the white faded screen that shows when a puzzle is completed is showing
        self.is_finished_screen_showing = False

        while not finished:
            #updates clock
            self.update_timer()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finished = True
                #if the game is currently going
                if not self.is_finished_screen_showing:
                    position = pygame.mouse.get_pos()
                    #user clicked somewhere on the grid
                    if event.type == pygame.MOUSEBUTTONDOWN and self.is_in_bounds(position):
                        #colors in the focused cell BEIGE
                        self.update_grid_focus(position)
                    #if user presses on the new puzzle button
                    elif event.type == pygame.MOUSEBUTTONDOWN and self.new_game_button.is_hovering(position):
                        self.reinitialize_variables_for_new_game()
                    #if user wants to clear their markings, resets some of the variables
                    elif event.type == pygame.MOUSEBUTTONDOWN and self.clear_board_button.is_hovering(position):
                        self.clear_board()
                        self.reset_in_game_variables()
                        self.scene.fill(Constants.BLUE)
                        self.redraw_screen(-1, -1, Constants.BLUE)
                    #wants to immediately solve the board
                    elif event.type == pygame.MOUSEBUTTONDOWN and self.solve_button.is_hovering(position):
                        self.clear_board()
                        self.reset_in_game_variables()
                        self.show_solution()
                        #shows finish screen
                        self.execute_finish_screen()
                    #wants to show animated backtracking screen
                    elif event.type == pygame.MOUSEBUTTONDOWN and self.backtracking_button.is_hovering(position):
                        self.clear_board()
                        self.reset_in_game_variables()
                        #solve w/ backtracking algorithm
                        self.backtracker.solve(0, 0)
                        #show finish screen
                        self.execute_finish_screen()
                    #animates clicking notes button
                    elif event.type == pygame.MOUSEBUTTONDOWN and self.notes_button.is_hovering(position):
                        self.clicked_notes_button()
                    #if not mouse pressed, but just mouse motion
                    elif event.type == pygame.MOUSEMOTION:
                        self.animate_buttons()
                        self.redraw_buttons()
                    #if user finishes board, show finish screen
                    elif self.is_board_solved():
                        self.execute_finish_screen()
                    pygame.display.update()
                    #controls key presses on the grid
                    self.update_board_if_key_pressed()
                #if the finish screen is showing and finish-button is pressed for new game
                elif event.type == pygame.MOUSEBUTTONDOWN and self.finish_button.is_hovering(pygame.mouse.get_pos()):
                        self.reinitialize_variables_for_new_game()
                        pygame.display.update()
                #if finish button is being hovered over
                elif event.type == pygame.MOUSEMOTION:
                        self.finish_button_hovering()
                        pygame.display.update()
        pygame.quit()

    def finish_button_hovering(self):
        if self.finish_button.is_hovering(pygame.mouse.get_pos()):
            self.finish_button = Button(Constants.WHITE, Constants.BLACK,
                                        Constants.WINDOW_WIDTH // 2 - Constants.FINISHED_BUTTON_WIDTH // 2,
                                        Constants.WINDOW_HEIGHT // 2 - Constants.FINISHED_BUTTON_HEIGHT // 2, Constants.FINISHED_BUTTON_WIDTH,
                                        Constants.FINISHED_BUTTON_HEIGHT, 'New Puzzle', Constants.BLACK, 15)
        else:
            self.finish_button = Button(Constants.BLUE, Constants.BLACK,
                                        Constants.WINDOW_WIDTH // 2 - Constants.FINISHED_BUTTON_WIDTH // 2,
                                        Constants.WINDOW_HEIGHT // 2 - Constants.FINISHED_BUTTON_HEIGHT // 2, Constants.FINISHED_BUTTON_WIDTH,
                                        Constants.FINISHED_BUTTON_HEIGHT, 'New Puzzle', Constants.BLACK, 15)
        self.finish_button.draw(self.scene)

    def clicked_notes_button(self):
        color = Constants.BLUE
        #if notes hasn't been pressed, it will change to white
        if not self.notes_pressed:
            color = Constants.WHITE
        self.notes_button = Button(color, Constants.BLACK,
                                   Constants.PADDING * 4 + Constants.CLEAR_BOARD_BUTTON_WIDTH + Constants.SOLVE_BUTTON_WIDTH + Constants.NEW_GAME_BUTTON_WIDTH,
                                   Constants.PADDING + Constants.NUM_ROWS * Constants.RECT_HEIGHT + Constants.PADDING,
                                   Constants.NOTES_BUTTON_WIDTH, Constants.NOTES_BUTTON_HEIGHT, "Notes",
                                   Constants.BLACK, Constants.MENU_FONT_SIZE)
        #stores that notes is now pressed
        self.notes_pressed = not self.notes_pressed

    #resets the variables that have been changed this game, but still preserves the same game
    def reset_in_game_variables(self):
        #resets invalid rows, cols, matrices
        self.invalid_rows = []
        self.invalid_cols = []
        self.invalid_matrices = []
        self.curr_cell = [-1, -1]
        #make notes_pressed back to blue
        self.notes_pressed = False
        self.animate_buttons()

    #creates a 3d array with blank notes for each cell
    def create_blank_note_board(self):
        self.note_numbers = [[[], [], [], [], [], [], [], [], []],
                             [[], [], [], [], [], [], [], [], []],
                             [[], [], [], [], [], [], [], [], []],
                             [[], [], [], [], [], [], [], [], []],
                             [[], [], [], [], [], [], [], [], []],
                             [[], [], [], [], [], [], [], [], []],
                             [[], [], [], [], [], [], [], [], []],
                             [[], [], [], [], [], [], [], [], []],
                             [[], [], [], [], [], [], [], [], []]]

    #instantly shows the solution and animates it as fills in rows
    def show_solution(self):
        for row in range(Constants.NUM_ROWS):
            for col in range(Constants.NUM_COLS):
                #sets the board to the solution created in sudoku generator and assigned to controller before blanks put in
                self.board[row][col] = self.solution[row][col]
                #animates the setting of the board to the solution for every row, col
                self.backtracker.animate_solution(row, col)

    #updates cell to BEIGE if it is clicked by user
    def update_grid_focus(self, position):
        curr_col = self.get_col(position[0])
        curr_row = self.get_row(position[1])
        #if the row, col where the user clicked is not part of the given sudoku board
        if self.is_changeable(curr_row, curr_col):
            #highlights the cell as BLUE
            self.redraw_screen(curr_row, curr_col, Constants.BLUE)
            #updates curr_cell, which stores focused_cell
            self.curr_cell[0] = curr_row
            self.curr_cell[1] = curr_col

    #redraws all of the buttons except finish animation button which is controlled when backtracking algorithm is run
    def redraw_buttons(self):
        self.solve_button.draw(self.scene)
        self.clear_board_button.draw(self.scene)
        self.new_game_button.draw(self.scene)
        self.backtracking_button.draw(self.scene)
        self.notes_button.draw(self.scene)
        self.finish_animation_button.draw(self.scene)

    #creates a new sudoku board
    def create_new_board(self):
        self.board = self.sudoku_generator.generate_matrices()
        #stores the completely filled grid for instant solving
        self.solution = []
        self.board = self.sudoku_generator.fill_in_puzzle()

    #show the finish screen
    def execute_finish_screen(self):
        #change this to [-1, -1], so when self.update_board_if_key_pressed is called afterwards, it doesn't run because self.curr_cell[0] = -1
        self.curr_cell = [-1, -1]

        self.is_finished_screen_showing = True
        #controls fading white screen
        self.fade(Constants.WHITE)
        #get current finish time
        finish_time = (pygame.time.get_ticks() - self.start_time) // 1000
        #"Sudoku Solved!" text
        self.write_finish_screen_text()
        #finish time text
        self.write_finish_time(finish_time)
        #new puzzle button
        self.finish_button.draw(self.scene)

    #redraw screen every second for the purpose of the clock
    def update_timer(self):
        self.curr_time_seconds = (pygame.time.get_ticks() - self.start_time) // 1000
        if self.curr_time_seconds >= self.prev_time_seconds and not self.is_finished_screen_showing:
            #redraws the screen
            self.redraw_screen(self.curr_cell[0], self.curr_cell[1], Constants.BLUE)
            self.prev_time_seconds = self.curr_time_seconds
            pygame.display.update()

    #controls the formatting of the time in the bottom right corner
    def draw_time_label(self):
        str_time = ""
        if self.curr_time_seconds < 10:
            str_time = "0:0" + str(self.curr_time_seconds)
        elif self.curr_time_seconds < 60:
            str_time = "0:" + str(self.curr_time_seconds)
        else:
            minutes = self.curr_time_seconds // 60
            seconds = self.curr_time_seconds % 60
            str_addition = ""
            if seconds < 10:
                str_addition = "0"
            str_time = str(minutes) + ":" + str_addition + str(seconds)
        text_width, text_height = self.time_font.size(str_time)
        x_pos = ((Constants.PADDING * 5 + Constants.CLEAR_BOARD_BUTTON_WIDTH + Constants.SOLVE_BUTTON_WIDTH + Constants.NEW_GAME_BUTTON_WIDTH + Constants.NOTES_BUTTON_WIDTH) +
                 (Constants.PADDING + Constants.NUM_COLS * Constants.RECT_WIDTH)) // 2 - text_width // 2
        y_pos = ((2 * Constants.PADDING + Constants.NUM_ROWS * Constants.RECT_HEIGHT) +
                 (2 * Constants.PADDING + Constants.NUM_ROWS * Constants.RECT_HEIGHT + Constants.SOLVE_BUTTON_HEIGHT)) // 2 - text_height // 2
        #creates text from the time_font
        time_label = self.time_font.render(str_time, True, Constants.BLACK)
        #places text on screen
        self.scene.blit(time_label, (x_pos, y_pos))

    def animate_buttons(self):
        #new puzzle button
        color = Constants.BLUE
        if self.new_game_button.is_hovering(pygame.mouse.get_pos()):
            color = Constants.WHITE
        self.new_game_button = Button(color, Constants.BLACK,
                                      Constants.PADDING * 3 + Constants.CLEAR_BOARD_BUTTON_WIDTH + Constants.SOLVE_BUTTON_WIDTH,
                                      Constants.PADDING + Constants.NUM_ROWS * Constants.RECT_HEIGHT + Constants.PADDING,
                                      Constants.NEW_GAME_BUTTON_WIDTH, Constants.NEW_GAME_BUTTON_HEIGHT, 'New Puzzle',
                                      Constants.BLACK, Constants.MENU_FONT_SIZE)

        #clear board button
        color = Constants.BLUE
        if self.clear_board_button.is_hovering(pygame.mouse.get_pos()):
            color = Constants.WHITE
        self.clear_board_button = Button(color, Constants.BLACK, Constants.PADDING,
                                         Constants.PADDING + Constants.NUM_ROWS * Constants.RECT_HEIGHT + Constants.PADDING,
                                         Constants.CLEAR_BOARD_BUTTON_WIDTH, Constants.CLEAR_BOARD_BUTTON_HEIGHT, 'Clear Board',
                                         Constants.BLACK, Constants.MENU_FONT_SIZE)
        #show solution button
        color = Constants.BLUE
        if self.solve_button.is_hovering(pygame.mouse.get_pos()):
            color = Constants.WHITE
        self.solve_button = Button(color, Constants.BLACK, Constants.PADDING * 2 + Constants.CLEAR_BOARD_BUTTON_WIDTH,
                                   Constants.PADDING + Constants.NUM_ROWS * Constants.RECT_HEIGHT + Constants.PADDING,
                                   Constants.SOLVE_BUTTON_WIDTH, Constants.SOLVE_BUTTON_HEIGHT, 'Show Solution', Constants.BLACK,
                                   Constants.MENU_FONT_SIZE)

        #animate backtracking algorithm button
        color = Constants.BLUE
        if self.backtracking_button.is_hovering(pygame.mouse.get_pos()):
            color = Constants.WHITE
        self.backtracking_button = Button(color, Constants.BLACK, Constants.PADDING,
                                          3 * Constants.PADDING + Constants.NUM_ROWS * Constants.RECT_HEIGHT + Constants.NEW_GAME_BUTTON_HEIGHT,
                                          Constants.BACKTRACKING_BUTTON_WIDTH, Constants.BACKTRACKING_BUTTON_HEIGHT,
                                          'Solve with Backtracking Animation', Constants.BLACK, Constants.MENU_FONT_SIZE)

        #only animate to white if notes hasn't been pressed yet
        if not self.notes_pressed:
            color = Constants.BLUE
            if self.notes_button.is_hovering(pygame.mouse.get_pos()):
                color = Constants.WHITE
            self.notes_button = Button(color, Constants.BLACK,
                                       Constants.PADDING * 4 + Constants.CLEAR_BOARD_BUTTON_WIDTH + Constants.SOLVE_BUTTON_WIDTH + Constants.NEW_GAME_BUTTON_WIDTH,
                                       Constants.PADDING + Constants.NUM_ROWS * Constants.RECT_HEIGHT + Constants.PADDING,
                                       Constants.NOTES_BUTTON_WIDTH, Constants.NOTES_BUTTON_HEIGHT, "Notes",
                                       Constants.BLACK, Constants.MENU_FONT_SIZE)

    #delete all user markings by setting them in the board to 0
    def clear_board(self):
        for row in range(Constants.NUM_ROWS):
            for col in range(Constants.NUM_COLS):
                if not self.boolean_board[row][col]:
                    self.board[row][col] = 0
                    #resets note_numbers as well
                    self.note_numbers[row][col] = []

    #creates new game
    def reinitialize_variables_for_new_game(self):

        self.is_finished_screen_showing = False
        #blanks the note board
        self.create_blank_note_board()
        self.create_new_board()
        self.initialize_boolean_board()
        self.backtracker = Backtracking(self, self.board, self.boolean_board, True)

        self.reset_in_game_variables()
        #need to add this so that new puzzle after finish goes back to blue
        self.finish_button = Button(Constants.BLUE, Constants.BLACK,
                                    Constants.WINDOW_WIDTH // 2 - Constants.FINISHED_BUTTON_WIDTH // 2,
                                    Constants.WINDOW_HEIGHT // 2 - Constants.FINISHED_BUTTON_HEIGHT // 2, Constants.FINISHED_BUTTON_WIDTH,
                                    Constants.FINISHED_BUTTON_HEIGHT, 'New Puzzle', Constants.BLACK, 15)
        #need to add this so that finish animation button goes back to blue
        self.finish_animation_button = Button(Constants.BLUE, Constants.BLACK,
                                              Constants.PADDING * 2 + Constants.BACKTRACKING_BUTTON_WIDTH,
                                              3 * Constants.PADDING + Constants.NUM_ROWS * Constants.RECT_HEIGHT + Constants.NEW_GAME_BUTTON_HEIGHT,
                                              Constants.FINISH_ANIMATION_BUTTON_WIDTH, Constants.FINISH_ANIMATION_BUTTON_HEIGHT, 'Finish Animation',
                                              Constants.BLACK, Constants.MENU_FONT_SIZE)

        self.scene.fill(Constants.BLUE)
        self.redraw_screen(-1, -1, Constants.BLUE)


        #time
        self.start_time = pygame.time.get_ticks()
        self.prev_time_seconds = -1
        pygame.display.update()

    #writes text after finish puzzle
    def write_finish_screen_text(self):
        text_width, text_height = self.grid_font.size("Sudoku Solved!")
        finished_label = self.grid_font.render("Sudoku Solved!", True, Constants.BLUE)
        self.scene.blit(finished_label, (Constants.WINDOW_WIDTH // 2 - text_width // 2,
                                         Constants.WINDOW_HEIGHT // 2 - text_height // 2 -
                                         Constants.FINISHED_BUTTON_HEIGHT - Constants.FINISHED_MENU_SPACING))

    #writes the finish time of the program
    def write_finish_time(self, finish_time):
        str_time = "Finished In - "
        if self.curr_time_seconds < 10:
            str_time += "0:0" + str(self.curr_time_seconds)
        elif self.curr_time_seconds < 60:
            str_time +=  "0:" + str(self.curr_time_seconds)
        else:
            minutes = self.curr_time_seconds // 60
            seconds = self.curr_time_seconds % 60
            str_addition = ""
            if seconds < 10:
                str_addition = "0"
            str_time +=  str(minutes) + ":" + str_addition + str(seconds)
        text_width, text_height = self.time_font.size(str_time)
        finished_time_label = self.time_font.render(str_time, True, Constants.BLACK)
        self.scene.blit(finished_time_label, (Constants.WINDOW_WIDTH // 2 - text_width // 2, self.finish_button.y + Constants.FINISHED_MENU_SPACING + Constants.FINISHED_BUTTON_HEIGHT))

    #creates a fading white screen
    def fade(self, color):
        fading_surface = pygame.Surface((Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT))
        fading_surface.fill(color)
        #fades from 0 to 219 alpha
        for a in range(220):
            fading_surface.set_alpha(a)
            self.redraw_screen(-1, -1, Constants.BLUE)
            self.scene.blit(fading_surface, (0, 0))
            pygame.display.update()
            #add delay so it smoothens transition
            pygame.time.delay(5)

    def redraw_screen(self, row, col, color):
        self.scene.fill(Constants.BLUE)
        #time
        self.draw_time_label()
        #grid
        self.draw_grid(row, col)
        #6 (all) buttons redrawn
        self.redraw_buttons()
        #numbers in grid
        self.fill_in_numbers(color)

    #returns whether mouse pressed in the grid
    def is_in_bounds(self, position):
        return position[0] > Constants.PADDING and position[0] < Constants.PADDING + Constants.RECT_WIDTH * Constants.NUM_COLS and position[1] > Constants.PADDING and position[1] < Constants.PADDING + Constants.RECT_WIDTH * Constants.NUM_ROWS

    #creates a 9 x 9 grid where True means that row, col position was given in the initial sudoku puzzle
    def initialize_boolean_board(self):
        #true if part of original board
        self.boolean_board = []
        for row in range(Constants.NUM_ROWS):
            arr = []
            for col in range(Constants.NUM_COLS):
                if self.board[row][col] != 0:
                    arr.append(True)
                else:
                    arr.append(False)
            self.boolean_board.append(arr)

    def update_board_if_key_pressed(self):
        focused_row = self.curr_cell[0]
        focused_col = self.curr_cell[1]
        #if there is a focused row, col and it didn't come with the original grid
        if focused_row != -1 and self.is_changeable(focused_row, focused_col):
            keys = pygame.key.get_pressed()
            #if not taking notes
            if not self.notes_pressed:
                if keys[pygame.K_1] or keys[pygame.K_KP1]:
                    self.board[focused_row][focused_col] = 1
                    #sets notes to blank array
                    self.note_numbers[focused_row][focused_col] = []
                elif keys[pygame.K_2] or keys[pygame.K_KP2]:
                    self.board[focused_row][focused_col] = 2
                    self.note_numbers[focused_row][focused_col] = []
                elif keys[pygame.K_3] or keys[pygame.K_KP3]:
                    self.board[focused_row][focused_col] = 3
                    self.note_numbers[focused_row][focused_col] = []
                elif keys[pygame.K_4] or keys[pygame.K_KP4]:
                    self.board[focused_row][focused_col] = 4
                    self.note_numbers[focused_row][focused_col] = []
                elif keys[pygame.K_5] or keys[pygame.K_KP5]:
                    self.board[focused_row][focused_col] = 5
                    self.note_numbers[focused_row][focused_col] = []
                elif keys[pygame.K_6] or keys[pygame.K_KP6]:
                    self.board[focused_row][focused_col] = 6
                    self.note_numbers[focused_row][focused_col] = []
                elif keys[pygame.K_7] or keys[pygame.K_KP7]:
                    self.board[focused_row][focused_col] = 7
                    self.note_numbers[focused_row][focused_col] = []
                elif keys[pygame.K_8] or keys[pygame.K_KP8]:
                    self.board[focused_row][focused_col] = 8
                    self.note_numbers[focused_row][focused_col] = []
                elif keys[pygame.K_9] or keys[pygame.K_KP9]:
                    self.board[focused_row][focused_col] = 9
                    self.note_numbers[focused_row][focused_col] = []
                elif keys[pygame.K_DELETE] or keys[pygame.K_BACKSPACE]:
                    self.board[focused_row][focused_col] = 0
                    self.note_numbers[focused_row][focused_col] = []

                #need removal for both delete and numbers because changing number could remove it from invalidity
                #remove focused_row from invalid_rows if no longer invalid
                if focused_row in self.invalid_rows and not self.is_row_broken(focused_row):
                    self.invalid_rows.remove(focused_row)
                #remove focused_col from invalid_cols if no longer invalid
                if focused_col in self.invalid_cols and not self.is_col_broken(focused_col):
                    self.invalid_cols.remove(focused_col)
                #remove matrix from invalid_matrices if no longer invalid
                if self.get_matrix_num(focused_row, focused_col) in self.invalid_matrices and not self.is_matrix_broken(focused_row, focused_col):
                    self.invalid_matrices.remove(self.get_matrix_num(focused_row, focused_col))
                #add focused_row to invalid_rows if now invalid
                if self.is_row_broken(focused_row) and focused_row not in self.invalid_rows:
                    self.invalid_rows.append(focused_row)
                #add focused_col to invalid_cols if now invalid
                if self.is_col_broken(focused_col) and focused_col not in self.invalid_cols:
                    self.invalid_cols.append(focused_col)
                #add matrix to invalid_matrices if now invalid
                if self.is_matrix_broken(focused_row, focused_col) and self.get_matrix_num(focused_row, focused_col) not in self.invalid_matrices:
                    self.invalid_matrices.append(self.get_matrix_num(focused_row, focused_col))
            else:
                #taking notes
                if keys[pygame.K_1] or keys[pygame.K_KP1]:
                    if 1 not in self.note_numbers[focused_row][focused_col]:
                        #add 1 to the note_numbers
                        self.note_numbers[focused_row][focused_col].append(1)
                        #set board to blank (0)
                        self.board[focused_row][focused_col] = 0
                elif keys[pygame.K_2] or keys[pygame.K_KP2]:
                    if 2 not in self.note_numbers[focused_row][focused_col]:
                        self.note_numbers[focused_row][focused_col].append(2)
                        self.board[focused_row][focused_col] = 0
                elif keys[pygame.K_3] or keys[pygame.K_KP3]:
                    if 3 not in self.note_numbers[focused_row][focused_col]:
                        self.note_numbers[focused_row][focused_col].append(3)
                        self.board[focused_row][focused_col] = 0
                elif keys[pygame.K_4] or keys[pygame.K_KP4]:
                    if 4 not in self.note_numbers[focused_row][focused_col]:
                        self.note_numbers[focused_row][focused_col].append(4)
                        self.board[focused_row][focused_col] = 0
                elif keys[pygame.K_5] or keys[pygame.K_KP5]:
                    if 5 not in self.note_numbers[focused_row][focused_col]:
                        self.note_numbers[focused_row][focused_col].append(5)
                        self.board[focused_row][focused_col] = 0
                elif keys[pygame.K_6] or keys[pygame.K_KP6]:
                    if 6 not in self.note_numbers[focused_row][focused_col]:
                        self.note_numbers[focused_row][focused_col].append(6)
                        self.board[focused_row][focused_col] = 0
                elif keys[pygame.K_7] or keys[pygame.K_KP7]:
                    if 7 not in self.note_numbers[focused_row][focused_col]:
                        self.note_numbers[focused_row][focused_col].append(7)
                        self.board[focused_row][focused_col] = 0
                elif keys[pygame.K_8] or keys[pygame.K_KP8]:
                    if 8 not in self.note_numbers[focused_row][focused_col]:
                        self.note_numbers[focused_row][focused_col].append(8)
                        self.board[focused_row][focused_col] = 0
                elif keys[pygame.K_9] or keys[pygame.K_KP9]:
                    if 9 not in self.note_numbers[focused_row][focused_col]:
                        self.note_numbers[focused_row][focused_col].append(9)
                        self.board[focused_row][focused_col] = 0
                elif keys[pygame.K_DELETE] or keys[pygame.K_BACKSPACE]:
                    self.note_numbers[focused_row][focused_col] = []
                    self.board[focused_row][focused_col] = 0

            self.redraw_screen(focused_row, focused_col, Constants.BLUE)
            pygame.display.update()

    #selected_row and selected_col is made BEIGE
    def draw_grid(self, selected_row, selected_col):
        #draws 9 boxes in each matrix with Constants.INNER_MATRIX_BORDER_WIDTH
        for row in range(Constants.NUM_ROWS):
            for col in range(Constants.NUM_COLS):
                square_color = Constants.WHITE
                if row == selected_row and col == selected_col:
                    square_color = Constants.BEIGE
                #gray background if came with original grid
                elif self.boolean_board[row][col]:
                    square_color = Constants.GRAY
                #draws the actual rectangle
                pygame.draw.rect(self.scene, square_color,
                [Constants.PADDING + Constants.RECT_WIDTH * col,
                 Constants.PADDING + Constants.RECT_WIDTH * row,
                 Constants.RECT_WIDTH, Constants.RECT_HEIGHT])

                 #draws the outline around it, last argument changes this to just outline
                pygame.draw.rect(self.scene, Constants.BLACK,
                [Constants.PADDING + Constants.RECT_WIDTH * col,
                 Constants.PADDING + Constants.RECT_WIDTH * row,
                 Constants.RECT_WIDTH, Constants.RECT_HEIGHT], Constants.INNER_MATRIX_BORDER_WIDTH)

        #draws 9 box outlines that represent the 9 matrices with Constants.MATRIX_BORDER_WIDTH (the big boxes)
        for row in range(Constants.NUM_ROWS // 3):
            for col in range(Constants.NUM_COLS // 3):
                pygame.draw.rect(self.scene, Constants.BLACK,
                [Constants.PADDING + Constants.RECT_WIDTH * col * 3,
                 Constants.PADDING + Constants.RECT_WIDTH * row * 3,
                 Constants.RECT_WIDTH * 3, Constants.RECT_HEIGHT * 3], Constants.MATRIX_BORDER_WIDTH)

    #returns x given col_num
    def get_x(self, col_num):
        return Constants.PADDING + Constants.RECT_WIDTH * col_num

    #returns y given row_num
    def get_y(self, row_num):
        return Constants.PADDING + Constants.RECT_WIDTH * row_num

    #fills in numbers
    def fill_in_numbers(self, color):
        og_color = color
        for row in range(Constants.NUM_ROWS):
            for col in range(Constants.NUM_COLS):
                #if it's not blank
                if self.board[row][col] != 0:
                    #color is red if anything invalid
                    if row in self.invalid_rows or col in self.invalid_cols or self.get_matrix_num(row, col) in self.invalid_matrices:
                        color = Constants.RED
                    #creates label with grid_font
                    label = self.grid_font.render(str(self.board[row][col]), True, color)
                    #adds label to screen if a number is supposed to go there
                    if self.board[row][col] != 0:
                        self.scene.blit(label, (self.get_x(col) + Constants.RECT_WIDTH // 2 - self.number_width // 2, self.get_y(row) + Constants.RECT_WIDTH // 2 - self.number_height // 2))
                    #resets color to what it is if not invalid
                    color = og_color
                #execute if the row, col position is 0 on the board and there are notes on the note_list
                elif len(self.note_numbers[row][col]) != 0:
                    #upper left corner of row, col
                        x_pos = self.get_x(col)
                        y_pos = self.get_y(row)
                        for number in self.note_numbers[row][col]:
                            label = self.note_font.render(str(number), True, color)
                            #123
                            #456
                            #789
                            x = x_pos
                            y = y_pos

                            #y positioning
                            if number <= 3:
                                y -= Constants.NOTE_OFFSET // 2
                            elif number >= 4 and number <= 6:
                                y += Constants.NOTE_OFFSET * 2 + Constants.NOTE_OFFSET // 2
                            else:
                                y += Constants.NOTE_OFFSET * 5 + Constants.NOTE_OFFSET // 2

                            #x positioning
                            if number % 3 == 1:
                                x += Constants.NOTE_OFFSET
                            elif number % 3 == 2:
                                x += Constants.NOTE_OFFSET * 3 + Constants.NOTE_OFFSET // 2
                            else:
                                x += Constants.NOTE_OFFSET * 6
                            self.scene.blit(label, (x, y))

    #gives row in grid given y
    def get_row(self, y):
        return (y - Constants.PADDING) // Constants.RECT_WIDTH

    #gives col in grid given x
    def get_col(self, x):
        return (x - Constants.PADDING) // Constants.RECT_WIDTH

    #returns whether there are 2 instances of the same number in col_number
    def is_col_broken(self, col_number):
        col_values = []
        for row_number in range(Constants.NUM_ROWS):
            col_values.append(self.board[row_number][col_number])
        #removes all 0's
        while 0 in col_values:
            col_values.remove(0)
        #sets don't contain duplicates so if there are no duplicates, the lengths will be the same and the function returns false
        return len(col_values) != len(set(col_values))

    #returns whether there are 2 instances of the same number in the given matrix
    def is_matrix_broken(self, row_start, col_start):
        row_start = 3 * (row_start // 3)
        col_start = 3 * (col_start // 3)
        matrix_nums = []
        for curr_row in range(row_start, row_start + 3):
            for curr_col in range(col_start, col_start + 3):
                matrix_nums.append(self.board[curr_row][curr_col])
        while 0 in matrix_nums:
            matrix_nums.remove(0)
        return len(matrix_nums) != len(set(matrix_nums))

    #returns whether there are 2 instances of the same number in col_number
    def is_row_broken(self, row_number):
        original_row_values = self.board[row_number]
        row_values = original_row_values.copy()
        while 0 in row_values:
            row_values.remove(0)
        return len(row_values) != len(set(row_values))

    #returns if it didn't come in the original sudoku puzzle
    def is_changeable(self, row, col):
        return not self.boolean_board[row][col]

    #returns the matrix_number given row, col
    # 0  is upper left corner, 1 is upper top ,  2 is upper right corner
    # 3                        4                 5
    # 6                        7                 8
    def get_matrix_num(self, row, col):
        matrix_row = row // 3
        matrix_col = col // 3
        if matrix_row == 0 and matrix_col == 0:
            return 0
        elif matrix_row == 0 and matrix_col == 1:
            return 1
        elif matrix_row == 0 and matrix_col == 2:
            return 2
        elif matrix_row == 1 and matrix_col == 0:
            return 3
        elif matrix_row == 1 and matrix_col == 1:
            return 4
        elif matrix_row == 1 and matrix_col == 2:
            return 5
        elif matrix_row == 2 and matrix_col == 0:
            return 6
        elif matrix_row == 2 and matrix_col == 1:
            return 7
        elif matrix_row == 2 and matrix_col == 2:
            return 8

    #returns whether the board is solved
    def is_board_solved(self):
        #no duplicates in rows
        for row in range(Constants.NUM_ROWS):
            curr_row = self.board[row]
            if 0 in curr_row:
                return False
            elif self.is_row_broken(row):
                return False
        #no duplicates in cols
        for col in range(Constants.NUM_COLS):
            if self.is_col_broken(col):
                return False
        #no duplicates in matrices
        for row in range(0, Constants.NUM_ROWS, 3):
            for col in range(0, Constants.NUM_COLS, 3):
                if self.is_matrix_broken(row, col):
                    return False
        return True

def main():
    driver = Controller()

if __name__ == "__main__":
    main()
