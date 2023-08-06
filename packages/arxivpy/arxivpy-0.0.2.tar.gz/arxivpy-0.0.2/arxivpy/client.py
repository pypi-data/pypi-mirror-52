from .search import Search


class ArXivPyClient:

    URL = 'https://arxiv.org/search'

    def __init__(self):
        self.search = Search(self.URL)
