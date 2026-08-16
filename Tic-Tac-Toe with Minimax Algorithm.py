import math


def print_board(board):
    """Print a 3x3 board (board is a list of 9 elements)."""
    print()
    for r in range(3):
        row = board[r*3:(r+1)*3]
        print(" " + " | ".join(cell if cell != " " else "." for cell in row))
        if r < 2:
            print("---+---+---")
    print()

def show_guide():
    """Show positions 1-9 for the player's reference."""
    print("\nPositions:")
    print(" 1 | 2 | 3")
    print("---+---+---")
    print(" 4 | 5 | 6")
    print("---+---+---")
    print(" 7 | 8 | 9\n")

def check_winner(board, player):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),   
        (0,3,6),(1,4,7),(2,5,8),   
        (0,4,8),(2,4,6)            
    ]
    return any(board[a]==board[b]==board[c]==player for a,b,c in wins)

def is_full(board):
    return all(cell != " " for cell in board)

def minimax(board, is_maximizing):
    
    if check_winner(board, "O"):
        return 10
    if check_winner(board, "X"):
        return -10
    if is_full(board):
        return 0

    if is_maximizing: 
        best = -float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = " "
                if score > best:
                    best = score
        return best
    else:  
        best = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, True)
                board[i] = " "
                if score < best:
                    best = score
        return best

def computer_move(board):
    best_score = -float("inf")
    best_move = None
    for i in range(8):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i
    if best_move is not None:
        board[best_move] = "O"

def play():
    board = [" "] * 9
    print("Tic-Tac-Toe — You are X, Computer is O")
    show_guide()
    print_board(board)

    while True:
        while True:
            try:
                user_input = input("Enter your move (1-9): ").strip()
                move = int(user_input) - 1
                if move < 0 or move > 8:
                    print("Choose a number from 1 to 9.")
                    continue
                if board[move] != " ":
                    print("Spot taken — pick another.")
                    continue
                board[move] = "X"
                break
            except ValueError:
                print("Invalid input. Enter a number from 1 to 9.")

        print_board(board)
        if check_winner(board, "X"):
            print("🎉 You win!")
            break
        if is_full(board):
            print("It's a tie!")
            break

        print("Computer is thinking...")
        computer_move(board)
        print_board(board)

        if check_winner(board, "O"):
            print("💻 Computer wins!")
            break
        if is_full(board):
            print("It's a tie!")
            break

if __name__ == "__main__":
    while True:
        play()
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break
