# Interactive-Sudoku-Solver
This is a graphical user interface where users can play Sudoku. Additionally, users have to ability to make the program automatically solve the board using a Sudoku solving backtracking algorithm; this algorithm is shown step-by-step so that users can understand and picture how it works. This was built with Python and the Pygame module. To run it, run python3 Controller.py.

## Basic Controls on the User Interface

- When the user clicks on a cell, it becomes a teal color and is now the focused cell where numbers can be placed.

- The cells with a light gray background are the clues given in the original board that cannot be altered.

- Numbers are added to the focused cell using the keyboard. If the added number is a duplicate in a row, column, or matrix, the numbers in the row, column, or matrix, respectively, will turn red. Otherwise, the numbers will remain purple.

- In this example, adding 2 in the 2nd row and 1st column breaks the row, column, and matrix, so the numbers in the row, column, and matrix all turn red.

- The Clear Board button clears user markings from the board.

<p align = "center">
  <img src = "https://user-images.githubusercontent.com/63945057/88468122-f25e4480-ce93-11ea-92e3-b90654477014.gif" width = 259 height = 300>
</p>  


- The Show Solution button shows the solution to the sudoku puzzle without the backtracking animation being included.

<p align = "center">
  <img src = "https://user-images.githubusercontent.com/63945057/88468190-b5468200-ce94-11ea-83ad-67d557e88bd7.gif" width = 259 height = 300>
</p>  

- The New Puzzle button generates a new Sudoku puzzle.

- The Notes button can be pressed so that when the user clicks a cell and adds a number, they can add multiple numbers to the same cell as possible cell candidates. When the Notes button is not pressed, only one number can be placed in a cell.

<p align = "center">
  <img src = "https://user-images.githubusercontent.com/63945057/88468203-f9d21d80-ce94-11ea-9661-46228bd20f0a.gif" width = 259 height = 300>
</p>  

- The Solve with Backtracking Animation button can be selected so that the program will automatically solve the board for the user using a Sudoku solving backtracking algorithm. Users are able to see how the algorithm works and backtracks as it is being animated.

<p align = "center">
  <img src = "https://user-images.githubusercontent.com/63945057/88468872-5e45aa80-ce9e-11ea-8504-10c047c03d20.gif" width = 259 height = 300>
</p>  

- The Finish Animation button can be selected so that the backtracking animation from the Solve with Backtracking Animation button ends instantly and the board is immediately solved. This button is intended to be used when the backtracking animation takes a long amount of time because a Sudoku puzzle is particularly difficult for the backtracking algorithm to solve.

<p align = "center">
  <img src = "https://user-images.githubusercontent.com/63945057/88468319-8c26f100-ce96-11ea-8bf0-5885e15ec023.gif" width = 259 height = 300>
</p>  

