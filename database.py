import sqlite3
import pandas as pd


class Database:
    """Interacts with an sqlite database."""

    def __init__(self, filename="data/Library.db", script="data/create.sql"):
        """Constructor.

        Args:
          filename: str, name of file to be made.
          script: str, name of sql script that creates the tables.
        """
        self.filename = filename
        self.script = script
        self.connect()

        with open(self.script) as sql:
            sql_script = sql.read()
            self.execute_script(sql_script)

        if not self.query_database("SELECT COUNT(*) FROM BOOK")[0][0]:
            self.populate_loan_table()
            self.populate_book_table()
            self.populate_rec_table()

    def connect(self):
        """Opens a connection to the sqlite database."""
        self.conn = sqlite3.connect(self.filename)
        self.cursor = self.conn.cursor()

    def execute_script(self, sql):
        """Executes a .sql script."""
        self.cursor.executescript(sql)
        self.conn.commit()

    def parse_book_file(self, text_file):
        """The book data text file is put into a dictionary."""
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
        loans = self.parse_loan_file("data/Loan_Reservation_History.txt")
        for loan in loans:
            self.cursor.execute(
                "INSERT INTO loans (bookCopiesID, memberID, checkoutDate, returnDate, reservationDate) VALUES (?, ?, ?, ?, ?)",
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
        """The database tables are populated with records from the text file."""
        books = self.parse_book_file("data/Book_Info.txt")
        for book in books:
        
            author_exist = self.cursor.execute(
                "SELECT 1 FROM authors WHERE authorName = ?", (book["author"],)
            ).fetchone()
            
            if not author_exist:
                self.cursor.execute(
                    "INSERT INTO authors (authorName) VALUES(?)", (book["author"],)
                )
            
            book_exist = self.cursor.execute(
                "SELECT 1 FROM book WHERE title = ? AND genre = ?",
                (book["title"], book["genre"]),
            ).fetchone()
            
            # if book exists in table then only add to book copies
            if book_exist:    
                self.cursor.execute(
                "INSERT INTO bookCopies (bookid, purchaseDate, purchasePrice) SELECT book.id, ?, ? FROM book WHERE book.title = ?;",
                (book["purchase_date"], book["purchase_price"], book["title"]),
                )
            else:
                self.cursor.execute(
                    "INSERT INTO book (authorid, genre, title) SELECT authors.id, ?, ? FROM authors WHERE authorName = ?;",
                        (book["genre"], book["title"], book["author"]),
                    )
                self.cursor.execute(
                    "INSERT INTO bookCopies (bookid, purchaseDate, purchasePrice) VALUES(last_insert_rowid(), ?, ?);",
                    (book["purchase_date"], book["purchase_price"]),
                    )
               
        self.conn.commit()

    def populate_rec_table(self):
        books = self.parse_book_file("data/Book_Recommendations.txt")
        for book in books:
            author_exist = self.cursor.execute(
                "SELECT 1 FROM authors WHERE authorName = ?", (book["author"],)
            ).fetchone()
            if not author_exist:
                self.cursor.execute(
                    "INSERT INTO authors (authorName) VALUES(?)", (book["author"],)
                )
            self.cursor.execute(
                "INSERT INTO recommendations (authorid, genre, title, purchasePrice) VALUES(last_insert_rowid(), ?, ?, ?)",
                (book["genre"], book["title"], book["purchase_price"]),
            )
        self.conn.commit()

    def query_database(self, query):
        return self.cursor.execute(query).fetchall()

    def insert_loan(
        self, book_id, member_id, checkout_date=None, return_date=None, resv_date=None
    ):
        self.cursor.execute(
            "INSERT INTO loans (bookCopiesID, memberID, checkoutDate, returnDate, reservationDate) VALUES (?, ?, ?, ?, ?)",
            (book_id, member_id, checkout_date, return_date, resv_date),
        )
        self.conn.commit()

    def insert_reservation(self, book_id, member_id, resv_date):
        self.cursor.execute(
            "INSERT INTO loans (bookCopiesID, memberID, checkoutDate, returnDate, reservationDate) VALUES (?, ?, ?, ?, ?)",
            (book_id, member_id, None, None, resv_date),
        )
        self.conn.commit()

    def update_book_return(self, book_id, return_date):
        self.cursor.execute(
            "UPDATE loans SET returnDate = ? WHERE bookCopiesID = ?;",
            (return_date, book_id),
        )
        self.conn.commit()

    def get_info_from_title(self, book_title):
        return self.cursor.execute(
            "SELECT book.title, authors.authorName, book.genre from book INNER JOIN authors ON book.authorid = authors.id WHERE book.title = ?",
            (book_title,),
        ).fetchall()

    def get_popular_books(self):
        return self.cursor.execute(
            '''
        SELECT loans.bookCopiesID, book.title, book.genre, authors.authorName, COUNT(loans.checkoutDate) from loans 
        INNER JOIN bookCopies ON loans.bookCopiesID = bookCopies.id
        INNER JOIN book ON bookCopies.bookID = book.id 
        INNER JOIN authors ON book.authorID = authors.id
        GROUP BY loans.bookCopiesID ORDER BY COUNT(loans.checkoutDate) DESC;'''
        ).fetchall()

    def get_rec_table(self):
        return pd.read_sql_query(
            '''
            SELECT recommendations.id, authors.authorName, recommendations.genre, recommendations.title, recommendations.purchasePrice
            FROM recommendations
            INNER JOIN authors
            ON recommendations.authorID=authors.id;
            ''',
            self.conn,
        )

    def get_book_on_loan(self, book_id):
        return self.cursor.execute(
            "SELECT returnDate from loans WHERE bookCopiesID = ?;",
            (book_id,),
        ).fetchall()
        
    def get_is_book_valid(self, book_id):
        return self.cursor.execute(
            "SELECT * FROM BookCopies WHERE id = ?",
            (book_id,),
        ).fetchall()
        
    def get_is_book_reserved(self, book_id):
        return self.cursor.execute(
            "SELECT reservationDate from loans WHERE bookCopiesID = ?",
            (book_id,),
        ).fetchall()
        
    def get_book_info_reserved(self, book_id):
        return self.cursor.execute(
            "SELECT reservationDate, memberid from loans WHERE bookCopiesID = ?;",
            (book_id,),
        ).fetchall()
        
    def get_book_reserved_member(self, book_id, member_id):
        return self.cursor.execute(
            "SELECT reservationDate from loans WHERE bookCopiesID = ? AND memberid = ?;",
            (book_id, member_id),
        ).fetchall()
        
    def get_book_exist(self, book_id):
        return self.cursor.execute(
            "SELECT 1 FROM bookCopies WHERE id = ?;",
            (book_id,),
        ).fetchall()
        
    def get_book_return_dates(self, book_id):
        return self.cursor.execute(
            "SELECT returnDate from loans WHERE bookCopiesID = ?;",
            (book_id,),
        ).fetchall()
        
    def get_book_copies_count(self):
        return self.cursor.execute(
            "SELECT COUNT(*) FROM bookCopies;",
        ).fetchall()
        
    def get_book_count(self):
        return self.cursor.execute(
            "SELECT COUNT(*) FROM book;",
        ).fetchall()
        
    def get_books_loan_count(self):
        return self.cursor.execute(
            "SELECT COUNT(*) FROM loans WHERE returnDate is NULL;",
        ).fetchall()
        
    def get_books_resv_count(self):
        return self.cursor.execute(
            "SELECT COUNT(*) FROM loans WHERE reservationDate IS NOT NULL;",
        ).fetchall() 
        
        
        