import tkinter as tk

from db import Database


class RegWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.wm_title("Sign Up")

        self.id = tk.StringVar()
        self.fName = tk.StringVar()
        self.ty = tk.StringVar()
        self.fi = tk.StringVar()

        tk.Label(self.window, text="Login", width=25).grid(pady=5, column=1, row=1)
        tk.Label(self.window, text="Password", width=25).grid(pady=5, column=1, row=2)
        tk.Label(self.window, text="FIO", width=25).grid(pady=5, column=1, row=3)
        tk.Label(self.window, text="Type", width=25).grid(pady=5, column=1, row=4)

        self.idEntry = tk.Entry(self.window, width=25, textvariable=self.id)
        self.fNameEntry = tk.Entry(
            self.window, show="*", width=25, textvariable=self.fName
        )
        self.FIO = tk.Entry(self.window, width=25, textvariable=self.ty)
        self.Type = tk.Entry(self.window, width=25, textvariable=self.fi)

        self.idEntry.grid(pady=5, column=3, row=1)
        self.fNameEntry.grid(pady=5, column=3, row=2)
        self.FIO.grid(pady=5, column=3, row=3)
        self.Type.grid(pady=5, column=3, row=4)

        tk.Button(
            self.window, width=20, text="Registration", command=self.registration
        ).grid(pady=15, column=1, row=5)

    def registration(self):
        database = Database()
        database.registration(self.idEntry.get(), self.fNameEntry.get())
        tk.messagebox.showinfo("Registration", "Successfully registered")
        self.window.destroy()
