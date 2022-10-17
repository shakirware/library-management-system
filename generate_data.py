import requests

API_URL = "https://www.googleapis.com/books/v1/volumes?q=cars"
book_list = []


def get_book_data(url):
    return requests.get(url).json()


def parse_item(item, book_count) -> str:
    if "categories" in item["volumeInfo"] and "retailPrice" in item["saleInfo"]:
        return (
            f"{book_count},{item['volumeInfo']['categories'][0]},"
            f"{item['volumeInfo']['title']},{item['volumeInfo']['authors'][0]},"
            f"${item['saleInfo']['retailPrice']['amount']}"
        )
    return None


def parse_books(books):
    book_count = 1
    for book in books["items"]:
        book_string = parse_item(book, book_count)
        if book_string is not None:
            book_list.append(book_string)
            book_count += 1


def save_books(filename):
    with open(filename, "w", encoding="UTF-8") as file_:
        for line in file_:
            file_.write("\n".join(line))


def main():
    book_data = get_book_data(API_URL)
    parse_books(book_data)
    print(book_list)


main()
