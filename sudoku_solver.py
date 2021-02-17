import random
import numpy as np
import tkinter as tk
from tkinter import messagebox

class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid
        self.possible_digits_in_fields_dictionary = None
        self.number_of_assumptions = 0

    @staticmethod
    def get_bounds_of_corresponding_3x3_square(row_index, column_index):
        row_value = row_index // 3
        column_value = column_index // 3

        return 3 * row_value, 3 * (row_value + 1), 3 * column_value, 3 * (column_value + 1)

    def get_possible_digits_in_fields(self):
        possible_digits_in_fields_dictionary = {}

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j]:
                    continue

                used_digits = []

                used_digits.append([digit for digit in self.grid[i] if digit])
                used_digits.append([digit for digit in self.grid[:, j] if digit])
                row_lower_bound, row_upper_bound, column_lower_bound, column_upper_bound = self.get_bounds_of_corresponding_3x3_square(i, j)
                square_3x3_digits = [digit for square in self.grid[row_lower_bound:row_upper_bound, column_lower_bound:column_upper_bound] for digit in square if digit]
                for row in square_3x3_digits:
                    used_digits.append([row])

                used_digits = [el for row in used_digits for el in row]
                possible_digits_in_fields_dictionary[(i, j)] = tuple([number for number in list(range(1, 10)) if number not in used_digits])

        return possible_digits_in_fields_dictionary

    def check_if_grid_is_possible_to_solve(self):
        for field_coords in self.possible_digits_in_fields_dictionary:
            if not len(self.possible_digits_in_fields_dictionary[field_coords]):
                return False

        return True

    def get_coords_of_fields_with_the_lowest_amount_of_possibilities(self):
        amount_of_possibilities = []
        for key in self.possible_digits_in_fields_dictionary:
            amount_of_possibilities.append(len(self.possible_digits_in_fields_dictionary[key]))

        minimum_amount_of_possibilities = min(amount_of_possibilities)
        dictionary = dict(zip(list(self.possible_digits_in_fields_dictionary.keys()), amount_of_possibilities))

        return [coords_with_minimum_amount_of_possibilities for coords_with_minimum_amount_of_possibilities in list(dictionary.keys()) if dictionary[coords_with_minimum_amount_of_possibilities] == minimum_amount_of_possibilities], minimum_amount_of_possibilities

    def pick_random_digit_index_from_possibilities(self, coords):
        return random.choice(list(range(len(self.possible_digits_in_fields_dictionary[coords]))))

    def solve_grid(self):
        loop_status = True
        grid_backup, coord_assumptions_backup, digit_index_assumptions_backup, possibilities_backup = [], [], [], []

        while loop_status:
            self.possible_digits_in_fields_dictionary = self.get_possible_digits_in_fields()
            if not len(self.possible_digits_in_fields_dictionary.keys()):  # end condition
                break

            if self.check_if_grid_is_possible_to_solve():  # check if the grid is still solvable
                coords_of_fields_with_the_lowest_amount_of_possibilities, minimum_amount_of_possibilities = self.get_coords_of_fields_with_the_lowest_amount_of_possibilities()
                coords_of_field_with_the_lowest_amount_of_possibilities = random.choice(coords_of_fields_with_the_lowest_amount_of_possibilities)
                digit_index = self.pick_random_digit_index_from_possibilities(coords_of_field_with_the_lowest_amount_of_possibilities)

                if minimum_amount_of_possibilities > 1:  # make an assumption
                    grid_backup.append(np.array([[element for element in row] for row in self.grid]))
                    coord_assumptions_backup.append(coords_of_field_with_the_lowest_amount_of_possibilities)
                    digit_index_assumptions_backup.append(digit_index)
                    possibilities_backup.append([element for element in self.possible_digits_in_fields_dictionary[coords_of_field_with_the_lowest_amount_of_possibilities]])

                self.grid[coords_of_field_with_the_lowest_amount_of_possibilities] = self.possible_digits_in_fields_dictionary[coords_of_field_with_the_lowest_amount_of_possibilities][digit_index]

            else:  # wrong assumption - rollback
                del possibilities_backup[-1][digit_index_assumptions_backup[-1]]

                loop_status2 = True
                while loop_status2:
                    if len(possibilities_backup[-1]):
                        digit_index_assumptions_backup[-1] = random.choice(list(range(len(possibilities_backup[-1]))))
                        break
                    else:  # deep rollback
                        del possibilities_backup[-1]
                        del digit_index_assumptions_backup[-1]
                        del grid_backup[-1]
                        del coord_assumptions_backup[-1]

                        try:
                            del possibilities_backup[-1][digit_index_assumptions_backup[-1]]
                        except:
                            root = tk.Tk()
                            root.withdraw()
                            messagebox.showerror('Error!', 'The clues, given in your Sudoku grid, are incorrect!\n')
                            root.destroy()
                            return None

                self.grid = np.array([[element for element in row] for row in grid_backup[-1]])
                self.grid[coord_assumptions_backup[-1]] = possibilities_backup[-1][digit_index_assumptions_backup[-1]]

        self.number_of_assumptions = len(coord_assumptions_backup)

        return self.grid
