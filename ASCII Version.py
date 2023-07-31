import random

def print_board(board):
    row_numbers = "   1   2   3   4   5"
    separator = " -" * 11
    print(row_numbers)
    print(separator)
    for i, row in enumerate(board, 1):
        row_str = f"{i}|"
        for cell in row:
            row_str += f" {cell} |"
        print(row_str)
        print(separator)

def check_winner(board, current_player):
    for row in range(5):
        for col in range(5):
            if board[row][col] == current_player:
                if is_win(board, row, col, current_player):
                    return True
    return False

def is_win(board, row, col, current_player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for dr, dc in directions:
        count = 1
        for step in range(1, 5):
            r, c = row + dr * step, col + dc * step
            if 0 <= r < 5 and 0 <= c < 5 and board[r][c] == current_player:
                count += 1
            else:
                break
        for step in range(1, 5):
            r, c = row - dr * step, col - dc * step
            if 0 <= r < 5 and 0 <= c < 5 and board[r][c] == current_player:
                count += 1
            else:
                break
        if count >= 5:
            return True
    return False

def computer_turn(board):
    available_cells = [(row, col) for row in range(5) for col in range(5) if board[row][col] == " "]
    if available_cells:
        row, col = random.choice(available_cells)
        board[row][col] = "O"
        return True
    return False

def main():
    board = [[" " for _ in range(5)] for _ in range(5)]
    while True:
        try:
            game_mode = int(input("Press 1 for Single-Player. Press 2 for Player vs Player: "))
            if game_mode in (1, 2):
                player_vs_player = game_mode == 2
                break
            else:
                print("Invalid input. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter 1 or 2.")
            
    print("Welcome to the Longest Line Game!")
    print("Player 1: X")
    if player_vs_player:
        print("Player 2: O")
    else:
        print("Computer: O")

    current_player = "X"
    while True:
        print_board(board)

        if current_player == "X":
            while True:
                try:
                    row = int(input(f"Player {current_player}, enter row (1-5): ")) - 1
                    col = int(input(f"Player {current_player}, enter column (1-5): ")) - 1
                    if 0 <= row < 5 and 0 <= col < 5 and board[row][col] == " ":
                        board[row][col] = current_player
                        break
                    else:
                        print("Invalid input or cell already occupied. Try again.")
                except ValueError:
                    print("Invalid input. Try again.")
        else:
            if player_vs_player:
                while True:
                    try:
                        row = int(input(f"Player {current_player}, enter row (1-5): ")) - 1
                        col = int(input(f"Player {current_player}, enter column (1-5): ")) - 1
                        if 0 <= row < 5 and 0 <= col < 5 and board[row][col] == " ":
                            board[row][col] = current_player
                            break
                        else:
                            print("Invalid input or cell already occupied. Try again.")
                    except ValueError:
                        print("Invalid input. Try again.")
            else:
                if not computer_turn(board):
                    print("No more moves left. It's a tie!")
                    break

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()
