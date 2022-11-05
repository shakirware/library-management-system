from database import Database
from book_search import Search
from book_checkout import Checkout
from book_return import Return
from book_select import Select
from datetime import date
from dateutil.relativedelta import relativedelta


db = Database()
#search = Search(db)
#checkout = Checkout(db)
#return_ = Return(db)
select = Select(db)
#print(search.book_title_search("Harry"))
# print(checkout.is_book_valid(123))
# print(checkout.withdraw(104, 1111))
#print(checkout.reserve_book(35, 1176, "22-10-2022"))
# print(return_.is_book_reserved(38))
# print(return_.return_book(38))

# print(select.get_title_from_index(0))
# print(select.get_similar_books('All the Light We Cannot See'))
# blist, amount = select.recommend_books(200)
# print(blist)

#select.rec_more_copies()

book_date = (date.today() + relativedelta(months=-1)).strftime("%Y-%m-%d")

books = db.get_popular_books(book_date)[:5]
title = 'Harry Potter Paperback Box Set (Books 1-7)'
print(title)
similar_books = select.get_similar_book(title, 5)
print(similar_books)