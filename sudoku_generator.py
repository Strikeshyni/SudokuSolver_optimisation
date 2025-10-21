import random

def generate_sudoku(size):
    """
    Génère une grille Sudoku complète de taille size x size,
    où size doit être un carré parfait (ex : 4, 9, 16, 25...)
    """
    n = int(size**0.5)  # Taille d’un bloc

    if n * n != size:
        raise ValueError("size doit être un carré parfait : 4, 9, 16, 25, ...")

    # Grille vide
    board = [[0]*size for _ in range(size)]

    # Formule de génération en décalage
    for r in range(size):
        for c in range(size):
            board[r][c] = (r*n + r//n + c) % size + 1

    # Mélanges aléatoires pour éviter une grille trop régulière
    shuffle_board(board, n)

    return board

def shuffle_board(board, n):
    size = len(board)

    def swap_rows(r1, r2):
        board[r1], board[r2] = board[r2], board[r1]

    def swap_cols(c1, c2):
        for row in board:
            row[c1], row[c2] = row[c2], row[c1]

    # Mélanger les lignes dans chaque bloc
    for block in range(n):
        rows = list(range(block*n, block*n + n))
        random.shuffle(rows)
        for i in range(n):
            swap_rows(block*n + i, rows[i])

    # Mélanger les colonnes dans chaque bloc
    for block in range(n):
        cols = list(range(block*n, block*n + n))
        random.shuffle(cols)
        for i in range(n):
            swap_cols(block*n + i, cols[i])

    # Mélanger les blocs de lignes
    blocks = list(range(n))
    random.shuffle(blocks)
    for i in range(n):
        for k in range(n):
            swap_rows(i*n + k, blocks[i]*n + k)

    # Mélanger les blocs de colonnes
    blocks = list(range(n))
    random.shuffle(blocks)
    for i in range(n):
        for k in range(n):
            swap_cols(i*n + k, blocks[i]*n + k)

def mask_grid(grid, percentage):
    """
    Met des 0 dans la grille selon un pourcentage donné.
    percentage = entre 0 et 1 (ex : 0.5 pour 50% de cases masquées)
    """
    size = len(grid)
    total_cells = size * size
    cells_to_mask = int(total_cells * percentage)

    flat_positions = [(r, c) for r in range(size) for c in range(size)]
    random.shuffle(flat_positions)

    for i in range(cells_to_mask):
        r, c = flat_positions[i]
        grid[r][c] = 0

    return grid

def print_board(board):
    for row in board:
        print(" ".join(str(x) for x in row))

def save_grid_to_file(filename, grid):
    with open(filename, 'a') as f:
        f.write("\nGrid 00\n")
        for row in grid:
            f.write(" ".join(str(x) for x in row) + "\n")
        f.write("\n")

# Exemple d'utilisation
if __name__ == "__main__":
    filename = "sudoku_grids_16.txt"
    size = 16
    percentage = 0.7  # 50% des cases masquées

    grid = generate_sudoku(size)
    print("Grille complète :")
    print_board(grid)

    masked = mask_grid([row[:] for row in grid], percentage)  # copie sécurisée

    print("\nGrille incomplète :")
    print_board(masked)

    save_grid_to_file(filename, masked)