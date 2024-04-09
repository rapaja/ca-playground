"""Game of Schools (GoS) module"""

import numpy as np


def game_of_schools(grid):
    # Padding the grid to handle edge cells
    padded_grid = np.pad(grid, pad_width=1, mode="constant", constant_values=0)
    new_grid = np.zeros(grid.shape, dtype=int)

    for i in range(1, padded_grid.shape[0] - 1):
        for j in range(1, padded_grid.shape[1] - 1):
            # Summing all eight neighbors
            total = (
                np.sum(padded_grid[i - 1 : i + 2, j - 1 : j + 2]) - padded_grid[i, j]
            )

            # Applying Conway's Game of Life Rules
            if padded_grid[i, j] == 1:
                if total < 2 or total > 3:
                    new_grid[i - 1, j - 1] = 0
                else:
                    new_grid[i - 1, j - 1] = 1
            else:
                if total == 3:
                    new_grid[i - 1, j - 1] = 1

    return new_grid


def deki_rule_1(grid):
    padded_grid = np.pad(grid, pad_width=1, mode="constant", constant_values=0)
    new_grid = np.zeros(grid.shape, dtype=int)
