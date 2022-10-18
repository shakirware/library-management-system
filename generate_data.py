import random
import datetime
import time
import requests

book_list = []
loan_list = []
book_count = 1

keywords = [
        "harry",
        "eagles",
        "boats",
        "cars",
        "people",
        "sea",
        "ocean",
        "england",
        "building",
        "houses",
        "london",
        "note",
        "grapeboy",
        "connection",
        "eletric",
        "maths",
        "physics",
    ]

def get_book_data(url):
    return requests.get(url).json()

def parse_item(item) -> str:
    if (
        all(x in item["volumeInfo"] for x in ["categories", "authors"])
        and "retailPrice" in item["saleInfo"]
    ):
        return (
            f"{book_count},{item['volumeInfo']['categories'][0]},"
            f"{item['volumeInfo']['title']},{item['volumeInfo']['authors'][0]},"
            f"${item['saleInfo']['retailPrice']['amount']},{random_date()}"
        )
    return None

def parse_books(books):
    global book_count
    for book in books["items"]:
        book_string = parse_item(book)
        if book_string is not None:
            book_list.append(book_string)
            book_count += 1
        
def save_file(filename, array):
    with open(filename, "w", encoding="UTF-8") as file_:
        file_.write("\n".join(array))

def random_date():
    start = datetime.date(2019, 2, 1)
    time_between_dates = datetime.date(2022, 9, 1) - start
    random_number_of_days = random.randrange(time_between_dates.days)
    return start + datetime.timedelta(days=random_number_of_days)

def loan_string():
    return f'{random.randint(1,len(book_list))},{random_date()},{random_date()},{random.randint(1111,2222)}'

def generate_books(keywords):
    for keyword in keywords:
        book_data = get_book_data(
            f"https://www.googleapis.com/books/v1/volumes?q={keyword}&maxResults=40"
        )
        parse_books(book_data)
        save_file("Book_Info.txt", book_list)

def generate_loans(amount):
    for i in range(1, amount):
        loan_list.append(loan_string())
    save_file("Loan_Reservation_History.txt", loan_list)
    

def main():
    generate_books(keywords)
    generate_loans(200)

main()
