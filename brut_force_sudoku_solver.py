import math
import time

class SudokuSolver:
    def __init__(self, board):
        self.board = board
        self.board_size = len(board)
        self.box_size = int(math.sqrt(self.board_size))

    def solve_sudoku(self):
        empty = self.find_empty_location()
        if not empty:
            return True
        row, col = empty

        for num in range(1, self.board_size + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num

                if self.solve_sudoku():
                    return True

                self.board[row][col] = 0  # Backtrack
        return False

    def find_empty_location(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self, row, col, num):
        # Check if num is not in the given row
        for x in range(self.board_size):
            if self.board[row][x] == num:
                return False

        # Check if num is not in the given column
        for x in range(self.board_size):
            if self.board[x][col] == num:
                return False

        # Check if num is not in the 3x3 box
        start_row = row - row % self.box_size
        start_col = col - col % self.box_size
        for i in range(self.box_size):
            for j in range(self.box_size):
                if self.board[i + start_row][j + start_col] == num:
                    return False
        return True
    
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

            # When 9 rows are collected, store the grid and start a new one
            if len(current_grid) == grid_size:
                grids.append(current_grid)
                current_grid = []

    return grids

sudoku_size = 25
all_grids_9 = load_sudoku_grids(f"sudoku_grids_{sudoku_size}.txt", sudoku_size)
t_start_all = time.time()
for idx, grid in enumerate(all_grids_9):
    sudoku = SudokuSolver(grid)

    print(f"{idx+1} Original Sudoku:")
    sudoku.print_board()
    t_start = time.time()
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