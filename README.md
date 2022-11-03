# library-management-system
A simple library management system in Python.


# TODO

# library-management-system
A simple library management system in Python.


# TODO

Unit Testing
Visualise the recommendation list using Matplotlib.
Revise reserve book function and add option to reserve book if book is not available.
Finish Docstrings
Change encoding 
Fix UI input - input should be flashing. Potentially add a status bar at the bottom. Change colour of input in UI.


 key
update search every
make listbox with multiple lines oor more visible
multiple return
check books from search to return and checkout



update popular book sql {

SQL to get books that have been reserved the most

SELECT bookCopiesID, COUNT(reservationDate) FROM loans GROUP BY bookCopiesID ORDER BY COUNT(reservationDate) ASC;

Check books that checked out the most in last month or so

SELECT bookCopiesID, COUNT(checkoutDate) from loans 
WHERE checkoutDate >= '20-12-2022' 
GROUP BY bookCopiesID
ORDER BY COUNT(checkoutDate);



}

