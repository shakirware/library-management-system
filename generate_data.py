import random
import datetime
from datetime import date
import time
import requests
from dateutil.relativedelta import relativedelta

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
            f"{book_count}|{item['volumeInfo']['categories'][0]}|"
            f"{item['volumeInfo']['title']}|{item['volumeInfo']['authors'][0]}|"
            f"${item['saleInfo']['retailPrice']['amount']}|{generate_date()}"
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

def generate_date(reserve=None):
    today = date.today()
    if reserve:
        start = today + relativedelta(months=+1)
        end = today + relativedelta(months=+3)
    else:
        start = today - relativedelta(months=+2)
        end = today
        
    random_number_of_days = random.randrange((end - start).days)
    return start + datetime.timedelta(days=random_number_of_days)
    

def generate_books(keywords):
    for keyword in keywords:
        book_data = get_book_data(
            f"https://www.googleapis.com/books/v1/volumes?q={keyword}&maxResults=40"
        )
        parse_books(book_data)
        save_file("Book_Info.txt", book_list)

def generate_loans(amount):
    used_books = []
    for i in range(1, amount):
        probability = random.random()
        
        book_id = random.randint(1,len(book_list))
        while book_id in used_books:
            book_id = random.randint(1,len(book_list))
        used_books.append(book_id)
        
        if probability < 0.5:
            for i in range(random.randint(1,5)):
                resv_date = None
                checkout_date = generate_date()
                return_date = generate_date()
                member_id = random.randint(1111,1222)
                loan_list.append(f'{book_id}|{resv_date}|{checkout_date}|{return_date}|{member_id}')  
        elif 0.5 < probability < 0.7:
            resv_date = None
            checkout_date = generate_date()
            return_date = None
            member_id = random.randint(1111,1222)
            loan_list.append(f'{book_id}|{resv_date}|{checkout_date}|{return_date}|{member_id}')
        else:
            resv_date = generate_date(reserve=True)
            checkout_date = None
            return_date = None
            member_id = random.randint(1111,1222)
            loan_list.append(f'{book_id}|{resv_date}|{checkout_date}|{return_date}|{member_id}')
            
    save_file("Loan_Reservation_History.txt", loan_list)
    

def main():
    generate_books(keywords)
    generate_loans(100)

main()
