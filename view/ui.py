def display_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else "." for num in row))
        
def print_board(board):
    for i in range(9):
        row = ""
        for j in range(9):
            cell = board[i][j]
            row += str(cell) if cell != 0 else "."
            row += " "
            if j % 3 == 2 and j != 8:
                row += "| "
        print(row)
        if i % 3 == 2 and i != 8:
            print("-" * 21)
