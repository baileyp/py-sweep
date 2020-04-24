class FunctionInvoked(BaseException):
    pass


class Square:
    def __init__(self, r=False, f=False, t=False):
        self.revealed = lambda: r
        self.is_flagged = lambda: f
        self.has_threat = lambda: t

    def reveal(self):
        pass

    def flag(self):
        return not self.is_flagged()
