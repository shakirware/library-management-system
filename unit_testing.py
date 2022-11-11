from database import Database
from book_search import Search
from book_checkout import Checkout
from book_return import Return
from book_select import Select

import unittest
import os

class BasicLibraryTests(unittest.TestCase):

    def setUp(self):
        os.remove("./data/Library.db")
        self.database = Database()
        self.search = Search(self.database)
        self.checkout = Checkout(self.database)
        self.return_ = Return(self.database)
        self.select = Select(self.database)
        

    def test_search_book(self):
        # Search for the book 'If I Stay' - [(181, 'If I Stay')]
        book = self.search.book_title_search('If I Stay')[0][1]
        self.assertEqual(book, 'If I Stay')

    def test_withdraw_book_on_loan(self):
        # Attempt to withdraw book 1 which is currently on loan.
        book_id = 1
        member_id = 1111
        result, text = self.checkout.withdraw(book_id, member_id)
        self.assertFalse(result)
    
    def test_withdraw_book(self):
        # Attempt to withdraw book 2 which is available.
        book_id = 2
        member_id = 1111
        result, text = self.checkout.withdraw(book_id, member_id)
        self.assertTrue(result)
    
    def test_return_book(self):
        # Attempt to return book 10 which is on loan.
        book_id = 10
        returned, text = self.return_.return_book(book_id)
        self.assertTrue(returned)
    
    def test_return_available_book(self):
        # Attempt to return book 12 which is available.
        book_id = 12
        returned, text = self.return_.return_book(book_id)
        self.assertFalse(returned)
        
if __name__ == '__main__':
    unittest.main()