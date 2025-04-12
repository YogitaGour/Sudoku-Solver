import sys
import os
import csv
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.sudoku_generator import generate_puzzle
from model.backtracking_solver import solve_with_heuristics

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def benchmark_cli(methods, n=10):
    print(f"\n📊 Running Benchmark for {n} runs on each method:\n")
    results = {}

    for method in methods:
        total_time = 0
        print(f"🔍 {method}")
        for i in range(n):
            puzzle = generate_puzzle()
            elapsed, _ = solve_with_heuristics(puzzle, method=method)
            print(f"  Run {i+1}: {elapsed:.4f} sec")
            total_time += elapsed
        avg = total_time / n
        results[method] = avg
        print(f"  👉 Average: {avg:.4f} sec\n")

    # Save to CSV
    csv_path = os.path.join(OUTPUT_DIR, "benchmark_results.csv")
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Technique", "Average Time (s)"])
        for method, avg_time in results.items():
            writer.writerow([method, round(avg_time, 4)])
    print(f"📁 Results saved to: {csv_path}")

    # Plot results
    plot_path = os.path.join(OUTPUT_DIR, "benchmark_plot.png")
    plot_results(results, plot_path)
    print(f"📊 Plot saved to: {plot_path}")
    
    # Save Markdown summary
    md_path = os.path.join(OUTPUT_DIR, "benchmark_report.md")
    write_markdown_summary(results, md_path)
    print(f"📝 Markdown report saved to: {md_path}")

    # Display Table
    print("\n📈 Final Comparison Table:")
    print("-" * 50)
    print(f"{'Technique':40} {'Avg Time (s)':>10}")
    print("-" * 50)
    for method, avg_time in results.items():
        print(f"{method:40} {avg_time:>10.4f}")
    print("-" * 50)

def write_markdown_summary(results, md_path):
    with open(md_path, 'w') as f:
        f.write("# 🧠 Sudoku Solver Benchmark Report\n\n")
        f.write("This report compares the performance of different CSP techniques used to solve randomly generated Sudoku puzzles.\n\n")
        f.write("## 🔍 Comparison Table\n\n")
        f.write("| Technique | Average Time (s) |\n")
        f.write("|-----------|------------------|\n")
        for method, avg_time in results.items():
            f.write(f"| {method} | {avg_time:.4f} |\n")

        f.write("\n## 📊 Visualization\n")
        f.write("![Benchmark Plot](benchmark_plot.png)\n")

        f.write("\n---\n")
        f.write("🕒 Each average time is based on 10 randomly generated puzzles.\n")


def plot_results(results, plot_path):
    methods = list(results.keys())
    times = list(results.values())

    plt.figure(figsize=(10, 5))
    bars = plt.barh(methods, times, color='skyblue')
    plt.xlabel("Average Time (s)")
    plt.title("Sudoku Solver Heuristic Benchmark")

    for bar, t in zip(bars, times):
        plt.text(bar.get_width() + 0.01, bar.get_y() + 0.25, f"{t:.4f}", fontsize=9)

    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

if __name__ == "__main__":
    heuristic_methods = [
        "Backtracking",
        "Backtracking + Forward Checking",
        "Backtracking + Arc Consistency",
        "Backtracking + MRV",
        "Backtracking + MRV + LCV + Degree"
    ]
    
    benchmark_cli(heuristic_methods)
