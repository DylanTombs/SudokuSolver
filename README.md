# Sudoku Solver

A Sudoku solver written in Python using NumPy, pencil marking, and depth-first search with backtracking. It models the puzzle as a grid of custom `Cell` objects, narrows down possible values using constraint propagation, and solves efficiently with DFS.

## Features

- Solves standard 9x9 Sudoku puzzles
- Uses **pencil marks** to track possible values for each cell
- Employs **depth-first search** with **backtracking** to explore solutions
- Uses **NumPy** arrays for efficient grid operations
- Object-oriented design with custom `Cell` and `partialSudoku` classes

## How It Works

1. **Pencil Marking:**  
   Initial values in the puzzle are used to eliminate impossible values from related cells (row, column, and square).

2. **DFS Solving:**  
   The solver recursively selects the cell with the fewest possibilities and attempts each, backtracking if a dead-end is reached.

3. **Goal Check:**  
   Once all cells are filled with valid values, the final Sudoku is returned.

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/sudoku-solver.git
   cd sudoku-solver

