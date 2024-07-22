import tkinter as tk
from tkinter import ttk

import numpy as np
import png
import pydicom


def create_button(parent, text, command, row, column=1, width=20, pady=15, padx=5):
    button = tk.Button(parent, text=text, width=width, command=command)
    button.grid(row=row, column=column, pady=pady, padx=padx)
    return button


def setup_treeview_columns(treeview, columns):
    for col, width in columns.items():
        treeview.column(col, width=width)
        treeview.heading(col, text=col.capitalize())


def create_entry(parent, textvariable, row, column=3, width=25, pady=5):
    entry = tk.Entry(parent, textvariable=textvariable, width=width)
    entry.grid(row=row, column=column, pady=pady)
    return entry


def create_combobox(parent, values, row, column=3, width=20, pady=5):
    combobox = ttk.Combobox(parent, values=values, width=width)
    combobox.grid(row=row, column=column, pady=pady)
    return combobox


def convert_to_png(file):
    try:
        ds = pydicom.dcmread(file)
        shape = ds.pixel_array.shape

        image_2d = ds.pixel_array.astype(float)
        image_2d_scaled = (np.maximum(image_2d, 0) / image_2d.max()) * 255.0
        image_2d_scaled = np.uint8(image_2d_scaled)

        png_file_path = f'{file.rstrip(".dcm")}.png'
        with open(png_file_path, "wb") as png_file:
            w = png.Writer(shape[1], shape[0], greyscale=True)
            w.write(png_file, image_2d_scaled)
    except Exception as e:
        print(f"Error converting DICOM to PNG: {e}")
        return None
    return png_file_path


def validate_values(id, fName, lName, phone, email, history):
    if not id.isdigit() or len(id) != 3:
        return "Invalid ID: ID should be a 3-digit number."
    if not fName.isalpha():
        return "Invalid First Name: First Name should contain only letters."
    if not lName.isalpha():
        return "Invalid Last Name: Last Name should contain only letters."
    if not phone.isdigit() or len(phone) != 10:
        return "Invalid Phone Number: Phone Number should be a 10-digit number."
    if "@" not in email or "." not in email.split("@")[-1]:
        return "Invalid Email: Email should contain '@' and a domain."
    if not history.isalpha():
        return "Invalid History: History should contain only letters."
    return "SUCCESS"
