import tkinter as tk

from db import Database
from misc import create_button
from windows.base import BaseWindow


class DeleteWindow(BaseWindow):
    def __init__(self, login):
        self.login = login
        super().__init__("Delete data")
        self.setup_delete_window()
        self.show()

    def setup_delete_window(self):
        heading = "Please enter Patient ID to delete"
        tk.Label(self.window, text=heading, width=50).grid(pady=20, row=1)
        tk.Label(self.window, text="Patient ID", width=10).grid(pady=5, row=2)

        self.idEntry = tk.Entry(self.window, width=5, textvariable=self.patient["id"])
        self.idEntry.grid(pady=5, row=3)

        create_button(self.window, "Delete", self.delete, row=14, column=1)

    def delete(self):
        database = Database()
        database.delete_patient(self.idEntry.get(), self.login)
        tk.messagebox.showinfo(
            "Deleted data", "Successfully deleted the data from the database"
        )
