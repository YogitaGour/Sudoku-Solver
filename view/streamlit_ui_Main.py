
import streamlit as st
import time
from model.sudoku_generator import generate_puzzle
from model.backtracking_solver import solve_and_time, solve_with_heuristics
from controller.run_analysis import benchmark

"""
def display_puzzle(grid):
    st.title("Sudoku Puzzle Solver")
    st.write("### 🧩 Generated Sudoku Puzzle")
    for row in grid:
        st.write(" ".join(str(val) if val != 0 else "." for val in row))
        """

import streamlit as st

def display_puzzle(grid):
    st.write("### 🧩 Generated Sudoku Puzzle")
    
    # CSS for styling the grid and highlighting subgrids
    st.markdown("""
  
    <style>
        .sudoku-table {
            display: grid;
            grid-template-columns: repeat(9, 1fr);
            gap: 5px;
        }
        .cell {
            width: 30px;
            height: 30px;
            text-align: center;
            font-size: 18px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .highlight {
            background-color: #f0f8ff;
        }
    </style>
    """, unsafe_allow_html=True)

    # Create the grid layout using markdown and text input for each cell
    with st.container():
        for i in range(9):
            # Using a grid to display cells
            cols = st.columns(9)
            for j in range(9):
                # Determine the cell value (empty or filled)
                value = str(grid[i][j]) if grid[i][j] != 0 else ""
                
                # Set a class to highlight 3x3 subgrids
                is_highlighted = ((i // 3) + (j // 3)) % 2 == 0
                highlight_class = "highlight" if is_highlighted else ""

                # Creating text input field inside the grid layout
                with cols[j]:
                    st.text_input(
                        label="",
                        value=value,
                        disabled=False if grid[i][j] == 0 else True,
                        label_visibility="collapsed",
                        max_chars=1,
                        help="Enter number (1-9)" if grid[i][j] == 0 else "",
                        key=f"cell_{i}_{j}"  # Unique key for each input field
                    )

    


def show_results(method_name, puzzle):
    st.write(f"### 🔍 Solving using: `{method_name}`")
    elapsed, solution = solve_with_heuristics(puzzle, method=method_name)
    st.success(f"Solved in **{elapsed:.4f} seconds**")
    st.write("### ✅ Solution:")
    for row in solution:
        st.write(" ".join(str(val) for val in row))

def main():
    st.title("🧠 Sudoku Solver & CSP Analyzer")
    st.write("✔️ Streamlit is working.")  # ✅ Debug line

    st.sidebar.header("Select Heuristic / Algorithm")
    method = st.sidebar.selectbox("Choose technique", [
        "Backtracking",
        "Backtracking + Forward Checking",
        "Backtracking + Arc Consistency",
        "Backtracking + MRV",
        "Backtracking + MRV + LCV + Degree"
    ])

    if st.button("🎲 Generate Puzzle and Solve"):
        puzzle = generate_puzzle()
        display_puzzle(puzzle)
        show_results(method, puzzle)

    if st.button("📊 Run Benchmark (10 Runs)"):
        st.write("Running average time test...")
        times = []
        for _ in range(10):
            puzzle = generate_puzzle()
            elapsed, _ = solve_with_heuristics(puzzle, method)
            times.append(elapsed)
        avg_time = sum(times) / len(times)
        st.success(f"Average time over 10 runs: **{avg_time:.4f} sec**")

if __name__ == "__main__":
    main()
