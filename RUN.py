from Main import SudokuSolver, LoadSudokuGrid

if __name__ == '__main__':
    user_grid = LoadSudokuGrid().get_user_grid()
    if user_grid is not None:
        SudokuSolver(user_grid).main()
