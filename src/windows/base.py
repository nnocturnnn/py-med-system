import tkinter as tk

from misc import create_button, create_combobox, create_entry

EMPTY_STRING = ""


class BaseWindow:
    def __init__(self, title):
        self.window = tk.Tk()
        self.window.wm_title(title)

        variable_names = [
            "id",
            "fName",
            "lName",
            "address",
            "phone",
            "email",
            "history",
        ]
        self.patient = {name: tk.StringVar() for name in variable_names}
        self.patient_details = {
            "doctor": tk.StringVar(),
        }

        self.setup_fields()
        self.setup_comboboxes()
        create_button(self.window, "Dicom", self.file_dialog, row=13, column=1)

    def setup_fields(self):
        labels = [
            ("Patient ID", 1),
            ("First Name", 2),
            ("Last Name", 3),
            ("D.O.B", 4),
            ("M.O.B", 5),
            ("Y.O.B", 6),
            ("Gender", 7),
            ("Home Address", 8),
            ("Phone Number", 9),
            ("Email ID", 10),
            ("Blood Group", 11),
            ("Patient History", 12),
        ]

        for text, row in labels:
            tk.Label(self.window, text=text, width=25).grid(pady=5, column=1, row=row)

        self.entries = [
            (self.patient["id"], 1),
            (self.patient["fName"], 2),
            (self.patient["lName"], 3),
            (self.patient["address"], 8),
            (self.patient["phone"], 9),
            (self.patient["email"], 10),
            (self.patient["history"], 12),
            (self.patient_details["doctor"], 13),
        ]

        for var, row in self.entries:
            create_entry(self.window, var, row=row)

    def setup_comboboxes(self):
        self.patient_details["genderList"] = ["Male", "Female", "Transgender", "Other"]
        self.patient_details["dateList"] = list(range(1, 32))
        self.patient_details["monthList"] = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        self.patient_details["yearList"] = list(range(1920, 2022))
        self.patient_details["bloodGroupList"] = [
            "A+",
            "A-",
            "B+",
            "B-",
            "O+",
            "O-",
            "AB+",
            "AB-",
        ]

        self.comboboxes = [
            (self.dateList, 4),
            (self.monthList, 5),
            (self.yearList, 6),
            (self.genderList, 7),
            (self.bloodGroupList, 11),
        ]

        for values, row in self.comboboxes:
            create_combobox(self.window, values, row=row)

    def file_dialog(self):
        file_path = tk.filedialog.askopenfilename(filetypes=(("All files", "*.*"),))
        self.patient_details["doctor"].set(file_path)

    def show(self):
        self.window.mainloop()

    def reset_fields(self):
        for var in self.patient.values():
            var.set("")
        for var in self.patient_details.values():
            var.set("")
        for combobox, _ in self.comboboxes:
            combobox.set("")
