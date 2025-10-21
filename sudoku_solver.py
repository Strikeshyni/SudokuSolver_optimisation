import math
import time
from collections import defaultdict

class SudokuSolver:
    def __init__(self, board):
        self.board = board
        self.board_size = len(board)
        self.box_size = int(math.sqrt(self.board_size))
        self.row_possibility = [defaultdict(int) for _ in range(self.board_size)]
        self.col_possibility = [defaultdict(int) for _ in range(self.board_size)]
        self.box_possibility = [defaultdict(int) for _ in range(self.board_size)]
        for num in range(1, self.board_size + 1):
            for row in range(self.board_size):
                if num not in self.board[row]:
                    self.row_possibility[row][num] = 1

            for col in range(self.board_size):
                is_in_col = False
                for row in range(self.board_size):
                    if self.board[row][col] == num:
                        is_in_col = True
                        break
                if not is_in_col:
                    self.col_possibility[col][num] = 1

            for box in range(self.board_size):
                start_row = (box // self.box_size) * self.box_size
                start_col = (box % self.box_size) * self.box_size

                found = False
                for r in range(start_row, start_row + self.box_size):
                    for c in range(start_col, start_col + self.box_size):
                        if self.board[r][c] == num:
                            found = True
                            break
                    if found:
                        break

                if not found:
                    self.box_possibility[box][num] = 1

    def solve_sudoku(self):
        empty = self.find_best_empty()
        if not empty:
            return True
        row, col = empty

        for num in range(1, self.board_size + 1):
            if self.is_valid(row, col, num):
                self.place_number(row, col, num)

                if self.solve_sudoku():
                    return True

                self.remove_number(row, col, num)
        return False

    def find_empty_dummy(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def find_best_empty(self):
        best = None
        min_poss = float('inf')

        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board[r][c] == 0:
                    box = (r // self.box_size) * self.box_size + (c // self.box_size)
                    count = sum(
                        self.row_possibility[r][n] and self.col_possibility[c][n] and self.box_possibility[box][n]
                        for n in range(1, self.board_size + 1)
                    )
                    if count < min_poss:
                        min_poss = count
                        best = (r, c)

        return best


    def is_valid(self, row, col, num):
        box = (row // self.box_size) * self.box_size + (col // self.box_size)
        return (
            self.row_possibility[row].get(num, 0) == 1 and
            self.col_possibility[col].get(num, 0) == 1 and
            self.box_possibility[box].get(num, 0) == 1
        )

    def place_number(self, row, col, num):
        self.board[row][col] = num
        box = (row // self.box_size) * self.box_size + (col // self.box_size)
        self.row_possibility[row][num] = 0
        self.col_possibility[col][num] = 0
        self.box_possibility[box][num] = 0

    def remove_number(self, row, col, num):
        self.board[row][col] = 0
        box = (row // self.box_size) * self.box_size + (col // self.box_size)
        self.row_possibility[row][num] = 1
        self.col_possibility[col][num] = 1
        self.box_possibility[box][num] = 1

    def print_board(self):
        # Determine the max width of any number or dot
        max_width = max(
            len(str(num)) for row in self.board for num in row
        )
        dot = ".".rjust(max_width)

        # Build horizontal separator based on box size and max width
        sep = "|" + "+".join(["-" * ((self.box_size * (max_width + 1)) + 1)] * self.box_size) + "|"

        for i, row in enumerate(self.board):
            row_str = "| "
            for j, num in enumerate(row):
                cell = (str(num) if num != 0 else dot).rjust(max_width)
                row_str += cell + " "
                if (j + 1) % self.box_size == 0:
                    row_str += "| "
            print(row_str)

            if (i + 1) % self.box_size == 0 and i != self.board_size - 1:
                print(sep)



def load_sudoku_grids(filename, grid_size):
    grids = []
    current_grid = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()

            # Skip empty lines or "Grid XX" headers
            if not line or line.startswith("Grid"):
                continue

            # Convert a character string like "0 0 3 0 2 0 6 0 0" into [0,0,3,0,2,0,6,0,0]
            row = []
            for row_str in line.split(' '):
                row.append(int(row_str))
            current_grid.append(row)

            # When grid is collected, store the grid and start a new one
            if len(current_grid) == grid_size:
                grids.append(current_grid)
                current_grid = []

    return grids

sudoku_size = 16
sudoku_dir = "sudoku_grids/"
file_path = f"{sudoku_dir}sudoku_grids_16.txt"
all_grids_9 = load_sudoku_grids(file_path, sudoku_size)
t_start_all = time.time()
for idx, grid in enumerate(all_grids_9):
    t_start = time.time()

    sudoku = SudokuSolver(grid)
    print(f"{idx+1} Original Sudoku:")
    sudoku.print_board()
    if sudoku.solve_sudoku():
        duration = time.time() - t_start
        print(f"{idx+1} Solved Sudoku:")
        sudoku.print_board()
    else:
        duration = time.time() - t_start
        print(f"{idx+1} No solution exists")
    print(f"Completion in {duration*1000}ms\n")

full_duration = time.time() - t_start_all
print(f"Full duration = {full_duration}s")