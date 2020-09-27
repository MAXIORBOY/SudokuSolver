import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox


class LoadSudokuGrid:
    def __init__(self, file_name='sudoku.txt'):
        self.file_name = file_name
        self.grid = self.load_data_from_text_file()

    def load_data_from_text_file(self):
        root = tk.Tk()
        root.withdraw()
        try:
            f = open(self.file_name, 'r')
        except:
            messagebox.showerror('Error!', 'Unable to open ' + self.file_name + ' file!\nThe file was renamed, moved or deleted!')
            return None

        grid = f.read().split('\n')

        if not self.check_user_input_correctness(grid):
            messagebox.showerror('Error!', 'Your Sudoku grid is incorrect!\nThe grid size is wrong and/or the grid contains a forbidden character!')
            return None

        f.close()

        return [[int(el) for el in row] for row in grid]

    @staticmethod
    def check_user_input_correctness(grid):
        valid_characters = [str(number) for number in range(10)]
        if len(grid) == 9:
            for i in range(len(grid)):
                if len(grid[i]) != 9:
                    return False
                for j in range(len(grid[i])):
                    if grid[i][j] not in valid_characters:
                        return False
        else:
            return False

        return True

    def get_user_grid(self):
        return self.grid


class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid
        self.old_grid = None
        self.possible_numbers_in_the_field_list = None

    def set_old_grid(self):
        self.old_grid = [[el for el in row] for row in self.grid]

    @staticmethod
    def internal_square_index_position(index_table):
        for i in range(len(index_table)):
            if index_table[i] < 3:
                index_table[i] = 0
            elif index_table[i] < 6:
                index_table[i] = 3
            else:
                index_table[i] = 6

        return index_table

    def possible_numbers_in_the_field(self):
        possible_numbers_in_the_field_list = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j]:
                    continue
                used_numbers = []
                used_numbers.append(self.grid[i])

                row = []
                for k in range(len(self.grid)):
                    row.append(self.grid[k][j])
                used_numbers.append(row)

                internal_square_begin_index = (self.internal_square_index_position([i, j]))
                for k in range(3):
                    used_numbers.append(self.grid[internal_square_begin_index[0] + k][internal_square_begin_index[1]:internal_square_begin_index[1] + 3])

                used_numbers = [el for row in used_numbers for el in row]
                possible_numbers_in_the_field_list.append([number for number in [1, 2, 3, 4, 5, 6, 7, 8, 9] if number not in used_numbers])

        return possible_numbers_in_the_field_list

    def locate_field_with_only_one_possibility(self):
        for i in range(len(self.possible_numbers_in_the_field_list)):
            if len(self.possible_numbers_in_the_field_list[i]) == 1:
                return i

        return -1

    def change_number_on_the_grid(self, number, empty_field_index):
        counter = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 0:
                    counter += 1
                if counter == empty_field_index + 1:
                    self.grid[i][j] = number
                    return

    def check_if_grid_is_possible_to_solve(self):
        for i in range(len(self.possible_numbers_in_the_field_list)):
            if not len(self.possible_numbers_in_the_field_list[i]):
                return False

        return True

    def locate_the_field_with_the_lowest_amount_of_possibilities(self):
        minimum_index, minimum = 0, 10
        for i in range(len(self.possible_numbers_in_the_field_list)):
            if len(self.possible_numbers_in_the_field_list[i]) < minimum:
                minimum = len(self.possible_numbers_in_the_field_list[i])
                minimum_index = i

        return minimum_index

    def main(self):
        root = tk.Tk()
        root.withdraw()
        if self.grid is not None:
            self.set_old_grid()
        else:
            messagebox.showerror('Error!', 'Invalid grid!')
            return None

        loop_status = True
        array_backup, assumption_index_backup, assumption_backup = [], [], []

        while loop_status:
            try:
                self.possible_numbers_in_the_field_list = self.possible_numbers_in_the_field()
                loop_status = bool(len(self.possible_numbers_in_the_field_list))
                if loop_status:
                    if self.check_if_grid_is_possible_to_solve():
                        if self.locate_field_with_only_one_possibility() >= 0:
                            min_index = self.locate_field_with_only_one_possibility()
                            self.change_number_on_the_grid(self.possible_numbers_in_the_field_list[min_index][0], min_index)
                        else:
                            array_backup.append([[el for el in row] for row in self.grid])
                            assumption_index_backup.append(self.locate_the_field_with_the_lowest_amount_of_possibilities())
                            assumption_backup.append(self.possible_numbers_in_the_field_list[self.locate_the_field_with_the_lowest_amount_of_possibilities()])
                            self.change_number_on_the_grid(assumption_backup[-1][0], assumption_index_backup[-1])
                    else:
                        del assumption_backup[-1][0]
                        if len(assumption_backup[-1]):
                            self.grid = array_backup[-1]
                            self.change_number_on_the_grid(assumption_backup[-1][0], assumption_index_backup[-1])
                        else:
                            loop_status2 = True
                            while loop_status2:
                                del assumption_backup[-1]
                                del assumption_backup[-1][0]
                                del assumption_index_backup[-1]
                                del array_backup[-1]
                                loop_status2 = not (bool(len(assumption_backup[-1])))

                            self.grid = array_backup[-1]
                            self.change_number_on_the_grid(assumption_backup[-1][0], assumption_index_backup[-1])
            except:
                messagebox.showerror('Error!', 'The clues, given in your Sudoku grid, are incorrect!\n')
                return None

        return self.format_output()

    def format_output(self, cell_dimension=0.1):
        cell_text = [[str(el) for el in row] for row in self.grid]
        final_grid = plt.table(cell_text, loc='center', rowLoc='center', colLoc='center', cellLoc='center')

        cell_dict = final_grid.get_celld()
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                cell_dict[(i, j)].set_height(cell_dimension)
                cell_dict[(i, j)].set_width(cell_dimension)
                if not self.old_grid[i][j]:
                    cell_dict[(i, j)].get_text().set_color('blue')
                else:
                    cell_dict[(i, j)].get_text().set_color('black')

        final_grid.auto_set_font_size(False)
        final_grid.set_fontsize(20)
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        for i in range(4):
            ax.axhline(xmin=cell_dimension / 2, xmax=1 - cell_dimension / 2, y=3 * i * cell_dimension + cell_dimension / 2, linewidth=3, color='black')
            ax.axvline(ymin=cell_dimension / 2, ymax=1 - cell_dimension / 2, x=3 * i * cell_dimension + cell_dimension / 2, linewidth=3, color='black')

        plt.box(on=None)
        plt.show()
