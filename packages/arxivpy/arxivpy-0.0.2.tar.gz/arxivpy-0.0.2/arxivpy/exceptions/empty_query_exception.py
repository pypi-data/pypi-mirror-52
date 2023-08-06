

class EmptyQueryException(Exception):

    def __init__(self, message):
        super().__init__()
        self.message = message

    def __str__(self):
        return "\nMessage: {}\n".format(self.message)