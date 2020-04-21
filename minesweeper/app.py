from minesweeper import util, game

def run():
    u_input = util.prompt_input("Would you like to play a game?").lower()
    if u_input not in ('y', 'yes', 'yup', 'yeah', 'ya', 'sure', 'why not', 'ok'):
        print("Ok bye!")
        exit(0)

    while True:
        u_input = util.prompt_input("What difficulty? (E)asy, (I)ntermediate, (H)ard: ").upper()
        if u_input in (game.DIFFICULTIES):
            break
        print("Invalid difficulty chosen.")

    board = game.Board(u_input)

    print ("Let's begin, here is your gameboard:");
    board.render()

    try:
        while True:
            print("\nChoose a square!")
            while True:
                col = util.prompt_input("Which column?")
                if board.valid_col(col):
                    break
                print("Invalid column, please choose again")
            while True:
                row = util.prompt_input("Which row?")
                if board.valid_row(row):
                    break
                print("Invalid row, please choose again")

            board.play(int(col) - 1, int(row) - 1)
            board.render()
    finally:
        exit(0)
