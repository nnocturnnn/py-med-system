import tkinter as tk
from tkinter import ttk

from misc import setup_treeview_columns
from windows.dicom import DicomWindow


class DatabaseView:
    def __init__(self, data):
        self.database_view_window = tk.Tk()
        self.database_view_window.geometry("1400x600")
        self.database_view_window.wm_title("Database View")

        tk.Label(self.database_view_window, text="Database View Window", width=25).grid(
            pady=5, column=1, row=1
        )

        self.database_view = ttk.Treeview(self.database_view_window)
        self.database_view.grid(pady=5, column=1, row=2)
        self.database_view["show"] = "headings"
        self.database_view["columns"] = (
            "id",
            "fName",
            "lName",
            "dob",
            "mob",
            "yob",
            "gender",
            "address",
            "phone",
            "email",
            "bloodGroup",
            "history",
            "doctor",
            "dicom",
        )

        column_widths = {
            "id": 40,
            "fName": 100,
            "lName": 100,
            "dob": 60,
            "mob": 60,
            "yob": 60,
            "gender": 60,
            "address": 200,
            "phone": 100,
            "email": 200,
            "bloodGroup": 100,
            "history": 100,
            "doctor": 100,
            "dicom": 100,
        }

        setup_treeview_columns(self.database_view, column_widths)

        for idx, record in enumerate(data):
            tk.Button(
                self.database_view_window,
                text=str(idx),
                command=lambda i=idx: self.open_dicom_window(data[i]),
            ).place(x=1300, y=60 + 20 * idx)
            record_list = list(record)
            record_list[13] = ""  # Clear DICOM path for display
            self.database_view.insert("", "end", values=record_list)

        self.database_view_window.mainloop()

    def open_dicom_window(self, record):
        dicom_path = record[13]
        history = record[11]
        DicomWindow(dicom_path, history)
