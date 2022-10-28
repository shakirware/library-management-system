# https://towardsdatascience.com/using-cosine-similarity-to-build-a-movie-recommendation-system-ae7f20842599
from database import Database
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


class Select(Database):
    def __init__(self, parent):
        self.parent = parent
        rec_table = self.parent.get_rec_table()
        self.database = pd.DataFrame(rec_table)

    def get_similar_book(self, book_title, amount):
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
            books.append(book_info)
        return books

    def create_count_matrix(self, features):
        cv = CountVectorizer()
        return cv.fit_transform(features)

    def get_cosine_similarity(self, count_matrix, index):
        cosine_sim = cosine_similarity(count_matrix)
        similar_books = list(enumerate(cosine_sim[index]))
        return sorted(similar_books, key=lambda x: x[1], reverse=True)

    def get_index(self, book_title, df):
        return df.loc[df["title"] == book_title].index[0]

    def get_book_from_index(self, index, df):
        return df.loc[df.index == index].to_dict(orient="records")[0]

    def get_popular_books(self, amount):
        popular_books = self.parent.get_popular_books()[:amount]
        return popular_books

    def recommend_books(self, budget):
        book_list = []
        cost = 0
        books = self.get_popular_books(5)
        for book in books:
            title = book[1]
            similar_books = self.get_similar_book(title, 5)
            for similar_book in similar_books:
                new_cost = cost + int(similar_book["purchasePrice"])
                if new_cost < int(budget):
                    book_list.append(similar_book)
                    cost += int(similar_book["purchasePrice"])
        return book_list, cost
