from minesweeper import console, game


def run():
    user_input = console.read("Would you like to play a game?").lower()
    if user_input not in ('y', 'yes', 'yup', 'yeah', 'ya', 'sure', 'why not', 'ok'):
        print("Ok bye!")
        exit(0)

    user_input = console.read_until(
        lambda: console.read("What difficulty? (E)asy, (I)ntermediate, (H)ard: ").upper(),
        lambda d: d in game.DIFFICULTIES,
        "Invalid difficulty chosen."
    )

    board = game.Board(user_input)

    console.out("\nLet's begin, here is your gameboard:")
    console.out(str(board))

    try:
        while True:
            console.out("Choose a square!")
            col = console.read_until(
                lambda: console.read("Which column?", int, 0),
                board.valid_col,
                "Invalid column, please choose again"
            )
            row = console.read_until(
                lambda: console.read("Which row?", int, 0),
                board.valid_row,
                "Invalid row, please choose again"
            )

            board.play(col - 1, row - 1)
            console.out(str(board))
    except game.BombFound as e:
        console.out(str(board))
        console.out("Oh no, you found a bomb! Game Over!")
    except Exception as e:
        console.out(type(e))
        console.out(e)
    finally:

        exit(0)
