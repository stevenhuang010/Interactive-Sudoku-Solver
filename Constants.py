#colors
BLACK = (0,0,0)
WHITE = (255, 255, 255)
BLUE = (120, 193, 245)
PURPLE = (186, 85, 201)
GREEN = (133, 222, 185)
RED = (245, 71, 71)
GRAY = (209, 204, 199)
#rect width and height in the grid
RECT_WIDTH = 40
RECT_HEIGHT = 40
#padding around the grid and for the buttons
PADDING = 5
NUM_ROWS = 9
NUM_COLS = 9
#outer matrix border width (thicker boxes)
MATRIX_BORDER_WIDTH = 3
#thin lines between boxes in grid
INNER_MATRIX_BORDER_WIDTH = 1

WINDOW_WIDTH = RECT_WIDTH * NUM_COLS + 2 * PADDING
#height of the menu below the grid
MENU_HEIGHT = 65

WINDOW_HEIGHT = RECT_HEIGHT * NUM_ROWS + 2 * PADDING + MENU_HEIGHT

#button that shows after finishing puzzle
FINISHED_BUTTON_WIDTH = 110
FINISHED_BUTTON_HEIGHT = 30
#New puzzle button on main screen
NEW_GAME_BUTTON_WIDTH = 80
NEW_GAME_BUTTON_HEIGHT = 25
#clear board button on main screen
CLEAR_BOARD_BUTTON_WIDTH = 80
CLEAR_BOARD_BUTTON_HEIGHT = 25
#show solution button on main screen
SOLVE_BUTTON_WIDTH = 100
SOLVE_BUTTON_HEIGHT = 25
#notes button on main main screen
NOTES_BUTTON_WIDTH = 40
NOTES_BUTTON_HEIGHT = 25
#backtracking animation button on main screen
BACKTRACKING_BUTTON_WIDTH = 240
BACKTRACKING_BUTTON_HEIGHT = 25
#finish animation button on main screen
FINISH_ANIMATION_BUTTON_WIDTH = 115
FINISH_ANIMATION_BUTTON_HEIGHT = 25
#font size of the menu items
MENU_FONT_SIZE = 11
#spacing of the items on the finished screen
FINISHED_MENU_SPACING = 20
#font size of notes on Board
NOTE_FONT_SIZE = 13
#controls offset in between notes in the same cell
NOTE_OFFSET = 4
