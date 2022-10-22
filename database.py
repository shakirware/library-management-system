import sqlite3
import os.path

class Database:
    """Interacts with an sqlite database."""

    def __init__(self, filename='Library.db', script='create.sql'):
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

        if not self.query_database('SELECT COUNT(*) FROM BOOK')[0][0]:
            self.populate_loan_table()
            self.populate_book_table()
            
    def connect(self):
        """Opens a connection to the sqlite database."""
        self.conn = sqlite3.connect(self.filename);
        self.cursor = self.conn.cursor()
    
    def execute_script(self, sql):
        """Executes a .sql script."""
        self.cursor.executescript(sql)
        self.conn.commit()
     
    def parse_book_file(self, text_file):
        """The book data text file is put into a dictionary."""
        books = []
        with open(text_file) as file:
            for line in file:
                book_string = line.rstrip().split('|')
                book = {
                    'id': book_string[0],
                    'title': book_string[2],
                    'genre': book_string[1],
                    'author': book_string[3],
                    'purchase_price': book_string[4],
                    'purchase_date': book_string[5]
                }
                books.append(book)
        return books
        
    def parse_loan_file(self, text_file):
        loans = []
        with open(text_file) as file:
            for line in file:
                loan_string = line.rstrip().split('|')
                loan_string = list(map(lambda x: None if x == 'None' else x, loan_string))
                loan = {
                    'bookCopiesID': loan_string[0],
                    'resv_date': loan_string[1],
                    'checkout_date': loan_string[2],
                    'return_date': loan_string[3],
                    'member_id': loan_string[4]
                }
                loans.append(loan)
        return loans
    
    def populate_loan_table(self):
        loans = self.parse_loan_file('Loan_Reservation_History.txt')
        for loan in loans:
            self.cursor.execute(
                "INSERT INTO loans (bookCopiesID, memberID, checkoutDate, returnDate, reservationDate) VALUES (?, ?, ?, ?, ?)",
                (loan['bookCopiesID'], loan['member_id'], loan['checkout_date'], loan['return_date'], loan['resv_date'])
                )
        self.conn.commit()
            
                
    def populate_book_table(self):
        """The database tables are populated with records from the text file."""
        books = self.parse_book_file('Book_Info.txt')
        for book in books:
            author_exist = self.cursor.execute("SELECT 1 FROM authors WHERE authorName = ?", (book['author'],)).fetchone()
            if not author_exist:
                self.cursor.execute("INSERT INTO authors (authorName) VALUES(?)", (book['author'],))
            book_exist = self.cursor.execute("SELECT 1 FROM book WHERE title = ? AND genre = ?", (book['title'], book['genre'])).fetchone()
            # if book not already in book table then add to bookcopies and book
            if not book_exist:
                self.cursor.execute("INSERT INTO book (authorid, genre, title) VALUES(last_insert_rowid(), ?, ?)", (book['genre'], book['title']))
                self.cursor.execute("INSERT INTO bookCopies (bookid, purchaseDate, purchasePrice) VALUES(last_insert_rowid(), ?, ?);", (book['purchase_date'], book['purchase_price']))
            else:
                # book already in book table so grab and id and insert into bookcopies
                book_id = self.cursor.execute("SELECT id FROM book WHERE title = ? AND genre = ?", (book['title'], book['genre'])).fetchone()
                self.cursor.execute("INSERT INTO bookCopies (bookid, purchaseDate, purchasePrice) VALUES(?, ?, ?);", (book_id[0], book['purchase_date'], book['purchase_price']))
        self.conn.commit()
                
    def query_database(self, query):
        return self.cursor.execute(query).fetchall()
        
        
    def insert_loan(self, book_id, member_id, checkout_date = None, return_date = None, resv_date = None):
        self.cursor.execute("INSERT INTO loans (bookCopiesID, memberID, checkoutDate, returnDate, reservationDate) VALUES (?, ?, ?, ?, ?)", 
                (book_id, member_id, checkout_date, return_date, resv_date)
        )
        self.conn.commit()
        
    def insert_reserve(self, book_id, member_id, resv_date):
        self.cursor.execute("INSERT INTO loans (bookCopiesID, memberID, checkoutDate, returnDate, reservationDate) VALUES (?, ?, ?, ?, ?)", 
                (book_id, member_id, None, None, resv_date)
        )
        self.conn.commit()
        
    def update_book_return(self, book_id, return_date):
        self.cursor.execute("UPDATE loans SET returnDate = ? WHERE bookCopiesID = ?;", 
                (return_date, book_id)
        )
        self.conn.commit()

