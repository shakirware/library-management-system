from database import Database
from datetime import datetime, timedelta


class Checkout(Database):
    def __init__(self, parent):
        self.parent = parent

    def is_member_valid(self, member_id):
        return 1111 <= member_id <= 2222

    def is_book_valid(self, book_id):
        return len(self.parent.get_is_book_valid(book_id)) > 0

    def withdraw(self, book_id, member_id):
        book_exist = self.parent.get_book_exist(book_id)

        dates = self.parent.get_book_return_dates(book_id)
        # check book_id is valid
        if book_exist:
            if not any(date[0] is None for date in dates):
                # the book is available
                today = datetime.today().strftime("%Y-%m-%d")
                self.parent.insert_loan(book_id, member_id, checkout_date=today)
                return True, f" Book {book_id} has been checked out."
            else:
                # book is still on loan
                return False, f" Book {book_id} is on loan to another member."
        else:
            return False, f" Book {book_id} does not exist."

    def reserve_book(self, book_id, member_id, resv_date):
        dates = self.parent.get_book_reserved_member(book_id, member_id)
        if dates:
            if any(date[0] is None for date in dates):
                pass
            else:
                return False, "Member already has a reservation."
        self.parent.insert_loan(book_id, member_id, resv_date=resv_date)
        # self.parent.insert_reservation(book_id, member_id, resv_date)
        return True, f"Reservation confirmed for {resv_date}"
