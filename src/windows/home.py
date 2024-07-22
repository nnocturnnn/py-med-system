import tkinter as tk

from db import Database
from misc import create_button
from windows.delete import DeleteWindow
from windows.display import DatabaseView
from windows.insert import InsertWindow
from windows.search import SearchWindow
from windows.update import UpdateWindow


class HomePage:
    def __init__(self, login):
        self.login = login
        self.home_page_window = tk.Tk()
        self.home_page_window.wm_title("Patient Information System")

        tk.Label(self.home_page_window, text="Home Page", width=100).grid(
            pady=20, column=1, row=1
        )

        create_button(self.home_page_window, "Insert", self.insert, row=2)
        create_button(self.home_page_window, "Update", self.update, row=3)
        create_button(self.home_page_window, "Search", self.search, row=4)
        create_button(self.home_page_window, "Delete", self.delete, row=5)
        create_button(self.home_page_window, "Display", self.display, row=6)
        create_button(
            self.home_page_window, "Exit", self.home_page_window.destroy, row=7
        )

        self.home_page_window.mainloop()

    def insert(self):
        InsertWindow(self.login)

    def update(self):
        self.update_id_window = tk.Tk()
        self.update_id_window.wm_title("Update data")

        self.id = tk.StringVar()

        tk.Label(self.update_id_window, text="Enter the ID to update", width=50).grid(
            pady=20, row=1
        )

        self.idEntry = tk.Entry(self.update_id_window, width=5, textvariable=self.id)
        self.idEntry.grid(pady=10, row=2)

        create_button(self.update_id_window, "Update", self.update_id, row=3)

        self.update_id_window.mainloop()

    def update_id(self):
        UpdateWindow(self.idEntry.get(), self.login)
        self.update_id_window.destroy()

    def search(self):
        SearchWindow(self.login)

    def delete(self):
        DeleteWindow(self.login)

    def display(self):
        database = Database()
        data = database.display_patients(self.login)
        DatabaseView(data)
