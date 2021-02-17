import matplotlib.pyplot as plt
import numpy as np


class Visualize:
    def __init__(self, solved_grid, old_grid):
        self.solved_grid = solved_grid
        self.old_grid = old_grid

    def show_solution(self, cell_dimension=0.1):
        cell_text = [[str(el) for el in row] for row in self.solved_grid]
        final_grid = plt.table(cell_text, loc='center', rowLoc='center', colLoc='center', cellLoc='center')

        cell_dict = final_grid.get_celld()
        for i in range(len(self.solved_grid)):
            for j in range(len(self.solved_grid[i])):
                cell_dict[(i, j)].set_height(cell_dimension)
                cell_dict[(i, j)].set_width(cell_dimension)
                if not self.old_grid[i, j]:
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
