from load_grid import LoadSudokuGrid
from visualize_results import Visualize
from sudoku_solver import SudokuSolver
import numpy as np

if __name__ == '__main__':
    user_grid = LoadSudokuGrid().grid
    if user_grid is not None:
        solved_grid = SudokuSolver(np.array([[element for element in row] for row in user_grid])).solve_grid()

    if solved_grid is not None:
        Visualize(solved_grid, user_grid).show_solution()
