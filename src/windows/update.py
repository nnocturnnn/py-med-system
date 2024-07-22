import tkinter as tk

from db import Database, Patient, PatientDetails
from misc import create_button, validate_values
from windows.base import BaseWindow


class UpdateWindow(BaseWindow):
    def __init__(self, id, login):
        self.id = id
        self.login = login
        super().__init__("Update data")
        self.load_data()
        self.setup_buttons()
        self.show()

    def setup_buttons(self):
        create_button(self.window, "Update", self.update, row=14, column=1)
        create_button(self.window, "Reset", self.reset_fields, row=14, column=2)
        create_button(self.window, "Close", self.window.destroy, row=14, column=3)

    def load_data(self):
        database = Database()
        search_results = database.search_patient(self.id, self.login)
        for idx, value in enumerate(search_results[0][1:], start=2):
            tk.Label(self.window, text=value, width=25).grid(pady=5, column=2, row=idx)

    def update(self):
        patient_values = [var.get() for var in self.patient.values()]
        detail_values = [var.get() for var in self.patient_details.values()]
        validation_result = validate_values(*patient_values)

        if validation_result == "SUCCESS":
            patient = Patient(*patient_values)
            patient_details = PatientDetails(
                self.patient["id"], *patient_details, self.login
            )
            database = Database()
            database.update_patient(patient, patient_details)
            tk.messagebox.showinfo(
                "Updated data", "Successfully updated the above data in the database"
            )
        else:
            tk.messagebox.showerror("Value Error", validation_result)
