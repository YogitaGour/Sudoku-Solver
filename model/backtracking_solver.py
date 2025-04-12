# model/backtracking_solver.py
import time
import copy
from collections import deque

# Check if placing 'num' at (row, col) is valid under Sudoku constraints
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False
    return True

# Find the next empty cell (represented by 0)
def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

# Basic backtracking algorithm to solve Sudoku without any heuristics or inference
def basic_backtracking_solver(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if basic_backtracking_solver(board):
                return True
            board[row][col] = 0
    return False

# Time the basic backtracking solver for performance evaluation
def solve_and_time(board):
    start = time.perf_counter()
    board_copy = copy.deepcopy(board)
    basic_backtracking_solver(board_copy)
    end = time.perf_counter()
    return end - start

# Solve puzzle using selected strategy (Backtracking, FC, AC, MRV, etc.)
def solve_with_heuristics(puzzle, method="Backtracking"):
    start = time.time()
    solution = backtracking_solver(copy.deepcopy(puzzle), strategy=method)
    end = time.time()
    return end - start, solution

# General backtracking solver with options for heuristics and inference
def backtracking_solver(puzzle, strategy="Backtracking"):
    variables = [(r, c) for r in range(9) for c in range(9) if puzzle[r][c] == 0]
    domains = {(r, c): list(range(1, 10)) for r, c in variables}

    if "Forward Checking" in strategy:
        apply_forward_checking(puzzle, domains)
    if "Arc Consistency" in strategy:
        apply_arc_consistency(puzzle, domains)

    return recursive_backtracking(puzzle, variables, domains, strategy)

# Recursive backtracking with support for heuristics (MRV, Degree, LCV)
def recursive_backtracking(puzzle, variables, domains, strategy):
    if not variables:
        return puzzle

    var = select_variable(variables, domains, strategy)

    for value in order_values(var, domains[var], puzzle, strategy):
        if is_safe(puzzle, var[0], var[1], value):
            puzzle[var[0]][var[1]] = value
            new_vars = [v for v in variables if v != var]
            result = recursive_backtracking(puzzle, new_vars, domains, strategy)
            if result:
                return result
            puzzle[var[0]][var[1]] = 0
    return None

# Select next variable to assign using MRV and Degree heuristic
def select_variable(variables, domains, strategy):
    if "MRV" in strategy:
        min_len = min(len(domains[v]) for v in variables)
        candidates = [v for v in variables if len(domains[v]) == min_len]
        if "Degree" in strategy:
            return max(candidates, key=lambda var: count_constraints(var))
        return candidates[0]
    return variables[0]

# Count how many constraints a variable imposes on others (used in Degree heuristic)
def count_constraints(var):
    r, c = var
    neighbors = set()
    for i in range(9):
        neighbors.add((r, i))
        neighbors.add((i, c))
    sr, sc = 3 * (r // 3), 3 * (c // 3)
    for i in range(sr, sr + 3):
        for j in range(sc, sc + 3):
            neighbors.add((i, j))
    neighbors.discard(var)
    return len(neighbors)

# Order values using Least Constraining Value (LCV)
def order_values(var, values, puzzle, strategy):
    if "LCV" not in strategy:
        return values

    def count_conflicts(value):
        r, c = var
        count = 0
        for i in range(9):
            if puzzle[r][i] == value or puzzle[i][c] == value:
                count += 1
        sr, sc = 3 * (r // 3), 3 * (c // 3)
        for i in range(sr, sr + 3):
            for j in range(sc, sc + 3):
                if puzzle[i][j] == value:
                    count += 1
        return count

    return sorted(values, key=count_conflicts)

# Apply Forward Checking: prune domain values that are not safe
def apply_forward_checking(puzzle, domains):
    for (r, c), domain in domains.items():
        domain[:] = [val for val in domain if is_safe(puzzle, r, c, val)]

# Apply Arc Consistency (AC-3) to prune domain values based on neighbors
def apply_arc_consistency(puzzle, domains):
    queue = deque(domains.keys())
    while queue:
        var = queue.popleft()
        r, c = var
        revised = False
        for val in domains[var][:]:
            if not any(is_safe(puzzle, r, c, v) for v in domains[var]):
                domains[var].remove(val)
                revised = True
        if revised:
            queue.extend(get_neighbors(var))

# Get all variables that share a constraint with the given variable
# (used by Arc Consistency and Degree heuristic)
def get_neighbors(var):
    r, c = var
    neighbors = set()
    for i in range(9):
        neighbors.add((r, i))
        neighbors.add((i, c))
    sr, sc = 3 * (r // 3), 3 * (c // 3)
    for i in range(sr, sr + 3):
        for j in range(sc, sc + 3):
            neighbors.add((i, j))
    neighbors.discard(var)
    return list(neighbors)

# Safety check used across different strategies to validate placement
def is_safe(puzzle, row, col, num):
    for i in range(9):
        if puzzle[row][i] == num or puzzle[i][col] == num:
            return False
    sr, sc = 3 * (row // 3), 3 * (col // 3)
    for i in range(sr, sr + 3):
        for j in range(sc, sc + 3):
            if puzzle[i][j] == num:
                return False
    return True
