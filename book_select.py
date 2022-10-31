from database import Database
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import matplotlib.pyplot as plt


class Select(Database):
    """This class contains methods to recommend books
    and genres for the Librarian.

    Attributes:
        parent: A reference to the Database object.
        database: A dataframe containing the recommendation table.

    """
    
    def __init__(self, parent):
        self.parent = parent
        rec_table = self.parent.get_rec_table()
        self.database = pd.DataFrame(rec_table)

    def get_similar_book(self, book_title, amount):
        """Gets a list of similar books.

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
        cv = CountVectorizer()
        return cv.fit_transform(features)

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

    def get_index(self, book_title, df):
        """Get the index of a book given the title. 

        Args:
            book_title: The book's title.
            df: Recommendation table dataframe..

        Returns:
            The index of the book within the dataframe.

        """
        return df.loc[df["title"] == book_title].index[0]

    def get_book_from_index(self, index, df):
        """Get the book record given the index.

        Args:
            index: Index of the book.
            df: Recommendation table dataframe..

        Returns:
            The record of the book within the dataframe.

        """
        return df.loc[df.index == index].to_dict(orient="records")[0]

    def recommend_books(self, budget):
        """Get a list of books to recommend to the librarian,
        given a budget.

        Args:
            budget: Maximum cost of all the books.
           
        Returns:
            A list of books to recommend and the cost of them.

        """
        x = []
        y = []
        book_list = []
        cost = 0
        books = self.parent.get_popular_books()[:5]
        for book in books:
            title = book[1]
            similar_books = self.get_similar_book(title, 5)
            for similar_book, similarity in similar_books:
               
                new_cost = cost + int(similar_book["purchasePrice"])
                if new_cost < int(budget):
                    x.append(similar_book['title'])
                    y.append(similarity)
                    book_list.append(similar_book)
                    cost += int(similar_book["purchasePrice"])
        self.create_graph(x, y)
        return book_list, cost

    def create_graph(self, x, y):
        plt.plot(x, y)
        plt.title('Cosine similarity of books')
        plt.xlabel('Book Title')
        plt.ylabel('Similarity')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig('./assets/books_similarity.png')