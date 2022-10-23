from database import Database
from datetime import datetime, timedelta


class Return(Database):
    def __init__(self, parent):
        self.parent = parent

    def is_book_available(self, book_id):
        dates = self.parent.get_book_on_loan(book_id)
        if any(date[0] is None for date in dates):
            return False
        return True

    def is_book_valid(self, book_id):
        return len(self.parent.get_is_book_valid(book_id)) > 0

    def is_book_reserved(self, book_id):
        is_reserved = self.parent.get_is_book_reserved(book_id)
        if not all(x[0] is None for x in is_reserved):
            query = self.parent.get_book_info_reserved(book_id)
            member_id, date = query[0][1], query[0][0]
            return f"Book {book_id} is reserved by {member_id} on the {date}."
        return False

    def return_book(self, book_id):
        # an appropriate message should be displayed if the book is reserved by a member.
        valid = self.is_book_valid(book_id)
        available = self.is_book_available(book_id)

        if not available and valid:
            today = datetime.today().strftime("%Y-%m-%d")
            self.parent.update_book_return(book_id, today)
            return True, "Book has been returned"

        return False, "The book is unavailable or invalid."
