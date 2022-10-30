from database import Database
from data.constants import *

class Search(Database):
    """This class contains methods to search for books
    and authors within the SQLite database.

    Attributes:
        parent: A reference to the Database object.

    """
    
    def __init__(self, parent):
        self.parent = parent

    def book_title_search(self, title):
        return self.parent.book_title_search_(title)

    def book_author_search(self, author):
        return self.parent.book_author_search_(author)

    def book_title_author_search(self, title, author):
        return self.parent.book_title_author_search_(title, author)
