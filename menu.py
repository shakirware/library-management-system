#https://github.com/Just-Moh-it/HotinGo
#https://www.clickminded.com/button-generator/
#https://coolors.co/c9cad9-d1d2f9-a3bcf9-7796cb-576490
#
import tkinter as tk
from tkinter import (
    Toplevel,
    Frame,
    Canvas,
    Button,
    PhotoImage,
    messagebox,
    StringVar,
    Entry,
    Listbox
)

from database import Database
from book_search import Search
from book_checkout import Checkout
from book_return import Return
from book_select import Select

class MainWindow(Toplevel):

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.title("Library Management System")
        self.geometry("1012x506")
        self.current_window = None
        
        self.database = Database()
        self.search = Search(self.database)
        self.checkout = Checkout(self.database)
        self.return_ = Return(self.database)
        self.select = Select(self.database)


        self.bind("<ButtonPress-1>", lambda event: self.capture(True))
        self.bind("<ButtonRelease-1>", lambda event: self.capture(False))
        

        self.canvas = Canvas(
            self,
            bg="#16262E",
            height=506,
            width=1012,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)

        # Side panel 
        self.canvas.create_rectangle(
            215, 0.0, 1012.0, 506.0, outline=""
        )

        # Home Button
        self.button_image_1 = PhotoImage(file="./assets/button_home.png")
        self.home_btn = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press("home"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",

        )
        self.home_btn.place(x=6.0, y=30.0, width=200.0, height=50.0)

        # Search Button
        self.button_image_2 = PhotoImage(file="./assets/button_search.png")
        self.search_btn = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press("search"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",

        )
        self.search_btn.place(x=6.0, y=100.0, width=200.0, height=50.0)

        # Return Button
        self.button_image_3 = PhotoImage(file="./assets/button_return.png")
        self.return_btn = Button(
            self.canvas,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press("return"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",

        )
        self.return_btn.place(x=6.0, y=170.0, width=200.0, height=50.0)

        # Select Button
        self.button_image_4 = PhotoImage(file="./assets/button_select.png")
        self.select_btn = Button(
            self.canvas,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press("select"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",

        )
        self.select_btn.place(x=6.0, y=240.0, width=200.0, height=50.0)

        # checkout Button
        self.button_image_5 = PhotoImage(file="./assets/button_checkout.png")
        self.checkout_btn = Button(
            self.canvas,
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press("checkout"),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",

        )
        self.checkout_btn.place(x=6.0, y=310.0, width=200.0, height=50.0)


        self.windows = {
            "home": HomeFrame(self),
            "search": SearchFrame(self),
            "return": ReturnFrame(self),
            "select": SelectFrame(self),
            "checkout": CheckoutFrame(self)
        }

        self.handle_btn_press("home")

        
        self.current_window.place(x=215, y=0, width=1013.0, height=506.0)

        
    def motion(self, event):
            x, y = event.x, event.y
            print('{}, {}'.format(x, y))

    def capture(self, flag):
        if flag:
            self.bind('<Motion>', self.motion)
        else:
            self.unbind('<Motion>')    
            
    def clear_listbox(self, listbox):
        listbox.delete('0', tk.END)

    def handle_btn_press(self, name):
            # Hide all screens
            for window in self.windows.values():
                window.place_forget()

            # Set current Window
            self.current_window = self.windows.get(name)

            # Show the screen of the button pressed
            self.windows[name].place(x=215, y=0, width=1013.0, height=506.0)


class HomeFrame(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.canvas = Canvas(
            self,
            bg="#2E4756",
            height=506,
            width=797,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)
        
        
        # current book count
        self.canvas.image_1 = PhotoImage(file="./assets/bg_1.png")
        self.canvas.create_image(115.0, 81.0, image=self.canvas.image_1)
        self.canvas.create_text(
            56.0,
            45.0,
            anchor="nw",
            text="Book Count",
            fill="#16262e",
            font=("Open Sans", 14, 'bold'),
        )
        self.canvas.create_text(
            164.0,
            63.0,
            anchor="ne",
            text=self.parent.database.get_book_copies_count(),
            fill="#16262e",
            font=("Open Sans", 30, 'bold'),
        )
        # books on loan
        self.canvas.create_image(299.0, 81.0, image=self.canvas.image_1)
        self.canvas.create_text(
            240.0,
            45.0,
            anchor="nw",
            text="On Loan",
            fill="#16262e",
            font=("Open Sans", 14, 'bold'),
        )
        self.canvas.create_text(
            346.0,
            63.0,
            anchor="ne",
            text=self.parent.database.get_books_loan_count(),
            fill="#16262e",
            font=("Open Sans", 30, 'bold'),
        )
        # reserved books
        self.canvas.create_image(483.0, 81.0, image=self.canvas.image_1)
        self.canvas.create_text(
            424.0,
            45.0,
            anchor="nw",
            text="Reserved",
            fill="#16262e",
            font=("Open Sans", 14, 'bold'),
        )
        self.canvas.create_text(
            540.0,
            63.0,
            anchor="ne",
            text=self.parent.database.get_books_resv_count(),
            fill="#16262e",
            font=("Open Sans", 30, 'bold'),
        )
        #unique books
        self.canvas.create_image(667.0, 81.0, image=self.canvas.image_1)
        self.canvas.create_text(
            608.0,
            45.0,
            anchor="nw",
            text="Unique Books",
            fill="#16262e",
            font=("Open Sans", 14, 'bold'),
        )
        self.canvas.create_text(
            712.0,
            63.0,
            anchor="ne",
            text=self.parent.database.get_book_count(),
            fill="#16262e",
            font=("Open Sans", 30, 'bold'),
        )
        
        # icon 1
        self.canvas.image_2 = PhotoImage(file="./assets/icon.png")
        self.canvas.create_image(670.0, 330.0, image=self.canvas.image_2)
        
        # icon 2
        self.canvas.image_3 = PhotoImage(file="./assets/icon1.png")
        self.canvas.create_image(140.0, 330.0, image=self.canvas.image_3)
        
        # icon 3
        self.canvas.image_4 = PhotoImage(file="./assets/icon2.png")
        self.canvas.create_image(390.0, 330.0, image=self.canvas.image_4)


class SearchFrame(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.canvas = Canvas(
            self,
            bg="#2E4756",
            height=506,
            width=797,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)
        
        self.entry_image_1 = PhotoImage(file="./assets/bg_2.png")
        self.entry_bg_1 = self.canvas.create_image(180.0, 150.0, image=self.entry_image_1)
        
        self.canvas.create_text(
            75.0,
            65.0,
            anchor="nw",
            text="Book Title",
            fill="#3c7a89",
            font=("Open Sans", 15, 'bold'),
        )
        self.title_entry = Entry(
            self.canvas,
            bd=0,
            bg="#e3e3e3",
            highlightthickness=0,
            font=("Open Sans", 15, 'bold'),
            foreground="#16262e",
        )
        self.title_entry.place(x=75.0, y=90.0, width=230, height=37)
        
        self.canvas.create_text(
            75.0,
            130.0,
            anchor="nw",
            text="Book Author",
            fill="#3c7a89",
            font=("Open Sans", 15, 'bold'),
        )
        self.author_entry = Entry(
            self.canvas,
            bd=0,
            bg="#e3e3e3",
            highlightthickness=0,
            font=("Open Sans", 15, 'bold'),
            foreground="#16262e",
        )
        self.author_entry.place(x=75.0, y=155.0, width=230, height=37)
        
        self.listbox = Listbox(self, width=60, height=20, activestyle='none', foreground='#3c7a89', bd=0)
        self.listbox.place(x=370.0, y=40.0)
        
        
        self.button_image_1 = PhotoImage(file="./assets/button_clear.png")
        self.clear_btn = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.clear_listbox(self.listbox),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        self.clear_btn.place(x=450.0, y=400.0, width=200.0, height=50.0)
        
        self.button_image_2 = PhotoImage(file="./assets/button_submit.png")
        self.submit_btn = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.search(self.title_entry.get(), self.author_entry.get()),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        self.submit_btn.place(x=80.0, y=290.0, width=200.0, height=50.0)
        
        self.canvas.image_1 = PhotoImage(file="./assets/icon4.png")
        self.canvas.create_image(190.0, 420.0, image=self.canvas.image_1)

    def search(self, title, author):
        self.parent.clear_listbox(self.listbox)
        if title and author:
            books = self.parent.search.book_title_author_search(title, author)
            for book in books:
                self.listbox.insert(tk.END, book[0])
        elif title:
            books = self.parent.search.book_title_search(title)
            for book in books:
                self.listbox.insert(tk.END, book[0])
        elif author:
            authors = self.parent.search.book_author_search(author)
            for author in authors:
                print(author[0])
                self.listbox.insert(tk.END, author[0])

        

class ReturnFrame(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.canvas = Canvas(
            self,
            bg="#2E4756",
            height=506,
            width=797,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)
        
        self.entry_image_1 = PhotoImage(file="./assets/entry_1.png")
        self.entry_bg_1 = self.canvas.create_image(200.0, 70.0, image=self.entry_image_1)
        
        self.canvas.create_text(
            45.0,
            40.0,
            anchor="nw",
            text="Insert Book ID",
            fill="#3c7a89",
            font=("Open Sans", 15, 'bold'),
        )
        self.book_entry = Entry(
            self.canvas,
            bd=0,
            bg="#e3e3e3",
            highlightthickness=0,
            font=("Open Sans", 15, 'bold'),
            foreground="#16262e",
        )
        self.book_entry.place(x=35.0, y=65.0, width=230, height=37)
        
        self.button_image_1 = PhotoImage(file="./assets/button_submit.png")
        self.submit_btn = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.return_book(self.book_entry.get()),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        self.submit_btn.place(x=20.0, y=120.0, width=200.0, height=50.0)
        
        self.entry_image_2 = PhotoImage(file="./assets/bg_2.png")
        self.entry_bg_2 = self.canvas.create_image(155.0, 380.0, image=self.entry_image_2)
        
        self.textbox = self.canvas.create_text(
            40.0,
            300.0,
            anchor="nw",
            text="",
            fill="#FF0000",
            width=250,
            font=("Open Sans", 10, 'bold'),
        )
        
        self.textbox1 = self.canvas.create_text(
            40.0,
            360.0,
            anchor="nw",
            text="",
            fill="#FF0000",
            width=250,
            font=("Open Sans", 10, 'bold'),
        )
        
        self.canvas.image_1 = PhotoImage(file="./assets/icon3.png")
        self.canvas.create_image(600.0, 330.0, image=self.canvas.image_1)
        
        
 
    def return_book(self, book_id):
        result, text = self.parent.return_.return_book(book_id)
        self.canvas.itemconfigure(self.textbox1, text="")
        if result:
            self.canvas.itemconfigure(self.textbox, text=text, fill="#00FF00")
            result, text = self.parent.return_.is_book_reserved(book_id)
            if result:
                self.canvas.itemconfigure(self.textbox1, text=text, fill="#FF0000")
        else:
            self.canvas.itemconfigure(self.textbox, text=text, fill="#00FF00")
            
    
           
        

class SelectFrame(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.canvas = Canvas(
            self,
            bg="#2E4756",
            height=506,
            width=797,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)
        
        self.entry_image_1 = PhotoImage(file="./assets/entry_1.png")
        self.entry_bg_1 = self.canvas.create_image(200.0, 70.0, image=self.entry_image_1)
        
        self.canvas.create_text(
            45.0,
            40.0,
            anchor="nw",
            text="Insert Budget",
            fill="#3c7a89",
            font=("Open Sans", 15, 'bold'),
        )
        self.budget_entry = Entry(
            self.canvas,
            bd=0,
            bg="#e3e3e3",
            highlightthickness=0,
            font=("Open Sans", 15, 'bold'),
            foreground="#16262e",
        )
        self.budget_entry.place(x=35.0, y=65.0, width=230, height=37)
        
        self.listbox = Listbox(self, width=50, height=20, activestyle='none', foreground='#3c7a89', bd=0)
        self.listbox.place(x=405.0, y=40.0)
        
        self.button_image_1 = PhotoImage(file="./assets/button_clear.png")
        self.clear_btn = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.clear(),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        self.clear_btn.place(x=450.0, y=400.0, width=200.0, height=50.0)
        
        self.button_image_2 = PhotoImage(file="./assets/button_submit.png")
        self.submit_btn = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.select(self.budget_entry.get()),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        self.submit_btn.place(x=30.0, y=140.0, width=200.0, height=50.0)
        
        self.canvas.image_1 = PhotoImage(file="./assets/icon6.png")
        self.canvas.create_image(150.0, 400.0, image=self.canvas.image_1)
        
    def select(self, budget):
        self.parent.clear_listbox(self.listbox)
        book_list, cost = self.parent.select.recommend_books(budget)
        
        if not hasattr(self, 'text'):
            self.text = self.canvas.create_text(
            490.0,
            370.0,
            anchor="nw",
            text=f"Total Cost £{cost}",
            fill="#FF0000",
            font=("Open Sans", 15, 'bold'),
        )
            
        self.canvas.itemconfigure(self.text, text=f"Total Cost £{cost}")

        for book in book_list:
            string = f"{book['title']} by {book['authorName']} - {book['genre']}"
            self.listbox.insert(tk.END, string)
        
    def clear(self):
        self.parent.clear_listbox(self.listbox)
        self.canvas.itemconfigure(self.text, text="")

class CheckoutFrame(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.canvas = Canvas(
            self,
            bg="#2E4756",
            height=506,
            width=797,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )
        
        self.canvas.place(x=0, y=0)
        
        self.entry_image_1 = PhotoImage(file="./assets/bg_2.png")
        self.entry_bg_1 = self.canvas.create_image(180.0, 150.0, image=self.entry_image_1)
        
        self.canvas.create_text(
            75.0,
            65.0,
            anchor="nw",
            text="Member ID",
            fill="#3c7a89",
            font=("Open Sans", 15, 'bold'),
        )
        self.member_entry = Entry(
            self.canvas,
            bd=0,
            bg="#e3e3e3",
            highlightthickness=0,
            font=("Open Sans", 15, 'bold'),
            foreground="#16262e",
        )
        self.member_entry.place(x=75.0, y=90.0, width=230, height=37)
        
        self.canvas.create_text(
            75.0,
            130.0,
            anchor="nw",
            text="Book ID",
            fill="#3c7a89",
            font=("Open Sans", 15, 'bold'),
        )
        self.book_entry = Entry(
            self.canvas,
            bd=0,
            bg="#e3e3e3",
            highlightthickness=0,
            font=("Open Sans", 15, 'bold'),
            foreground="#16262e",
        )
        self.book_entry.place(x=75.0, y=155.0, width=230, height=37)
        
        self.button_image_2 = PhotoImage(file="./assets/button_submit.png")
        self.submit_btn = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.checkout(self.member_entry.get(), self.book_entry.get()),
            cursor='hand2', activebackground="#5E95FF",
            relief="flat",
        )
        self.submit_btn.place(x=80.0, y=290.0, width=200.0, height=50.0)
        
        self.entry_image_2 = PhotoImage(file="./assets/bg_2.png")
        self.entry_bg_2 = self.canvas.create_image(600.0, 145.0, image=self.entry_image_2)
        
        self.textbox = self.canvas.create_text(
            525.0,
            150.0,
            anchor="nw",
            text="",
            fill="#FF0000",
            width=250,
            font=("Open Sans", 10, 'bold'),
        )
        
        self.canvas.image_1 = PhotoImage(file="./assets/icon5.png")
        self.canvas.create_image(600.0, 400.0, image=self.canvas.image_1)
        
    def checkout(self, member_id, book_id):
        member_id = int(member_id)
        book_id = int(book_id)
        book_valid = self.parent.checkout.is_book_valid(book_id)
        member_valid = self.parent.checkout.is_member_valid(member_id)
        self.canvas.itemconfigure(self.textbox, text="")
        
        if not member_valid:
            self.canvas.itemconfigure(self.textbox, text="Member ID is invalid.")
        elif not book_valid:
            self.canvas.itemconfigure(self.textbox, text="Book ID is invalid.")
        else:
            result, text = withdraw(book_id, member_id)
            if result:
                self.canvas.itemconfigure(self.textbox, text=text)
            else:
                # would you like to reserve a book?
                self.canvas.itemconfigure(self.textbox, text=text)
                            
            
        

root = tk.Tk()
root.withdraw()  

MainWindow()
root.mainloop()