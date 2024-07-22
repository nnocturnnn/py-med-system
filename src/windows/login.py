import tkinter as tk

from db import Database
from misc import create_button
from windows.home import HomePage
from windows.registration import RegWindow


class LoginPage:
    def __init__(self):
        self.login_page_window = tk.Tk()
        self.login_page_window.wm_title("Patient Information System")

        tk.Label(self.login_page_window, text="Login Page", width=100).grid(
            pady=20, column=1, row=1
        )
        tk.Button(
            self.login_page_window, width=20, text="Login", command=self.login
        ).grid(pady=15, column=1, row=2)
        tk.Button(
            self.login_page_window,
            width=20,
            text="Registration",
            command=self.registration,
        ).grid(pady=15, column=1, row=3)

        self.login_page_window.mainloop()

    def login(self):
        LoginWindow()

    def registration(self):
        RegWindow()


class LoginWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.wm_title("Sign In")

        self.id = tk.StringVar()
        self.fName = tk.StringVar()

        tk.Label(self.window, text="Login", width=25).grid(pady=5, column=1, row=1)
        tk.Label(self.window, text="Password", width=25).grid(pady=5, column=1, row=2)
        self.idEntry = tk.Entry(self.window, width=25, textvariable=self.id)
        self.fNameEntry = tk.Entry(
            self.window, show="*", width=25, textvariable=self.fName
        )
        self.idEntry.grid(pady=5, column=3, row=1)
        self.fNameEntry.grid(pady=5, column=3, row=2)

        tk.Button(self.window, width=20, text="Login", command=self.login).grid(
            pady=15, column=1, row=3
        )

    def login(self):
        database = Database()
        if database.login(self.idEntry.get(), self.fNameEntry.get()):
            login = self.idEntry.get()
            self.window.destroy()
            HomePage(login)
        else:
            tk.messagebox.showerror("Login Error", "Invalid login credentials")
            self.window.destroy()
