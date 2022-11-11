import unittest
from database import Database
from book_search import Search
from book_checkout import Checkout
from book_return import Return
from book_select import Select

class BasicLibraryTests(unittest.TestCase):

    def setUp(self):
        self.database = Database()
        self.search = Search(self.database)
        self.checkout = Checkout(self.database)
        self.return_ = Return(self.database)
        self.select = Select(self.database)
        

    def test_search_book(self):
        # Test search function by searching for the book 'If I Stay'.
        # [(181, 'If I Stay')]
        book = self.search.book_title_search('If I Stay')[0][1]
        self.assertEqual(book, 'If I Stay')

if __name__ == '__main__':
    unittest.main()