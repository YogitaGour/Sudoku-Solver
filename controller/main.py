import sys
import os

# Make sure the project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.sudoku_generator import generate_puzzle
from model.backtracking_solver import solve_and_time
from controller.run_analysis import benchmark

def run_full_pipeline():
    print("🎯 Generating a new Sudoku puzzle...\n")
    puzzle = generate_puzzle()

    print("🧩 Puzzle:")
    for row in puzzle:
        print(" ".join(str(cell) if cell != 0 else "." for cell in row))

    print("\n⏳ Solving with Backtracking...")
    elapsed_time = solve_and_time(puzzle)
    print(f"\n✅ Solved in {elapsed_time:.4f} seconds.\n")

    print("📊 Running Benchmark (10 runs)...\n")
    benchmark()

if __name__ == "__main__":
    run_full_pipeline()

