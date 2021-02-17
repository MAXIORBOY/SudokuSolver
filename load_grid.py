import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import messagebox
import random


class LoadSudokuGrid:
    def __init__(self, file_name='sudoku.txt'):
        self.file_name = file_name
        self.grid = self.load_data_from_text_file()

    def load_data_from_text_file(self):
        try:
            f = open(self.file_name, 'r')
        except:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror('Error!', 'Unable to open ' + self.file_name + ' file!\nThe file was renamed, moved or deleted!')
            root.destroy()
            return None

        grid = f.read().split('\n')

        if not self.check_user_input_correctness(grid):
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror('Error!', 'Your Sudoku grid is incorrect!\nThe grid size is wrong and/or the grid contains a forbidden character!')
            root.destroy()
            return None

        f.close()

        return np.array([[int(el) for el in row] for row in grid])

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
