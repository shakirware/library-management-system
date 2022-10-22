from database import Database
from book_search import Search
from book_checkout import Checkout
from book_return import Return

db = Database()
search = Search(db)
checkout = Checkout(db)
return_ = Return(db)
#print(search.book_title_search("Some Mathematical Methods of Physics"))
#print(checkout.is_book_valid(123))
#print(checkout.withdraw(104, 1111))
#print(checkout.reserve_book(35, 1176, '22-10-2022'))
print(return_.return_book(33))
