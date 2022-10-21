import sqlite3
from database import Database


class Search(Database):
    def __init__(self, parent):
        self.parent = parent

    def book_title_search(self, title):
        return self.parent.query_database(
            f"""
            SELECT  bookcopies.id,
                    book.title,
                    book.genre,
                    authors.authorname
            FROM   bookcopies
            JOIN book
                ON bookcopies.id = book.id
            JOIN authors
                ON book.authorid = authors.id
            WHERE  book.title LIKE '%{title}%'; 
        """
        )

    def book_author_search(self, author):
        return self.parent.query_database(
            f"""
            SELECT  bookcopies.id,
                    book.title,
                    book.genre,
                    authors.authorname
            FROM   bookcopies
            JOIN book
                ON bookcopies.id = book.id
            JOIN authors
                ON book.authorid = authors.id
            WHERE  authors.authorname LIKE '%{author}%'; 
        """
        )


db = Database()
print(Search(db).book_title_search("design"))
