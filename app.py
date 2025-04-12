"""from model.sudoku_generator import generate_puzzle
from view.ui import print_board  # or Streamlit layout
from view.streamlit_ui import main as streamlit_main  # ✅ avoid conflict
import sys
import os
sys.path.append(os.path.dirname(__file__))

def main():
    puzzle = generate_puzzle(removed_cells=40)
    print("🧩 New Sudoku Puzzle:")
    print_board(puzzle)


if __name__ == "__main__":
        streamlit_main() 

"""
# app.py
from view.streamlit_ui import main as streamlit_main
from model.sudoku_generator import generate_puzzle
from view.ui import print_board

def run_console_version():
    # This is optional, in case you want to run from terminal
    puzzle = generate_puzzle(removed_cells=40)
    print("🧩 New Sudoku Puzzle:")
    print_board(puzzle)

if __name__ == "__main__":
    # Launch Streamlit UI
    streamlit_main()


