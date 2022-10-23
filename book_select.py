# https://towardsdatascience.com/using-cosine-similarity-to-build-a-movie-recommendation-system-ae7f20842599
from database import Database
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class Select(Database):
    
    def __init__(self, parent):
        self.parent = parent
        sql_query = pd.read_sql_query ('''
            SELECT book.id, authors.authorName, book.genre, book.title
            FROM book
            INNER JOIN authors
            ON book.authorID=authors.id;
            ''',self.parent.conn)
        self.df = pd.DataFrame(sql_query)
        self.features = self.df[['title','authorName','genre']].astype(str).agg(' '.join,axis=1)
        self.create_count_matrix()
        
    def create_count_matrix(self):
        cv = CountVectorizer()
        self.count_matrix = cv.fit_transform(self.features) 
        
    def get_cosine_similarity(self, index):
        cosine_sim = cosine_similarity(self.count_matrix)
        similar_books = list(enumerate(cosine_sim[index]))
        return sorted(similar_books, key=lambda x:x[1], reverse=True)
        
    def get_similar_books(self, title):
        books = []
        index = self.get_index(title)
        similar_books = self.get_cosine_similarity(index)
        count = 1
        
        for book in similar_books[1:6]:
            title = self.get_title_from_index(book[0])
            books.append(title)
            
        return books
        
    def get_index(self, book_title):
        return self.df.loc[self.df['title'] == book_title].index[0]
        
    def get_title_from_index(self, index):
        return self.df.loc[self.df.index == index]['title'].values[0]
        
        

   
                
        
