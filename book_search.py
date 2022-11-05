"""book_search.py

This module is used to perform various searches
on the SQLite Database.

"""


class Search:
    """This class contains methods to search for books
    and authors within the SQLite database.

    Attributes:
        parent: A reference to the Database object.

    """

    def __init__(self, parent):
        self.parent = parent

    def book_title_search(self, title):
        """Perform a wildcard search with a book title.

        Args:
            title: The book's title

        Returns:
            The rows from the search.

        """
        return self.parent.book_title_search_(title)

    def book_author_search(self, author):
        """Perform a wildcard search with an author's name.

        Args:
            author: The book's author

        Returns:
            The rows from the search.

        """
        return self.parent.book_author_search_(author)

    def book_title_author_search(self, title, author):
        """Perform a wildcard search with a book's title and
        an author's name.

        Args:
            title: The book's title.
            author: The book's author

        Returns:
            The rows from the search.

        """
        return self.parent.book_title_author_search_(title, author)
