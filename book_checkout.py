from database import Database
from datetime import date
import datetime

class Checkout(Database):

    input_prefix, output_prefix, error_prefix = '[+]', '[-]', '[*]' 
    
    def __init__(self, parent):
        self.parent = parent

    def is_member_valid(self, member_id):
        return 1111 <= member_id <= 2222
    
    def is_book_valid(self, book_id):
        return len(self.parent.query_database(f'SELECT * FROM BookCopies WHERE id = {book_id}')) > 0
        
    def withdraw(self, book_id):
        dates = self.parent.query_database(f'SELECT returnDate from loans WHERE bookCopiesID = {book_id};')
        for return_date in dates[0]:
            return_date = datetime.datetime.strptime(return_date, "%Y-%m-%d").date()
            if date.today() < return_date:
                print(return_date)
                
        
