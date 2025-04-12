import random
import copy

# 1. Create empty board
def create_empty_board():
    return [[0 for _ in range(9)] for _ in range(9)]

# 2. Check if a number can be placed
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row+i][start_col+j] == num:
                return False
    return True

# 3. Solver to fill board (backtracking)
def solve_board(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_board(board):
                            return True
                        board[row][col] = 0 #backtrack
                return False
    return True # All cells are filled successfully

# 4. Generate puzzle by removing K cells
# Generate a Sudoku puzzle by first creating a full board,
# then removing a specified number of cells (default: 40)
def generate_puzzle(removed_cells=40):
    board = create_empty_board()
    solve_board(board)  # Now board is fully filled
    puzzle = copy.deepcopy(board)

    count = 0
    while count < removed_cells:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            count += 1
    return puzzle
