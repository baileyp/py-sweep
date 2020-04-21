from minesweeper import util

def run():
    u_input = util.prompt_input("Would you like to play a game?").lower()
    if u_input not in ('y', 'yes', 'yup', 'yeah', 'ya', 'sure', 'why not', 'ok'):
        print("Ok bye!")
        exit(0)

    while True:
        u_input = util.prompt_input("What difficulty? (E)asy, (I)ntermediate, (H)ard: ").upper()
        if u_input in ('E', 'I', 'H'):
            break
        print("Invalid difficulty chosen.")

