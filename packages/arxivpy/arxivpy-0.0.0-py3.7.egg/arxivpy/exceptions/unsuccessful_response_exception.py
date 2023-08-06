

class UnsuccessfulResponseException(Exception):

    def __init__(self, code):
        super().__init__()
        self.code = code

    def __str__(self):
        return "Error with code: {}\n".format(self.code)