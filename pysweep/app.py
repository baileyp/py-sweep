from pysweep import console, game


def run():
    user_input = console.read("Would you like to play a game?").lower()
    if user_input not in ('y', 'yes', 'yup', 'yeah', 'ya', 'sure', 'why not', 'ok'):
        console.out("Ok bye!")
        exit(0)

    user_input = console.read_until(
        lambda: console.read("What difficulty? (E)asy, (I)ntermediate, (H)ard: ").upper(),
        lambda d: d in game.DIFFICULTIES,
        "Invalid difficulty chosen."
    )

    board = game.Board(user_input)

    console.out("\nLet's begin, here is your yard:")
    console.out(str(board))

    try:
        while True:
            console.out("Choose a plot!")
            col = console.read_until(
                lambda: console.read("Which column?", int, 0) - 1,
                board.valid_col,
                "Invalid column, please choose again"
            )
            row = console.read_until(
                lambda: console.read("Which row?", int, 0) - 1,
                board.valid_row,
                "Invalid row, please choose again"
            )

            board.play(col, row)
            console.out(str(board))
    except game.ThreatFound:
        console.out(str(board))
        console.out("Oh no, you stepped on a snake! Game Over!")
    except game.Victory:
        console.out(str(board))
        console.out("Congratulations, you located all the snakes! Victory!")
    except Exception as e:
        console.out(type(e))
        console.out(e)
    finally:

        exit(0)