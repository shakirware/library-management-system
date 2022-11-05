"""book_search.py

This module is used to return books to the
library.

"""

from datetime import datetime


class Return:
    """This class contains methods to return one
    or more books.

    Attributes:
        parent: A reference to the Database object.

    """

    def __init__(self, parent):
        self.parent = parent

    def is_book_available(self, book_id):
        """Check if a book is available.

        Args:
            book_id: The book's ID.

        Returns:
            True, if available and False if unavailable.

        """
        dates = self.parent.get_book_return_dates(book_id)
        if any(date[0] is None for date in dates):
            return False
        return True

    def is_book_reserved(self, book_id):
        """Check if a book is reserved.

        Args:
            book_id: The book's ID.

        Returns:
            True, if reserved and False if not reserved.

        """
        is_reserved = self.parent.get_is_book_reserved(book_id)
        if not all(x[0] is None for x in is_reserved):
            query = self.parent.get_book_info_reserved(book_id)
            member_id, date = query[0][1], query[0][0]
            return True, f"Book {book_id} is reserved by {member_id} on the {date}."
        return False, ""

    def return_book(self, book_id):
        """Return a particular book.

        Args:
            book_id: The book's ID.

        Returns:
            True, if returned and False if not returned.

        """
        book_exist = self.parent.get_book_exist(book_id)
        available = self.is_book_available(book_id)
        if book_exist:
            if not available:
                today = datetime.today().strftime("%Y-%m-%d")
                self.parent.update_book_return(book_id, today)
                return True, "Book has been returned."
            else:
                return False, "The book is already available."
        return False, "The book is invalid."

    def return_books(self, id_array):
        """Return multiple books in one go.

        Args:
            id_array: Array of book IDs.

        Returns:
            Two arrays, containing book IDs of the returned and already available.

        """
        book_returned = []
        book_available = []
        for book_id in id_array:
            book_exist = self.parent.get_book_exist(book_id)
            available = self.is_book_available(book_id)
            if book_exist:
                if not available:
                    today = datetime.today().strftime("%Y-%m-%d")
                    self.parent.update_book_return(book_id, today)
                    book_returned.append(book_id)
                else:
                    book_available.append(book_id)

        return book_returned, book_available
