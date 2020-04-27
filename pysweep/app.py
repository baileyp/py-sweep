from pysweep import console, game, renderer

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

    board = game.Board(user_input, renderer.SnakeRenderer())

    console.out("\nHOW TO PLAY")
    console.out("-----------")
    console.out("Play by typing commands at the prompt. Commands are a combo of an action and/or a plot.")
    console.out("\nAvailable actions are (r)eveal, (f)lag, and (q)uit")
    console.out(" - Reveal will pull the grass and show what is underneath. This is the default and can be omitted.")
    console.out(" - Flag will toggle a plot of grass as having a snake under it or not.")
    console.out(" - Quit will exit the current game")
    console.out("\nPlots are specified by column then row.")
    console.out("\nSAMPLE COMMANDS")
    console.out("---------------")
    console.out("Reveal column 5, row 5: 5 5")
    console.out("Flag/Unflag column 1, row 3: f 1 3")
    console.out("Quit game: q")

    console.out("\nLet's begin! here is your yard:\n")
    console.out(board.render())

    def parse_command(cmd):
        if cmd.upper() == game.QUIT:
            raise game.QuitGame
        action = game.REVEAL
        col, row, *_ = cmd.split(' ')
        if col.upper() in game.ACTIONS:
            action, col, row = cmd.split(' ')
        action, col, row = action.upper(), int(col) - 1, int(row) - 1
        return action, col, row

    def validate_command(action, col, row):
        if action == game.QUIT:
            raise game.QuitGame
        return action in game.ACTIONS and board.valid_col(col) and board.valid_row(row)

    try:
        while True:
            action, col, row = console.read_until(
                lambda: console.read("Make your move:", parse_command, ('', 0, 0)),
                validate_command,
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
