class Colorless:
    CLUE = ''
    GRASS = ''
    FLAG = ''
    THREAT = ''
    END = ''
    ERROR = ''
    THREAT_COUNTER = ''


class Colored(Colorless):
    THREAT_COUNTER = '\033[38;5;196m'
    END = '\033[0m'


class SnakeColors(Colored):
    CLUE = '\033[38;5;33m'
    GRASS = '\033[38;5;40m'
    FLAG = '\033[38;5;196m'
    THREAT = '\033[38;5;94m'
