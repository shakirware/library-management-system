from database import Database
from datetime import datetime, timedelta

class Return(Database):
    
    def __init__(self, parent):
        self.parent = parent
        
    def is_book_available(self, book_id):
        dates = self.parent.query_database(f'SELECT returnDate from loans WHERE bookCopiesID = {book_id};')
        if any(date[0] is None for date in dates):
            return False
        return True
        
    def is_book_valid(self, book_id):
        return len(self.parent.query_database(f'SELECT * FROM BookCopies WHERE id = {book_id}')) > 0

    def return_book(self, book_id):
        # an appropriate message should be displayed if the book is reserved by a member. 
        valid = self.is_book_valid(book_id)
        available = self.is_book_available(book_id)
        
        if not available and valid:
            today = datetime.today().strftime('%Y-%m-%d')
            self.parent.update_book_return(book_id, today)
            return True, 'Book has been returned'
            
        return False, 'The book is unavailable or invalid.'

            
   
                
        
