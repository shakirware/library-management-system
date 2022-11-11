# library-management-system
A library management system in Python utilizing machine learning and an SQLite3 database.

# Basic Features 

- Search for a book using a book title, author name or both.
- Checkout or reserve a book.
- Return a book to the library.
- Machine learning algorithm to recommend new books for the library based on the current most popular book.

# ToDo

- Complete Unit Testing. (unit_testing.py)

# Nice Features

- Search automatically updates with every key entry. 
- Checkboxes for every book in the search, a book can be checked then an action can be performed on it.
- Multiple books can be returned at once using a comma with the book ids e.g 3,5,6.
- Status bar to deliver basic output.
- Reserve option for if a book is currently on loan.
- Calculate the current popular books by finding out the books that have been checked out the most in the last 2 months.
- Recommend getting more copies of a book if it has multiple reservations.
- Display a graph with cosine similarity of the recommended books to the library's current popular books.
- Mock data generation scripts and parsing.
- Normalised SQL tables within data/create.sql.