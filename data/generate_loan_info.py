import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

used_books = []
loan_list = []
COUNT = 150
num_lines = sum(1 for line in open('Book_Info.txt', encoding='utf-8'))

def generate_date(reserve=None):
    today = datetime.today()
    if reserve:
        start = today + relativedelta(months=+1)
        end = today + relativedelta(months=+3)
    else:
        start = today - relativedelta(months=+2)
        end = today
        
    random_number_of_days = random.randrange((end - start).days)
    date = start + timedelta(days=random_number_of_days)
    return date.strftime('%Y-%m-%d')

for i in range(COUNT):

    probability = random.random()
    member_id = random.randint(1111,1222)
    
    book_id = random.randint(1, num_lines)
    while book_id in used_books:
        book_id = random.randint(1, num_lines)
        used_books.append(book_id)

    if probability < 0.3:
        random_number = random.randint(1,3)
        for i in range(random_number):
            resv_date = None
            checkout_date = generate_date()
            return_date = generate_date()
            loan_list.append(f'{book_id}|{resv_date}|{checkout_date}|{return_date}|{member_id}')
    elif 0.3 < probability < 0.6:
        resv_date = None
        checkout_date = generate_date()
        return_date = None
        loan_list.append(f'{book_id}|{resv_date}|{checkout_date}|{return_date}|{member_id}')
    else: 
        resv_date = generate_date(reserve=True)
        checkout_date = None
        return_date = None
        loan_list.append(f'{book_id}|{resv_date}|{checkout_date}|{return_date}|{member_id}')
        
with open("Loan_Reservation_History.txt", "w", encoding="utf-8") as file_:
    file_.write("\n".join(loan_list))     
