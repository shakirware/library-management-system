from database import Database
from book_search import Search
from book_checkout import Checkout

db = Database()
search = Search(db)
checkout = Checkout(db)
#print(search.book_title_search("Some Mathematical Methods of Physics"))
#print(checkout.is_book_valid(123))
checkout.withdraw(43)