from pysweep import console, game, renderer


def run():
    user_input = console.read("Would you like to play a game?").lower()
    if user_input not in ('y', 'yes', 'yup', 'yeah', 'ya', 'sure', 'why not', 'ok'):
        console.out("Ok bye!")
        exit(0)

    user_input = console.read_until(
        lambda: console.read("What difficulty? (E)asy, (I)ntermediate, (H)ard: ").upper(),
        game.Spec.valid,
        "Invalid difficulty chosen."
    )

    board = game.Board(game.Spec(user_input), renderer.SnakeRenderer())

    console.out("\nHOW TO PLAY")
    console.out("-----------")
    console.out("Play by typing commands at the prompt. Commands are a combo of an action and/or a plot.")
    console.out("\nAvailable actions are (r)eveal, (f)lag, and (q)uit")
    console.out(" - Reveal will pull the grass and show what is underneath. This is the default and can be omitted.")
    console.out(" - Flag will toggle a plot of grass as having a snake under it or not.")
    console.out(" - Quit will exit the current game")
    console.out("\nPlots are specified by column then row. You can also specify sequences or rows/and or columns by")
    console.out("separating values with commas or ranges with a dash")
    console.out("\nSAMPLE COMMANDS")
    console.out("---------------")
    console.out("Reveal column 5, row 5: 5 5")
    console.out("Flag/Unflag column 1, row 3: f 1 3")
    console.out("Reveal column 5, rows 3 through 6: 5 3-6")
    console.out("Reveal columns 1 and 5, row 7: 1,5 7")
    console.out("Reveal columns 7 and 9, rows 3 through 5: 7,9 3-5")
    console.out("Quit game: q")

    console.out("\nLet's begin! here is your yard:\n")
    console.out(board.render())

    try:
        while True:
            action, col, row = console.read_until(
                lambda: console.read("Make your move:", board.parse_command, ('', 0, 0)),
                lambda c: board.validate_command(*c),
                "Invalid command, please try again"
            )
            try:
                board.play(action, col, row)
            except game.CannotReveal:
                console.out("\nFlags must be removed before the plot can be revealed!")
            except game.CannotFlag:
                console.out("\nFlags cannot be placed on revealed plots!")
            console.out("\n" + board.render())
    except game.ThreatFound:
        console.out(board.render())
        console.out("Oh no, you stepped on a snake! Game Over!")
    except game.Victory:
        console.out(board.render())
        console.out("Congratulations, you located all the snakes! Victory!")
    except game.QuitGame:
        console.out("Bye now, hope you had fun!")
    finally:
        exit(0)
