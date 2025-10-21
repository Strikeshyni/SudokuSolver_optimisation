import streamlit as st
import math
import time
from collections import defaultdict
import copy
import os
from pathlib import Path

class SudokuSolver:
    def __init__(self, board, track_steps=False):
        self.board = board
        self.board_size = len(board)
        self.box_size = int(math.sqrt(self.board_size))
        self.row_possibility = [defaultdict(int) for _ in range(self.board_size)]
        self.col_possibility = [defaultdict(int) for _ in range(self.board_size)]
        self.box_possibility = [defaultdict(int) for _ in range(self.board_size)]
        self.track_steps = track_steps
        self.steps = []
        self.backtrack_count = 0
        self.cells_filled = 0
        
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
                self.cells_filled += 1
                
                if self.track_steps and len(self.steps) < 50:
                    self.steps.append({
                        'board': copy.deepcopy(self.board),
                        'row': row,
                        'col': col,
                        'num': num,
                        'action': 'place'
                    })

                if self.solve_sudoku():
                    return True

                self.remove_number(row, col, num)
                self.backtrack_count += 1
                
                if self.track_steps and len(self.steps) < 50:
                    self.steps.append({
                        'board': copy.deepcopy(self.board),
                        'row': row,
                        'col': col,
                        'num': num,
                        'action': 'remove'
                    })
        return False

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


def display_sudoku_grid(board, title="Sudoku Grid", highlight_cell=None):
    """Display a beautiful Sudoku grid with CSS styling"""
    board_size = len(board)
    box_size = int(math.sqrt(board_size))
    
    # Determine cell size based on board size
    cell_size = 45 if board_size <= 9 else 35 if board_size <= 16 else 25
    font_size = 18 if board_size <= 9 else 14 if board_size <= 16 else 10
    
    st.markdown(f"### {title}")
    
    # CSS for the grid
    grid_html = f"""
    <style>
        .sudoku-grid {{
            display: inline-block;
            border: 3px solid #2c3e50;
            background: #ecf0f1;
            padding: 5px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .sudoku-row {{
            display: flex;
            margin: 0;
            padding: 0;
        }}
        .sudoku-cell {{
            width: {cell_size}px;
            height: {cell_size}px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid #bdc3c7;
            font-size: {font_size}px;
            font-weight: bold;
            font-family: 'Courier New', monospace;
        }}
        .sudoku-cell.empty {{
            background: #ffffff;
            color: #95a5a6;
        }}
        .sudoku-cell.filled {{
            background: #3498db;
            color: white;
        }}
        .sudoku-cell.highlight {{
            background: #e74c3c;
            color: white;
            animation: pulse 0.5s;
        }}
        .sudoku-cell.box-border-right {{
            border-right: 2px solid #2c3e50;
        }}
        .sudoku-cell.box-border-bottom {{
            border-bottom: 2px solid #2c3e50;
        }}
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
        }}
    </style>
    <div class="sudoku-grid">
    """
    
    for i, row in enumerate(board):
        grid_html += '<div class="sudoku-row">'
        for j, num in enumerate(row):
            classes = ["sudoku-cell"]
            
            if num == 0:
                classes.append("empty")
                display_num = "·"
            else:
                classes.append("filled")
                display_num = str(num)
            
            if highlight_cell and highlight_cell == (i, j):
                classes.append("highlight")
            
            if (j + 1) % box_size == 0 and j < board_size - 1:
                classes.append("box-border-right")
            
            if (i + 1) % box_size == 0 and i < board_size - 1:
                classes.append("box-border-bottom")
            
            grid_html += f'<div class="{" ".join(classes)}">{display_num}</div>'
        
        grid_html += '</div>'
    
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)


def parse_sudoku_file(file_content):
    """Parse a sudoku file and extract all grids with their metadata"""
    grids_data = []
    lines = file_content.strip().split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for Grid header
        if line.startswith("Grid"):
            grid_name = line
            current_grid = []
            i += 1
            
            # Collect grid rows
            while i < len(lines):
                line = lines[i].strip()
                
                # Stop if we hit another Grid header or empty line after collecting some rows
                if line.startswith("Grid") or (not line and current_grid):
                    break
                
                # Skip empty lines before grid starts
                if not line:
                    i += 1
                    continue
                
                # Parse the row
                try:
                    row = [int(x) for x in line.split()]
                    current_grid.append(row)
                    i += 1
                except ValueError:
                    # Skip invalid lines
                    i += 1
                    continue
            
            # Validate and add grid
            if current_grid and len(current_grid) > 0:
                grid_size = len(current_grid)
                # Check if it's a valid square grid
                if all(len(row) == grid_size for row in current_grid):
                    # Check if it's a valid sudoku size (perfect square)
                    box_size = int(math.sqrt(grid_size))
                    if box_size * box_size == grid_size:
                        grids_data.append({
                            'name': grid_name,
                            'grid': current_grid,
                            'size': grid_size
                        })
        else:
            i += 1
    
    return grids_data


def load_grids_from_directory(directory_path):
    """Load all sudoku grids from all .txt files in a directory"""
    all_grids = []
    
    if not os.path.exists(directory_path):
        return all_grids
    
    # Get all .txt files
    txt_files = sorted([f for f in os.listdir(directory_path) if f.endswith('.txt')])
    
    for filename in txt_files:
        filepath = os.path.join(directory_path, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                grids_data = parse_sudoku_file(content)
                
                # Add filename info to each grid
                for grid_data in grids_data:
                    grid_data['filename'] = filename
                    all_grids.append(grid_data)
        except Exception as e:
            st.warning(f"Could not read {filename}: {e}")
    
    return all_grids


# Streamlit App
st.set_page_config(page_title="Sudoku Solver", page_icon="🧩", layout="wide")

st.title("🧩 Sudoku Solver with Visual Steps")
st.markdown("Load Sudoku puzzles from a directory or upload individual files")

# Initialize session state
if 'all_grids' not in st.session_state:
    st.session_state.all_grids = []

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    track_steps = st.checkbox("Track solving steps (first 50)", value=True)
    
    st.markdown("---")
    st.header("📁 Load from Directory")
    
    # Directory input
    dir_path = st.text_input("Directory path", value="./sudoku_grids", 
                             help="Path to folder containing .txt files with sudoku grids")
    
    if st.button("🔄 Load All Grids"):
        with st.spinner("Loading grids..."):
            st.session_state.all_grids = load_grids_from_directory(dir_path)
            if st.session_state.all_grids:
                st.success(f"✅ Loaded {len(st.session_state.all_grids)} grids!")
                
                # Show statistics
                sizes = {}
                for grid_data in st.session_state.all_grids:
                    size = grid_data['size']
                    sizes[size] = sizes.get(size, 0) + 1
                
                st.info("Grid sizes found:")
                for size, count in sorted(sizes.items()):
                    st.write(f"- {size}x{size}: {count} grids")
            else:
                st.error("No grids found!")
    
    st.markdown("---")
    st.header("📤 Or Upload File")

# File uploader
uploaded_file = st.file_uploader("Upload Sudoku file (.txt)", type=['txt'])

if uploaded_file is not None:
    file_content = uploaded_file.read().decode('utf-8')
    uploaded_grids = parse_sudoku_file(file_content)
    
    for grid_data in uploaded_grids:
        grid_data['filename'] = uploaded_file.name
    
    st.session_state.all_grids = uploaded_grids
    st.success(f"✅ Loaded {len(uploaded_grids)} grid(s) from uploaded file")

# Display grids
if st.session_state.all_grids:
    # Filter options
    st.markdown("---")
    col_filter1, col_filter2 = st.columns(2)
    
    with col_filter1:
        # Get unique sizes
        available_sizes = sorted(set(g['size'] for g in st.session_state.all_grids))
        selected_size = st.selectbox("Filter by size", ["All"] + [f"{s}x{s}" for s in available_sizes])
    
    with col_filter2:
        # Get unique filenames
        available_files = sorted(set(g['filename'] for g in st.session_state.all_grids))
        selected_file = st.selectbox("Filter by file", ["All"] + available_files)
    
    # Apply filters
    filtered_grids = st.session_state.all_grids
    
    if selected_size != "All":
        size = int(selected_size.split('x')[0])
        filtered_grids = [g for g in filtered_grids if g['size'] == size]
    
    if selected_file != "All":
        filtered_grids = [g for g in filtered_grids if g['filename'] == selected_file]
    
    st.info(f"Showing {len(filtered_grids)} grid(s)")
    
    # Grid selector
    if filtered_grids:
        selected_idx = st.selectbox(
            "Select puzzle", 
            range(len(filtered_grids)),
            format_func=lambda x: f"{filtered_grids[x]['name']} ({filtered_grids[x]['size']}x{filtered_grids[x]['size']}) - {filtered_grids[x]['filename']}"
        )
        
        grid_data = filtered_grids[selected_idx]
        grid = grid_data['grid']
        grid_size = grid_data['size']
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            display_sudoku_grid(grid, f"Original Puzzle - {grid_data['name']}")
        
        if st.button("🚀 Solve Sudoku", type="primary"):
            with st.spinner("Solving..."):
                # Make a copy for solving
                grid_copy = copy.deepcopy(grid)
                
                # Solve with timing
                t_start = time.time()
                solver = SudokuSolver(grid_copy, track_steps=track_steps)
                solved = solver.solve_sudoku()
                duration = time.time() - t_start
                
                with col2:
                    if solved:
                        display_sudoku_grid(solver.board, "✅ Solved Puzzle")
                    else:
                        st.error("❌ No solution exists")
                
                # Statistics
                st.markdown("---")
                st.subheader("📊 Solving Statistics")
                
                stat_col1, stat_col2, stat_col3, stat_col4, stat_col5 = st.columns(5)
                
                with stat_col1:
                    st.metric("Grid Size", f"{grid_size}x{grid_size}")
                with stat_col2:
                    st.metric("Time", f"{duration*1000:.2f} ms")
                with stat_col3:
                    st.metric("Cells Filled", solver.cells_filled)
                with stat_col4:
                    st.metric("Backtracks", solver.backtrack_count)
                with stat_col5:
                    empty_cells = sum(row.count(0) for row in grid)
                    st.metric("Empty Cells", empty_cells)
                
                # Show solving steps
                if track_steps and solver.steps:
                    st.markdown("---")
                    st.subheader("🎬 Solving Steps (First 50)")
                    
                    step_idx = st.slider("Step", 0, len(solver.steps)-1, 0)
                    step = solver.steps[step_idx]
                    
                    action_emoji = "➕" if step['action'] == 'place' else "➖"
                    st.markdown(f"**Step {step_idx + 1}/{len(solver.steps)}:** {action_emoji} "
                               f"{'Place' if step['action'] == 'place' else 'Remove'} "
                               f"number **{step['num']}** at position "
                               f"**({step['row']}, {step['col']})**")
                    
                    display_sudoku_grid(step['board'], f"Board at Step {step_idx + 1}", 
                                       highlight_cell=(step['row'], step['col']))
    else:
        st.warning("No grids match the selected filters")

else:
    st.info("👆 Load grids from a directory or upload a file to get started!")
    
    st.markdown("---")
    st.markdown("""
    ### 📝 How to use:
    
    1. **Option A - Load from directory:**
       - Enter the path to your folder containing `.txt` files (e.g., `./sudoku_grids`)
       - Click "Load All Grids" button
       
    2. **Option B - Upload single file:**
       - Use the file uploader to select a `.txt` file
    
    3. **Select and solve:**
       - Use filters to find the puzzle you want
       - Select a grid from the dropdown
       - Click "Solve Sudoku" to see the solution!
    
    ### 📁 File format:
    ```
    Grid 01
    0 0 3 0 2 0 6 0 0
    9 0 0 3 0 5 0 0 1
    ...
    Grid 02
    2 0 0 0 8 0 3 0 0
    ...
    ```
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p>Built with Streamlit | Supports 4x4, 9x9, 16x16, and 25x25 Sudoku | Auto-detection of grid sizes</p>
</div>
""", unsafe_allow_html=True)