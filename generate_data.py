import requests

API_URL = "https://www.googleapis.com/books/v1/volumes?q=cars"
books = []


book_data = requests.get(API_URL).json()
book_count = 1
for book in book_data['items']:
    if not book['volumeInfo']['categories']:
        continue
    book_string = f"{book_count},{book['volumeInfo']['title']},{book['volumeInfo']['categories']}"
    books.append(book_string)
    print(book_string)
    book_count += 1

print(books)
