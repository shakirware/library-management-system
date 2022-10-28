from database import Database


class Search(Database):
    def __init__(self, parent):
        self.parent = parent

    def book_title_search(self, title):
        return self.parent.query_database(
            f"""
            SELECT book.title FROM bookCopies 
            JOIN book ON bookCopies.bookid = book.id 
            JOIN authors ON book.authorid = authors.id 
            WHERE book.title LIKE '%{title}%';
        """
        )

    def book_author_search(self, author):
        return self.parent.query_database(
            f"""
            SELECT book.title FROM bookCopies 
            JOIN book ON bookCopies.bookid = book.id 
            JOIN authors ON book.authorid = authors.id 
            WHERE authors.authorname LIKE '%{author}%';
        """
        )

    def book_title_author_search(self, title, author):
        return self.parent.query_database(
            f"""
            SELECT book.title FROM bookCopies 
            JOIN book ON bookCopies.bookid = book.id 
            JOIN authors ON book.authorid = authors.id 
            WHERE 
            book.title LIKE '%{title}%' 
            AND 
            authors.authorname LIKE '%{author}%';
        """
        )
