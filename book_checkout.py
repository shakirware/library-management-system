from database import Database
from datetime import datetime, timedelta


class Checkout(Database):
    """This class contains methods used to check out a book from the library.

    Attributes:
        parent: A reference to the Database object.

    """

    def __init__(self, parent):
        self.parent = parent

    def is_member_valid(self, member_id):
        """Performs a check to determine if member_id is valid.

        Args:
            member_id: The member's id.

        Returns:
            True if valid and False if invalid.

        """
        return 1111 <= member_id <= 2222

    def withdraw(self, book_id, member_id):
        """Checkout the book from the library.

        Args:
            book_id: The book's id.
            member_id: The member's id.

        Returns:
            A tuple containing a bool and a message for the graphical interface.
            The boolean returns as True if book has been checked out and
            False if book doesn't exist or on loan.

        """
        book_exist = self.parent.get_book_exist(book_id)
        if book_exist:
            dates = self.parent.get_book_return_dates(book_id)
            # If any returnDate is NULL then the book is still on loan
            if not any(date[0] is None for date in dates): 
                self.parent.insert_loan(
                    book_id,
                    member_id,
                    checkout_date=datetime.today().strftime("%Y-%m-%d"),
                )
                return True, f" Book {book_id} has been checked out."
            else:
                return False, f" Book {book_id} is on loan to another member."
        else:
            return False, f" Book {book_id} does not exist."

    # Improve function
    def reserve_book(self, book_id, member_id, resv_date):
        """Reserve a book for a member given a reservation date.

        Args:
            book_id: The book's id.
            member_id: The member's id.
            resv_date: A reservation date e.g 2022-10-30

        Returns:
            A tuple containing a bool and a message for the graphical interface.
            The boolean returns as True if book has been reserved and
            False if book already has a reservation.

        """
        dates = self.parent.get_book_reserved_member(book_id, member_id)
        if all(date[0] is None for date in dates) or not dates:
            self.parent.insert_loan(book_id, member_id, resv_date=resv_date)
        else:
            return False, "Member already has a reservation."
        return True, f"Reservation confirmed on {resv_date}"
