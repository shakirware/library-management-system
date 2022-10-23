from database import Database
from book_search import Search
from book_checkout import Checkout
from book_return import Return
from book_select import Select
import tkinter as tk


class MainFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is the start page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Select",
                  command=lambda: master.switch_frame(SelectFrame)).pack()
        tk.Button(self, text="Search",
                  command=lambda: master.switch_frame(SearchFrame)).pack()

class SearchFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is the search page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(MainFrame)).pack()

class SelectFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="This is the select page").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to start page",
                  command=lambda: master.switch_frame(MainFrame)).pack()


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(MainFrame)
        
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        
        
app = Application()
app.mainloop()