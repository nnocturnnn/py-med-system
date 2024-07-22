import tkinter as tk

from PIL import Image, ImageTk

from misc import convert_to_png


class DicomWindow:
    def __init__(self, dicom_path, history):
        if dicom_path.endswith(".dcm"):
            convert_to_png(dicom_path)
            dicom_path = f'{dicom_path.strip(".dcm")}.png'

        self.window = tk.Tk()
        self.window.wm_title("Dicom")
        self.window.geometry("1050x600")

        canvas = tk.Canvas(self.window, width=600, height=600)
        canvas.pack()
        img = ImageTk.PhotoImage(Image.open(dicom_path), master=canvas)
        canvas.create_image(0, 0, anchor="nw", image=img)
        canvas.place(x=1, y=1)

        tk.Label(self.window, text=history, width=100).place(
            width=100, height=100, x=750, y=250
        )
        tk.Button(self.window, width=20, text="Update", command=self.accept).place(
            y=500, x=620
        )
        tk.Button(self.window, width=20, text="Ok", command=self.delete).place(
            y=500, x=820
        )
        self.window.mainloop()

    def accept(self):
        from windows.update import UpdateWindow

        UpdateWindow(self.m)

    def delete(self):
        self.window.destroy()
