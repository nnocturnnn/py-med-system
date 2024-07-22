import tkinter as tk

from db import Database, Patient, PatientDetails
from misc import create_button, validate_values
from windows.base import BaseWindow


class InsertWindow(BaseWindow):
    def __init__(self, login):
        self.login = login
        super().__init__("Insert data")
        self.setup_buttons()
        self.show()

    def setup_buttons(self):
        create_button(self.window, "Insert", self.insert, row=14, column=1)
        create_button(self.window, "Reset", self.reset_fields, row=14, column=2)
        create_button(self.window, "Close", self.window.destroy, row=14, column=3)

    def insert(self):
        patient_values = [var.get() for var in self.patient.values()]
        detail_values = [var.get() for var in self.patient_details.values()]
        validation_result = validate_values(*patient_values)

        if validation_result == "SUCCESS":
            patient = Patient(*patient_values)
            patient_details = PatientDetails(
                self.patient["id"], *detail_values, self.login
            )
            database = Database()
            database.insert_patient(patient, patient_details)
            tk.messagebox.showinfo(
                "Inserted data", "Successfully inserted the above data in the database"
            )
        else:
            tk.messagebox.showerror("Value Error", validation_result)
