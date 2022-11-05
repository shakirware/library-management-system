"""book_select.py

This module recommends books for the librarian to purchase
by accessing the recommendations table within the SQLite
database.

"""

from datetime import date
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dateutil.relativedelta import relativedelta
import pandas as pd
import matplotlib.pyplot as plt


class Select:
    """This class contains methods to recommend books
    and genres for the Librarian.

    Attributes:
        parent: A reference to the Database object.
        database: A dataframe containing the recommendation table.

    """

    def __init__(self, parent):
        self.parent = parent
        self.database = pd.DataFrame(self.parent.get_rec_table())

    def get_similar_book(self, book_title, amount):
        """Gets a list of similar books using cosine similarity.

        Args:
            book_title: The book's title.
            amount: Number of books to be returned.

        Returns:
            An array of book records.

        """
        books = []
        query = self.parent.get_info_from_title(book_title)
        temp_df = pd.concat(
            [
                self.database,
                pd.DataFrame.from_records(
                    [
                        {
                            "title": query[0][0],
                            "authorName": query[0][1],
                            "genre": query[0][2],
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )
        book_features = (
            temp_df[["title", "authorName", "genre"]].astype(str).agg(" ".join, axis=1)
        )
        count_matrix = self.create_count_matrix(book_features)
        book_index = self.get_index(book_title, temp_df)
        similar_books = self.get_cosine_similarity(count_matrix, book_index)
        for similar_book in similar_books[1 : amount + 1]:
            book_info = self.get_book_from_index(similar_book[0], temp_df)
            books.append((book_info, similar_book[1]))
        return books

    def create_count_matrix(self, features):
        """Creates a count matrix using CountVectorizer()
        The text is counted to form a matrix. This method converts text data
        into numerical data.

        Args:
            features: The book features.

        Returns:
            A count matrix.

        """
        vectorizer = CountVectorizer()
        return vectorizer.fit_transform(features)

    def get_cosine_similarity(self, count_matrix, index):
        """Get the cosine similarity of an index within the count matrix.

        Args:
            count_matrix: A count matrix derived from book features.
            index: Index of the book.

        Returns:
            A list of books in desc order with respect to the cosine similarity
            of the given index.

        """
        cosine_sim = cosine_similarity(count_matrix)
        similar_books = list(enumerate(cosine_sim[index]))
        return sorted(similar_books, key=lambda x: x[1], reverse=True)

    def get_index(self, book_title, dataframe):
        """Get the index of a book given the title.

        Args:
            book_title: The book's title.
            df: Recommendation table dataframe..

        Returns:
            The index of the book within the dataframe.

        """
        return dataframe.loc[dataframe["title"] == book_title].index[0]

    def get_book_from_index(self, index, dataframe):
        """Get the book record given the index.

        Args:
            index: Index of the book.
            df: Recommendation table dataframe..

        Returns:
            The record of the book within the dataframe.

        """
        return dataframe.loc[dataframe.index == index].to_dict(orient="records")[0]

    def recommend_new_books(self, budget):
        """Get a list of books to recommend to the librarian,
        given a budget.

        Args:
            budget: Maximum cost of all the books.

        Returns:
            A list of books to recommend and the cost of them.

        """
        graph_x = []
        graph_y = []
        book_list = []
        cost = 0
        # Book_date represents 3 months ago today.
        book_date = (date.today() + relativedelta(months=-3)).strftime("%Y-%m-%d")
        books = self.parent.get_popular_books(book_date)[:5]
        for book in books:
            title = book[0]
            similar_books = self.get_similar_book(title, 2)
            for similar_book, similarity in similar_books:
                new_cost = cost + int(similar_book["purchasePrice"])
                if new_cost < int(budget) and similar_book not in book_list:
                    # Only get the first word of a book title for x axis.
                    graph_x.append(similar_book["title"].split(maxsplit=1)[0])
                    graph_y.append(similarity)
                    book_list.append(similar_book)
                    cost += int(similar_book["purchasePrice"])
        self.create_graph(graph_x, graph_y)
        return book_list, cost

    def rec_more_copies(self):
        """Get the book that has the most reservations and
        return a message recommending the librarian to get more
        copies.

        Returns:
            A recommendation message string.

        """
        books = self.parent.book_most_reserved()
        return (
            f"Book {books[0][0]} has {books[0][1]} reservations."
            "You should buy more due to high demand!"
        )

    def create_graph(self, x_axis, y_axis):
        """Create a line graph showing the cosine similarity
        of a recommended book and any current popular library books.

        Args:
            x: book title x axis
            y: cosine similarity y axis

        """
        plt.plot(x_axis, y_axis)
        plt.title("Cosine similarity of books")
        plt.xlabel("Book Title")
        plt.ylabel("Similarity")
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig("./assets/books_similarity.png")
        plt.clf()
