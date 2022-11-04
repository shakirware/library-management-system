# https://github.com/Just-Moh-it/HotinGo
# https://www.clickminded.com/button-generator/
# https://coolors.co/c9cad9-d1d2f9-a3bcf9-7796cb-576490
#
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import (
    Toplevel,
    Frame,
    Canvas,
    Button,
    PhotoImage,
    messagebox,
    StringVar,
    Entry,
    Listbox,
    Checkbutton,
    IntVar,
    Label,
)

from database import Database
from book_search import Search
from book_checkout import Checkout
from book_return import Return
from book_select import Select
from PIL import Image, ImageTk
from datetime import datetime, timedelta


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
        self.canvas.create_rectangle(215, 0.0, 1012.0, 506.0, outline="")

        # Home Button
        self.button_image_1 = PhotoImage(file="./assets/button_home.png")
        self.home_btn = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press("home"),
            cursor="hand2",
            activebackground="#5E95FF",
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
            cursor="hand2",
            activebackground="#5E95FF",
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
            cursor="hand2",
            activebackground="#5E95FF",
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
            cursor="hand2",
            activebackground="#5E95FF",
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
            cursor="hand2",
            activebackground="#5E95FF",
            relief="flat",
        )
        self.checkout_btn.place(x=6.0, y=310.0, width=200.0, height=50.0)
        
        # quit Button
        self.button_image_6 = PhotoImage(file="./assets/button_quit.png")
        self.checkout_btn = Button(
            self.canvas,
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.quit_app(),
            cursor="hand2",
            activebackground="#5E95FF",
            relief="flat",
        )
        self.checkout_btn.place(x=6.0, y=380.0, width=200.0, height=50.0)

        self.windows = {
            "home": HomeFrame(self),
            "search": SearchFrame(self),
            "return": ReturnFrame(self),
            "select": SelectFrame(self),
            "checkout": CheckoutFrame(self)
        }

        self.handle_btn_press("home")

        self.current_window.place(x=215, y=0, width=1013.0, height=506.0)
    
    def quit_app(self):
        root.quit()

    def clear_listbox(self, listbox):
        listbox.delete("0", tk.END)

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
            font=("Open Sans", 14, "bold"),
        )
        self.canvas.create_text(
            164.0,
            63.0,
            anchor="ne",
            text=self.parent.database.get_book_copies_count(),
            fill="#16262e",
            font=("Open Sans", 30, "bold"),
        )
        # books on loan
        self.canvas.create_image(299.0, 81.0, image=self.canvas.image_1)
        self.canvas.create_text(
            240.0,
            45.0,
            anchor="nw",
            text="On Loan",
            fill="#16262e",
            font=("Open Sans", 14, "bold"),
        )
        self.canvas.create_text(
            346.0,
            63.0,
            anchor="ne",
            text=self.parent.database.get_books_loan_count(),
            fill="#16262e",
            font=("Open Sans", 30, "bold"),
        )
        # reserved books
        self.canvas.create_image(483.0, 81.0, image=self.canvas.image_1)
        self.canvas.create_text(
            424.0,
            45.0,
            anchor="nw",
            text="Reserved",
            fill="#16262e",
            font=("Open Sans", 14, "bold"),
        )
        self.canvas.create_text(
            540.0,
            63.0,
            anchor="ne",
            text=self.parent.database.get_books_resv_count(),
            fill="#16262e",
            font=("Open Sans", 30, "bold"),
        )
        # unique books
        self.canvas.create_image(667.0, 81.0, image=self.canvas.image_1)
        self.canvas.create_text(
            608.0,
            45.0,
            anchor="nw",
            text="Unique Books",
            fill="#16262e",
            font=("Open Sans", 14, "bold"),
        )
        self.canvas.create_text(
            712.0,
            63.0,
            anchor="ne",
            text=self.parent.database.get_book_count(),
            fill="#16262e",
            font=("Open Sans", 30, "bold"),
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
        self.c_array = []

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
        self.entry_bg_1 = self.canvas.create_image(
            180.0, 150.0, image=self.entry_image_1
        )

        self.canvas.create_text(
            75.0,
            65.0,
            anchor="nw",
            text="Book Title",
            fill="#3c7a89",
            font=("Open Sans", 15, "bold"),
        )

        titlesv = StringVar()
        titlesv.trace(
            "w",
            lambda name, index, mode, titlesv=titlesv: self.search(
                self.title_entry.get(), self.author_entry.get()
            ),
        )

        self.title_entry = Entry(
            self.canvas,
            bd=0,
            bg="#e3e3e3",
            highlightthickness=0,
            font=("Open Sans", 15, "bold"),
            foreground="#16262e",
            textvariable=titlesv,
        )
        self.title_entry.place(x=75.0, y=90.0, width=230, height=37)

        self.canvas.create_text(
            75.0,
            130.0,
            anchor="nw",
            text="Book Author",
            fill="#3c7a89",
            font=("Open Sans", 15, "bold"),
        )

        authorsv = StringVar()
        authorsv.trace(
            "w",
            lambda name, index, mode, authorsv=authorsv: self.search(
                self.title_entry.get(), self.author_entry.get()
            ),
        )

        self.author_entry = Entry(
            self.canvas,
            bd=0,
            bg="#e3e3e3",
            highlightthickness=0,
            font=("Open Sans", 15, "bold"),
            foreground="#16262e",
            textvariable=authorsv,
        )
        self.author_entry.place(x=75.0, y=155.0, width=230, height=37)

        # list of checkbox
        self.text = ScrolledText(self, width=40, height=12, pady=60)
        self.text.place(x=360.0, y=40.0)

        self.button_image_3 = PhotoImage(file="./assets/button_clear_1.png")
        self.clear_btn = Button(
            self.canvas,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.clear(),
            cursor="hand2",
            activebackground="#5E95FF",
            relief="flat",
        )
        self.clear_btn.place(x=600.0, y=380.0, width=100.0, height=50.0)

        self.button_image_4 = PhotoImage(file="./assets/button_return_1.png")
        self.return_btn = Button(
            self.canvas,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.do_returns(),
            cursor="hand2",
            activebackground="#5E95FF",
            relief="flat",
        )
        self.return_btn.place(x=480.0, y=380.0, width=100.0, height=50.0)

        self.button_image_2 = PhotoImage(file="./assets/button_submit.png")
        self.submit_btn = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.search(
                self.title_entry.get(), self.author_entry.get()
            ),
            cursor="hand2",
            activebackground="#5E95FF",
            relief="flat",
        )
        self.submit_btn.place(x=80.0, y=290.0, width=200.0, height=50.0)

        self.canvas.image_1 = PhotoImage(file="./assets/icon4.png")
        self.canvas.create_image(190.0, 415.0, image=self.canvas.image_1)

        self.statusvar = StringVar()
        self.statusvar.set("Ready")
        self.sbar = Label(
            self, textvariable=self.statusvar, relief=tk.SUNKEN, anchor="w"
        )
        self.sbar.pack(side=tk.BOTTOM, fill=tk.X)

    def search(self, title, author):
        self.clear()
        books = None
        if title and author:
            books = self.parent.search.book_title_author_search(title, author)
            for book in books:
                self.add_item(book[0], book[1])
        elif title:
            books = self.parent.search.book_title_search(title)
            for book in books:
                self.add_item(book[0], book[1])
        elif author:
            books = self.parent.search.book_author_search(author)
            for book in books:
                self.add_item(book[0], book[1])
        if books:
            self.statusvar.set(f"{len(books)} records have been found and returned.")
            self.sbar.update()

    def do_returns(self):
        id_array = []
        for var, book_id in self.c_array:
            if var.get():
                id_array.append(book_id)

        if not id_array:
            self.statusvar.set("Nothing has been selected.")
            self.sbar.update()
        else:
            book_r, book_a = self.parent.return_.return_books(id_array)
            self.statusvar.set(
                f"RETURNED BOOK ID: {book_r} BOOK ID ALREADY AVAILABLE: {book_a}"
            )
            self.sbar.update()

    def add_item(self, book_id, title):
        is_checked = IntVar()
        text = f"{book_id} - {title}"
        button = Checkbutton(
            self, text=text, bg="white", anchor="w", variable=is_checked, wraplength=300
        )
        self.text.window_create("end", window=button)
        self.text.insert("end", "\n")
        self.c_array.append((is_checked, book_id))

    def clear(self):
        self.text.delete("1.0", "end")
        self.statusvar.set("List has been cleared.")
        self.sbar.update()


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
        self.entry_bg_1 = self.canvas.create_image(
            200.0, 70.0, image=self.entry_image_1
        )

        self.canvas.create_text(
            45.0,
            40.0,
            anchor="nw",
            text="Insert Book ID",
            fill="#3c7a89",
            font=("Open Sans", 15, "bold"),
        )
        self.book_entry = Entry(
            self.canvas,
            bd=0,
            bg="#e3e3e3",
            highlightthickness=0,
            font=("Open Sans", 15, "bold"),
            foreground="#16262e",
        )
        self.book_entry.place(x=35.0, y=65.0, width=335, height=37)

        self.button_image_1 = PhotoImage(file="./assets/button_submit.png")
        self.submit_btn = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.return_book(self.book_entry.get()),
            cursor="hand2",
            activebackground="#5E95FF",
            relief="flat",
        )
        self.submit_btn.place(x=20.0, y=120.0, width=200.0, height=50.0)

        self.canvas.image_1 = PhotoImage(file="./assets/icon3.png")
        self.canvas.create_image(600.0, 330.0, image=self.canvas.image_1)

        self.statusvar = StringVar()
        self.statusvar.set("Ready")
        self.sbar = Label(
            self, textvariable=self.statusvar, relief=tk.SUNKEN, anchor="w"
        )
        self.sbar.pack(side=tk.BOTTOM, fill=tk.X)

    def return_book(self, book_id):
        if "," in book_id:
            array_id = book_id.split(",")
            book_r, book_a = self.parent.return_.return_books(array_id)
            self.statusvar.set(
                f"RETURNED BOOK ID: {book_r} BOOK ID ALREADY AVAILABLE: {book_a}"
            )
            self.sbar.update()
        else:
            returned, text = self.parent.return_.return_book(book_id)
            if returned:
                return_text = text
                self.statusvar.set(return_text)
                self.sbar.update()
                is_reserved, text = self.parent.return_.is_book_reserved(book_id)
                if is_reserved:
                    reserved_text = text
                    self.statusvar.set(f"{return_text}  {reserved_text}")
                    self.sbar.update()
            else:
                self.statusvar.set(text)
                self.sbar.update()


class SelectFrame(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.graph = None

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
        self.entry_bg_1 = self.canvas.create_image(
            200.0, 70.0, image=self.entry_image_1
        )

        self.canvas.create_text(
            45.0,
            40.0,
            anchor="nw",
            text="Insert Budget",
            fill="#3c7a89",
            font=("Open Sans", 15, "bold"),
        )
        self.budget_entry = Entry(
            self.canvas,
            bd=0,
            bg="#e3e3e3",
            highlightthickness=0,
            font=("Open Sans", 15, "bold"),
            foreground="#16262e",
        )
        self.budget_entry.place(x=35.0, y=65.0, width=335, height=37)

        # change this

        self.text = ScrolledText(self, width=40, height=20)
        self.text.place(x=400.0, y=40.0)

        self.button_image_1 = PhotoImage(file="./assets/button_clear.png")
        self.clear_btn = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.clear(),
            cursor="hand2",
            activebackground="#5E95FF",
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
            cursor="hand2",
            activebackground="#5E95FF",
            relief="flat",
        )
        self.submit_btn.place(x=30.0, y=140.0, width=200.0, height=50.0)

        self.canvas.image_1 = PhotoImage(file="./assets/icon6.png")
        self.canvas.create_image(150.0, 400.0, image=self.canvas.image_1)

        self.statusvar = StringVar()
        self.statusvar.set("Ready")
        self.sbar = Label(
            self, textvariable=self.statusvar, relief=tk.SUNKEN, anchor="w"
        )
        self.sbar.pack(side=tk.BOTTOM, fill=tk.X)

    def select(self, budget):
        self.clear()
        book_list, cost = self.parent.select.recommend_new_books(budget)
        msg_more_copies = self.parent.select.rec_more_copies()
        msg = f'The total cost of the following {len(book_list)} books is £{cost}. '
        
        self.statusvar.set(msg + msg_more_copies)
        self.sbar.update()

        for book in book_list:
            string = f"{book['title']} by {book['authorName']} - {book['genre']} \n\n\n"
            self.text.insert(tk.INSERT, string)

        image = Image.open("./assets/books_similarity.png")
        resize_image = image.resize((250, 250))
        self.canvas.image_2 = ImageTk.PhotoImage(resize_image)
        self.graph = self.canvas.create_image(150.0, 350.0, image=self.canvas.image_2)

    def clear(self):
        self.canvas.delete(self.graph)
        self.text.delete("1.0", "end")
        self.statusvar.set("List has been cleared.")
        self.sbar.update()


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
        self.entry_bg_1 = self.canvas.create_image(
            180.0, 150.0, image=self.entry_image_1
        )

        self.canvas.create_text(
            75.0,
            65.0,
            anchor="nw",
            text="Member ID",
            fill="#3c7a89",
            font=("Open Sans", 15, "bold"),
        )
        self.member_entry = Entry(
            self.canvas,
            bd=0,
            bg="#e3e3e3",
            highlightthickness=0,
            font=("Open Sans", 15, "bold"),
            foreground="#16262e",
        )
        self.member_entry.place(x=75.0, y=90.0, width=230, height=37)

        self.canvas.create_text(
            75.0,
            130.0,
            anchor="nw",
            text="Book ID",
            fill="#3c7a89",
            font=("Open Sans", 15, "bold"),
        )
        self.book_entry = Entry(
            self.canvas,
            bd=0,
            bg="#e3e3e3",
            highlightthickness=0,
            font=("Open Sans", 15, "bold"),
            foreground="#16262e",
        )
        self.book_entry.place(x=75.0, y=155.0, width=230, height=37)

        self.button_image_2 = PhotoImage(file="./assets/button_submit.png")
        self.submit_btn = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.checkout(
                self.member_entry.get(), self.book_entry.get()
            ),
            cursor="hand2",
            activebackground="#5E95FF",
            relief="flat",
        )
        self.submit_btn.place(x=80.0, y=290.0, width=200.0, height=50.0)

        self.canvas.image_1 = PhotoImage(file="./assets/icon5.png")
        self.canvas.create_image(600.0, 400.0, image=self.canvas.image_1)

        self.statusvar = StringVar()
        self.statusvar.set("Ready")
        self.sbar = Label(
            self, textvariable=self.statusvar, relief=tk.SUNKEN, anchor="w"
        )
        self.sbar.pack(side=tk.BOTTOM, fill=tk.X)

    def checkout(self, member_id, book_id):
        member_id, book_id = int(member_id), int(book_id)
        book_valid = self.parent.database.get_book_exist(book_id)
        member_valid = self.parent.checkout.is_member_valid(member_id)

        if not member_valid:
            self.statusvar.set("Member ID is invalid.")
            self.sbar.update()
        elif not book_valid:
            self.statusvar.set("Member ID is invalid.")
            self.sbar.update()
        else:
            result, text = self.parent.checkout.withdraw(book_id, member_id)
            if result:
                self.statusvar.set(text)
                self.sbar.update()
            else:
                # would you like to reserve a book?
                self.statusvar.set(
                    text
                    + " Would you like to reserve a book? Type Yes or No into the textbox above the status bar."
                )
                self.sbar.update()
                reservesv = StringVar()
                reservesv.trace("w", lambda name, index, mode, reservesv=reservesv: self.reserve(book_id, member_id))
                self.reserve_entry = Entry(
                    self.canvas,
                    bd=0,
                    bg="#e3e3e3",
                    highlightthickness=0,
                    font=("Open Sans", 15, "bold"),
                    foreground="#16262e",
                    textvariable=reservesv
                    
                )
                self.entry = self.reserve_entry.place(x=0.0, y=440.0, width=100, height=37)


    def reserve(self, book_id, member_id):
        text = self.reserve_entry.get()
        if text.lower() == 'yes':
            self.reserve_entry.place_forget()
            today = datetime.today().strftime("%Y-%m-%d")
            result, text = self.parent.checkout.reserve_book(book_id, member_id, today)
            self.statusvar.set(text)
            self.sbar.update()
            
        elif text.lower() == 'no':
            self.reserve_entry.place_forget()
            self.statusvar.set('Ready')
            self.sbar.update()

root = tk.Tk()
root.withdraw()

MainWindow()
root.mainloop()
