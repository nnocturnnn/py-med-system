import tkinter as tk

from db import Database
from misc import create_button
from windows.base import BaseWindow
from windows.display import DatabaseView


class SearchWindow(BaseWindow):
    def __init__(self, login):
        self.login = login
        super().__init__("Search data")
        self.setup_search_window()
        self.show()

    def setup_search_window(self):
        heading = "Please enter Patient ID to search"
        tk.Label(self.window, text=heading, width=50).grid(pady=20, row=1)
        tk.Label(self.window, text="Patient ID", width=10).grid(pady=5, row=2)

        self.idEntry = tk.Entry(self.window, width=5, textvariable=self.patient["id"])
        self.idEntry.grid(pady=5, row=3)

        create_button(self.window, "Search", self.search, row=14, column=1)

    def search(self):
        database = Database()
        data = database.search_patient(self.idEntry.get(), self.login)
        DatabaseView(data)
