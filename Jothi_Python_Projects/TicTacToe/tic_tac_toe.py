# Tic-Tac-Toe Game
# A simple two-player game made with Python.

def show_board(board):
    print()
    print(" " + board[0] + " | " + board[1] + " | " + board[2])
    print("---+---+---")
    print(" " + board[3] + " | " + board[4] + " | " + board[5])
    print("---+---+---")
    print(" " + board[6] + " | " + board[7] + " | " + board[8])
    print()


def check_winner(board, mark):
    # Check all rows, columns, and diagonals.
    winning_lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    for line in winning_lines:
        if (board[line[0]] == mark and
                board[line[1]] == mark and
                board[line[2]] == mark):
            return True

    return False


def get_player_move(board, player):
    while True:
        choice = input("Player " + player + ", choose a box (1-9): ").strip()

        if not choice.isdigit():
            print("Please enter a number from 1 to 9.")
            continue

        position = int(choice)

        if position < 1 or position > 9:
            print("That number is outside the board. Choose 1 to 9.")
            continue

        if board[position - 1] in ["X", "O"]:
            print("That box is already taken. Choose another box.")
            continue

        return position - 1


def play_game():
    # The numbers show the available boxes at the start.
    board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    player = "X"

    while True:
        show_board(board)
        position = get_player_move(board, player)
        board[position] = player

        if check_winner(board, player):
            show_board(board)
            print("Player", player, "wins!")
            break

        if "X" not in board and "O" not in board:
            show_board(board)
            print("It is a draw!")
            break

        if all(box in ["X", "O"] for box in board):
            show_board(board)
            print("It is a draw!")
            break

        if player == "X":
            player = "O"
        else:
            player = "X"


def main():
    print("Welcome to Tic-Tac-Toe!")

    while True:
        play_game()
        again = input("Would you like to play again? (yes/no): ").strip().lower()

        if again != "yes":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()
