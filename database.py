import sqlite3
import pandas as pd

from data.constants import *


class Database:
    """This class represents an SQLite3 database.

    Attributes:
        conn: A Connection object that represents an open SQLite database.
        cursor: A Cursor object that represents a database cursor.
        filename: The path of the database file to be opened/created.
        script: The path of an SQL script.

    """

    def __init__(self, filename="data/Library.db", script="data/create.sql"):
        self.filename = filename
        self.script = script
        self.connect()

        with open(self.script) as sql:
            sql_script = sql.read()
            self.execute_script(sql_script)

        book_count = self.get_book_count()
        if not book_count:
            self.populate_loan_table()
            self.populate_book_table()
            self.populate_rec_table()

    def connect(self):
        """Opens a connection to the SQLite database."""
        self.conn = sqlite3.connect(self.filename)
        self.cursor = self.conn.cursor()

    def execute_script(self, sql):
        """Execute the statements within an SQL script and commit the changes.

        Args:
            sql: The sql script.

        """
        self.cursor.executescript(sql)
        self.conn.commit()

    def parse_book_file(self, text_file):
        """Open the book data file and parse it.

        Args:
            text_file: The book data file.

        Returns:
            books: An array of books.

        """
        books = []
        with open(text_file, encoding="utf8") as file:
            for line in file:
                book_string = line.rstrip().split("|")
                book = {
                    "id": book_string[0],
                    "title": book_string[2],
                    "genre": book_string[1],
                    "author": book_string[3],
                    "purchase_price": book_string[4],
                    "purchase_date": book_string[5],
                }
                books.append(book)
        return books

    def parse_loan_file(self, text_file):
        """Open the loan data file and parse it.

        Args:
            text_file: The loan data file.

        Returns:
            loans: An array of loan records.

        """
        loans = []
        with open(text_file) as file:
            for line in file:
                loan_string = line.rstrip().split("|")
                loan_string = list(
                    map(lambda x: None if x == "None" else x, loan_string)
                )
                loan = {
                    "bookCopiesID": loan_string[0],
                    "resv_date": loan_string[1],
                    "checkout_date": loan_string[2],
                    "return_date": loan_string[3],
                    "member_id": loan_string[4],
                }
                loans.append(loan)
        return loans

    def populate_loan_table(self):
        """Insert the loan data into the SQLite database."""
        loans = self.parse_loan_file("data/Loan_Reservation_History.txt")
        for loan in loans:
            self.cursor.execute(
                INSERT_LOAN_SQL,
                (
                    loan["bookCopiesID"],
                    loan["member_id"],
                    loan["checkout_date"],
                    loan["return_date"],
                    loan["resv_date"],
                ),
            )
        self.conn.commit()

    def populate_book_table(self):
        """Insert the book data into the SQLite database"""
        books = self.parse_book_file("data/Book_Info.txt")
        for book in books:

            author_exist = self.cursor.execute(
                AUTHOR_EXIST_SQL, (book["author"],)
            ).fetchone()

            if not author_exist:
                self.cursor.execute(INSERT_AUTHOR_SQL, (book["author"],))

            book_exist = self.cursor.execute(
                BOOK_EXIST_SQL,
                (book["title"], book["genre"]),
            ).fetchone()

            if book_exist:
                self.cursor.execute(
                    INSERT_BOOKCOPIES_SQL,
                    (book["purchase_date"],
                     book["purchase_price"], book["title"]),
                )
            else:
                self.cursor.execute(
                    INSERT_BOOK_SQL,
                    (book["genre"], book["title"], book["author"]),
                )
                self.cursor.execute(
                    INSERT_BOOKCOPIES_LAST_SQL,
                    (book["purchase_date"], book["purchase_price"]),
                )

        self.conn.commit()

    def populate_rec_table(self):
        """Insert the recommendation records into the SQLite database."""
        books = self.parse_book_file("data/Book_Recommendations.txt")
        for book in books:
            author_exist = self.cursor.execute(
                AUTHOR_EXIST_SQL, (book["author"],)
            ).fetchone()
            if not author_exist:
                self.cursor.execute(INSERT_AUTHOR_SQL, (book["author"],))
            self.cursor.execute(
                INSERT_RECOMMENDATION_SQL,
                (book["genre"], book["title"], book["purchase_price"]),
            )
        self.conn.commit()

    def query_database(self, query):
        """Execute an SQL statement and return the results.

        Args:
            query: An SQL statement.

        Returns:
            The rows of a query result.

        """
        return self.cursor.execute(query).fetchall()

    def insert_loan(
        self, book_id, member_id, checkout_date=None, return_date=None, resv_date=None
    ):
        """Insert a loan record into the SQLite Database.

        Args:
            book_id: The book id.
            member_id: The member id.
            checkout_date: The checkout date (optional).
            return_date: The return date (optional).
            resv_date: The reservation date (optional).

        """
        self.cursor.execute(
            INSERT_LOAN_SQL,
            (book_id, member_id, checkout_date, return_date, resv_date),
        )
        self.conn.commit()

    def update_book_return(self, book_id, return_date):
        """Update the return date for a loan record.

        Args:
            book_id: The book id.
            return_date: The return date e.g 29-10-2022

        """
        self.cursor.execute(
            UPDATE_LOAN_SQL,
            (return_date, book_id),
        )
        self.conn.commit()

    def get_info_from_title(self, book_title):
        """Get a book's author and genre from the title.

        Args:
            book_title: The book title.

        Returns:
            The rows a book's information - title, author and genre.

        """
        return self.cursor.execute(
            BOOK_INFO_SQL,
            (book_title,),
        ).fetchall()

    def get_popular_books(self):
        return self.cursor.execute(POPULAR_BOOK_SQL).fetchall()

    def get_rec_table(self):
        return pd.read_sql_query(
            GET_RECOMMENDATIONS_SQL,
            self.conn,
        )

    def get_is_book_valid(self, book_id):
        return self.cursor.execute(
            BOOK_VALID_SQL,
            (book_id,),
        ).fetchall()

    def get_is_book_reserved(self, book_id):
        return self.cursor.execute(
            BOOK_RESERVED_SQL,
            (book_id,),
        ).fetchall()

    def get_book_info_reserved(self, book_id):
        return self.cursor.execute(
            BOOK_RESERVED_INFO_SQL,
            (book_id,),
        ).fetchall()

    def get_book_reserved_member(self, book_id, member_id):
        return self.cursor.execute(
            BOOK_RESERVED_MEMBER_SQL,
            (book_id, member_id),
        ).fetchall()

    def get_book_exist(self, book_id):
        return self.cursor.execute(
            BOOK_ID_EXIST_SQL,
            (book_id,),
        ).fetchall()

    def get_book_return_dates(self, book_id):
        return self.cursor.execute(
            LOAN_RETURN_DATES_SQL,
            (book_id,),
        ).fetchall()

    def get_book_copies_count(self):
        return self.cursor.execute(
            BOOKCOPIES_COUNT_SQL,
        ).fetchall()

    def get_book_count(self):
        return self.cursor.execute(
            BOOK_COUNT_SQL,
        ).fetchall()

    def get_books_loan_count(self):
        return self.cursor.execute(
            LOAN_BOOK_COUNT_SQL,
        ).fetchall()

    def get_books_resv_count(self):
        return self.cursor.execute(
            LOAN_RESERVATION_COUNT_SQL,
        ).fetchall()
