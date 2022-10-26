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
    Entry
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
        self.current_window_label = StringVar()

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

        self.canvas.entry_image_1 = PhotoImage(file="./assets/entry.png")
        self.entry_bg_1 = self.canvas.create_image(115.0, 81.0, image=self.canvas.entry_image_1)
        self.entry_1 = Entry(
            self,
            bd=0,
            bg="#EFEFEF",
            highlightthickness=0,
            font=("Montserrat Bold", 150),
        )
        self.entry_1.place(x=55.0, y=30.0 + 2, width=120.0, height=0)

        self.canvas.create_text(
            56.0,
            45.0,
            anchor="nw",
            text="Vacant",
            fill="#5E95FF",
            font=("Montserrat Bold", 14 * -1),
        )





class SearchFrame(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.canvas = Canvas(
            self,
            bg="#DBC2CF",
            height=506,
            width=797,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)

class ReturnFrame(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.canvas = Canvas(
            self,
            bg="#9FA2B2",
            height=506,
            width=797,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)

class SelectFrame(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.canvas = Canvas(
            self,
            bg="#9FA2B2",
            height=506,
            width=797,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)

class CheckoutFrame(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.canvas = Canvas(
            self,
            bg="#9FA2B2",
            height=506,
            width=797,
            bd=0,
            highlightthickness=0,
            relief="ridge",
        )

        self.canvas.place(x=0, y=0)

root = tk.Tk()
root.withdraw()  

MainWindow()
root.mainloop()