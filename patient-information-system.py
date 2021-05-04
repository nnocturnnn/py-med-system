# Mini Project
import tkinter
import tkinter.filedialog
import tkinter.ttk
from PIL import ImageTk,Image
import tkinter.messagebox
import sqlite3
import pydicom
import png
import numpy as np
import os

LOGIN = "None"


class Database:
    def __init__(self):
        self.dbConnection = sqlite3.connect("dbFile.db")
        self.dbCursor = self.dbConnection.cursor()
        self.dbCursor.execute("CREATE TABLE IF NOT EXISTS patient_info (id PRIMARYKEY text, fName text, lName text, dob text, mob text, yob text, gender text, address text, phone text, email text, bloodGroup text, history text, doctor text, filec text)")
        self.dbCursor.execute("CREATE TABLE IF NOT EXISTS users (login text, password text)")

    def __del__(self):
        self.dbCursor.close()
        self.dbConnection.close()

    def Insert(self, id, fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, filec):
        global LOGIN
        self.dbCursor.execute("INSERT INTO patient_info VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id, fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, LOGIN, filec))
        self.dbConnection.commit()
        
    def Update(self, fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history,filec, id):
        global LOGIN
        self.dbCursor.execute("UPDATE patient_info SET fName = ?, lName = ?, dob = ?, mob = ?, yob = ?, gender = ?, address = ?, phone = ?, email = ?, bloodGroup = ?, history = ?, doctor = ?, filec = ? WHERE id = ?", (fName, lName, dob, mob, yob, gender, address, phone, email, bloodGroup, history, LOGIN, filec, id))
        self.dbConnection.commit()
        
    def Search(self, id):
        global LOGIN
        self.dbCursor.execute("SELECT * FROM patient_info WHERE id = ? AND doctor = ?", (id, LOGIN,))
        searchResults = self.dbCursor.fetchall()
        return searchResults
        
    def Delete(self, id):
        global LOGIN
        self.dbCursor.execute("DELETE FROM patient_info WHERE id = ? AND doctor = ?", (id, LOGIN, ))
        self.dbConnection.commit()

    def Display(self):
        global LOGIN
        self.dbCursor.execute("SELECT * FROM patient_info WHERE doctor = ?", (LOGIN,))
        records = self.dbCursor.fetchall()
        return records

    def Login(self,login,password):
        self.dbCursor.execute("SELECT password FROM users WHERE login = ?", (login, ))
        records = self.dbCursor.fetchone()
        if records == None:
            return False
        return records[0] == password

    def Registration(self,login,password):
        self.dbCursor.execute("INSERT INTO users VALUES (?, ?)",(login,password))
        self.dbConnection.commit()




class Values:
    def Validate(self, id, fName, lName, phone, email, history, doctor):
        if not (id.isdigit() and (len(id) == 3)):
            return "id"
        elif not (fName.isalpha()):
            return "fName"
        elif not (lName.isalpha()):
            return "lName"
        elif not (phone.isdigit() and (len(phone) == 10)):
            return "phone"
        elif not (email.count("@") == 1 and email.count(".") > 0):
            return "email"
        elif not (history.isalpha()):
            return "history"
        else:
            return "SUCCESS"
        




class InsertWindow:
    def __init__(self):
        global LOGIN
        self.window = tkinter.Tk()
        self.window.wm_title("Insert data")

        # Initializing all the variables
        self.id = tkinter.StringVar()
        self.fName = tkinter.StringVar()
        self.lName = tkinter.StringVar()
        self.address = tkinter.StringVar()
        self.phone = tkinter.StringVar()
        self.email = tkinter.StringVar()
        self.history = tkinter.StringVar()
        self.doctor = tkinter.StringVar()

        self.genderList = ["Male", "Female", "Transgender", "Other"]
        self.dateList = list(range(1, 32))
        self.monthList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.yearList = list(range(1920, 2022))
        self.bloodGroupList = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

        # Labels
        tkinter.Label(self.window, text = "Patient ID",  width = 25).grid(pady = 5, column = 1, row = 1)
        tkinter.Label(self.window, text = "First Name",  width = 25).grid(pady = 5, column = 1, row = 2)
        tkinter.Label(self.window, text = "Last Name",  width = 25).grid(pady = 5, column = 1, row = 3)
        tkinter.Label(self.window, text = "D.O.B",  width = 25).grid(pady = 5, column = 1, row = 4)
        tkinter.Label(self.window, text = "M.O.B",  width = 25).grid(pady = 5, column = 1, row = 5)
        tkinter.Label(self.window, text = "Y.O.B",  width = 25).grid(pady = 5, column = 1, row = 6)
        tkinter.Label(self.window, text = "Gender",  width = 25).grid(pady = 5, column = 1, row = 7)
        tkinter.Label(self.window, text = "Home Address",  width = 25).grid(pady = 5, column = 1, row = 8)
        tkinter.Label(self.window, text = "Phone Number",  width = 25).grid(pady = 5, column = 1, row = 9)
        tkinter.Label(self.window, text = "Email ID",  width = 25).grid(pady = 5, column = 1, row = 10)
        tkinter.Label(self.window, text = "Blood Group",  width = 25).grid(pady = 5, column = 1, row = 11)
        tkinter.Label(self.window, text = "Patient History",  width = 25).grid(pady = 5, column = 1, row = 12)

        # Fields
        # Entry widgets
        self.idEntry = tkinter.Entry(self.window,  width = 25, textvariable = self.id)
        self.fNameEntry = tkinter.Entry(self.window,  width = 25, textvariable = self.fName)
        self.lNameEntry = tkinter.Entry(self.window,  width = 25, textvariable = self.lName)
        self.addressEntry = tkinter.Entry(self.window,  width = 25, textvariable = self.address)
        self.phoneEntry = tkinter.Entry(self.window,  width = 25, textvariable = self.phone)
        self.emailEntry = tkinter.Entry(self.window,  width = 25, textvariable = self.email)
        self.historyEntry = tkinter.Entry(self.window,  width = 25, textvariable = self.history)
        self.doctorEntry = tkinter.Entry(self.window,  width = 25, textvariable = self.doctor)

        self.idEntry.grid(pady = 5, column = 3, row = 1)
        self.fNameEntry.grid(pady = 5, column = 3, row = 2)
        self.lNameEntry.grid(pady = 5, column = 3, row = 3)
        self.addressEntry.grid(pady = 5, column = 3, row = 8)
        self.phoneEntry.grid(pady = 5, column = 3, row = 9)
        self.emailEntry.grid(pady = 5, column = 3, row = 10)
        self.historyEntry.grid(pady = 5, column = 3, row = 12)
        self.doctorEntry.grid(pady = 5, column = 3, row = 13)

        # Combobox widgets
        self.dobBox = tkinter.ttk.Combobox(self.window, values = self.dateList, width = 20)
        self.mobBox = tkinter.ttk.Combobox(self.window, values = self.monthList, width = 20)
        self.yobBox = tkinter.ttk.Combobox(self.window, values = self.yearList, width = 20)
        self.genderBox = tkinter.ttk.Combobox(self.window, values = self.genderList, width = 20)
        self.bloodGroupBox = tkinter.ttk.Combobox(self.window, values = self.bloodGroupList, width = 20)

        self.dobBox.grid(pady = 5, column = 3, row = 4)
        self.mobBox.grid(pady = 5, column = 3, row = 5)
        self.yobBox.grid(pady = 5, column = 3, row = 6)
        self.genderBox.grid(pady = 5, column = 3, row = 7)
        self.bloodGroupBox.grid(pady = 5, column = 3, row = 11)

        # Button widgets
        tkinter.Button(self.window, width = 20, text = "Dicom", command = self.File).grid(pady = 15, column = 1, row = 13)
        tkinter.Button(self.window, width = 20, text = "Insert", command = self.Insert).grid(pady = 15, padx = 5, column = 1, row = 14)
        tkinter.Button(self.window, width = 20, text = "Reset", command = self.Reset).grid(pady = 15, padx = 5, column = 2, row = 14)
        tkinter.Button(self.window, width = 20, text = "Close", command = self.window.destroy).grid(pady = 15, padx = 5, column = 3, row = 14)

        self.window.mainloop()
    
    def File(self):
        file_path = tkinter.filedialog.askopenfilename(filetypes=(("All files", "*.*"),
                                       ("All files", "*.*") ))
        self.doctorEntry.delete(0, tkinter.END)
        self.doctorEntry.insert(0, file_path)

    def Insert(self):
        self.values = Values()
        self.database = Database()
        self.test = self.values.Validate(self.idEntry.get(), self.fNameEntry.get(), self.lNameEntry.get(), self.phoneEntry.get(), self.emailEntry.get(), self.historyEntry.get(), self.doctorEntry.get())
        if (self.test == "SUCCESS"):
            self.database.Insert(self.idEntry.get(), self.fNameEntry.get(), self.lNameEntry.get(), self.dobBox.get(), self.mobBox.get(), self.yobBox.get(), self.genderBox.get(), self.addressEntry.get(), self.phoneEntry.get(), self.emailEntry.get(), self.bloodGroupBox.get(), self.historyEntry.get(), self.doctorEntry.get())
            tkinter.messagebox.showinfo("Inserted data", "Successfully inserted the above data in the database")
        else:
            self.valueErrorMessage = "Invalid input in field " + self.test 
            tkinter.messagebox.showerror("Value Error", self.valueErrorMessage)

    def Reset(self):
        self.idEntry.delete(0, tkinter.END)
        self.fNameEntry.delete(0, tkinter.END)
        self.lNameEntry.delete(0, tkinter.END)
        self.dobBox.set("")
        self.mobBox.set("")
        self.yobBox.set("")
        self.genderBox.set("")
        self.addressEntry.delete(0, tkinter.END)
        self.phoneEntry.delete(0, tkinter.END)
        self.emailEntry.delete(0, tkinter.END)
        self.bloodGroupBox.set("")
        self.historyEntry.delete(0, tkinter.END)
        self.doctorEntry.delete(0, tkinter.END)





class UpdateWindow:
    def __init__(self, id):
        self.window = tkinter.Tk()
        self.window.wm_title("Update data")

        # Initializing all the variables
        self.id = id

        self.fName = tkinter.StringVar()
        self.lName = tkinter.StringVar()
        self.address = tkinter.StringVar()
        self.phone = tkinter.StringVar()
        self.email = tkinter.StringVar()
        self.history = tkinter.StringVar()
        self.doctor = tkinter.StringVar()

        self.genderList = ["Male", "Female", "Transgender", "Other"]
        self.dateList = list(range(1, 32))
        self.monthList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.yearList = list(range(1900, 2020))
        self.bloodGroupList = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]

        # Labels
        tkinter.Label(self.window, text = "Patient ID",  width = 25).grid(pady = 5, column = 1, row = 1)
        tkinter.Label(self.window, text = id,  width = 25).grid(pady = 5, column = 3, row = 1)
        tkinter.Label(self.window, text = "First Name",  width = 25).grid(pady = 5, column = 1, row = 2)
        tkinter.Label(self.window, text = "Last Name",  width = 25).grid(pady = 5, column = 1, row = 3)
        tkinter.Label(self.window, text = "D.O.B",  width = 25).grid(pady = 5, column = 1, row = 4)
        tkinter.Label(self.window, text = "M.O.B",  width = 25).grid(pady = 5, column = 1, row = 5)
        tkinter.Label(self.window, text = "Y.O.B",  width = 25).grid(pady = 5, column = 1, row = 6)
        tkinter.Label(self.window, text = "Gender",  width = 25).grid(pady = 5, column = 1, row = 7)
        tkinter.Label(self.window, text = "Home Address",  width = 25).grid(pady = 5, column = 1, row = 8)
        tkinter.Label(self.window, text = "Phone Number",  width = 25).grid(pady = 5, column = 1, row = 9)
        tkinter.Label(self.window, text = "Email ID",  width = 25).grid(pady = 5, column = 1, row = 10)
        tkinter.Label(self.window, text = "Blood Group",  width = 25).grid(pady = 5, column = 1, row = 11)
        tkinter.Label(self.window, text = "Patient History",  width = 25).grid(pady = 5, column = 1, row = 12)
        tkinter.Button(self.window, width = 20, text = "Dicom", command = self.File).grid(pady = 15, column = 1, row = 13)

        # Set previous values
        self.database = Database()
        self.searchResults = self.database.Search(id)
        
        tkinter.Label(self.window, text = self.searchResults[0][1],  width = 25).grid(pady = 5, column = 2, row = 2)
        tkinter.Label(self.window, text = self.searchResults[0][2],  width = 25).grid(pady = 5, column = 2, row = 3)
        tkinter.Label(self.window, text = self.searchResults[0][3],  width = 25).grid(pady = 5, column = 2, row = 4)
        tkinter.Label(self.window, text = self.searchResults[0][4],  width = 25).grid(pady = 5, column = 2, row = 5)
        tkinter.Label(self.window, text = self.searchResults[0][5],  width = 25).grid(pady = 5, column = 2, row = 6)
        tkinter.Label(self.window, text = self.searchResults[0][6],  width = 25).grid(pady = 5, column = 2, row = 7)
        tkinter.Label(self.window, text = self.searchResults[0][7],  width = 25).grid(pady = 5, column = 2, row = 8)
        tkinter.Label(self.window, text = self.searchResults[0][8],  width = 25).grid(pady = 5, column = 2, row = 9)
        tkinter.Label(self.window, text = self.searchResults[0][9],  width = 25).grid(pady = 5, column = 2, row = 10)
        tkinter.Label(self.window, text = self.searchResults[0][10],  width = 25).grid(pady = 5, column = 2, row = 11)
        tkinter.Label(self.window, text = self.searchResults[0][11],  width = 25).grid(pady = 5, column = 2, row = 12)
        tkinter.Label(self.window, text = self.searchResults[0][12],  width = 25).grid(pady = 5, column = 2, row = 13)

        # Fields
        # Entry widgets
        self.fNameEntry = tkinter.Entry(self.window,  width = 25, textvariable = self.fName)
        self.lNameEntry = tkinter.Entry(self.window,  width = 25, textvariable = self.lName)
        self.addressEntry = tkinter.Entry(self.window,  width = 25, textvariable = self.address)
        self.phoneEntry = tkinter.Entry(self.window,  width = 25, textvariable = self.phone)
        self.emailEntry = tkinter.Entry(self.window,  width = 25, textvariable = self.email)
        self.historyEntry = tkinter.Entry(self.window,  width = 25, textvariable = self.history)
        self.doctorEntry = tkinter.Entry(self.window,  width = 25, textvariable = self.doctor)

        self.fNameEntry.grid(pady = 5, column = 3, row = 2)
        self.lNameEntry.grid(pady = 5, column = 3, row = 3)
        self.addressEntry.grid(pady = 5, column = 3, row = 8)
        self.phoneEntry.grid(pady = 5, column = 3, row = 9)
        self.emailEntry.grid(pady = 5, column = 3, row = 10)
        self.historyEntry.grid(pady = 5, column = 3, row = 12)
        self.doctorEntry.grid(pady = 5, column = 3, row = 13)

        # Combobox widgets
        self.dobBox = tkinter.ttk.Combobox(self.window, values = self.dateList, width = 20)
        self.mobBox = tkinter.ttk.Combobox(self.window, values = self.monthList, width = 20)
        self.yobBox = tkinter.ttk.Combobox(self.window, values = self.yearList, width = 20)
        self.genderBox = tkinter.ttk.Combobox(self.window, values = self.genderList, width = 20)
        self.bloodGroupBox = tkinter.ttk.Combobox(self.window, values = self.bloodGroupList, width = 20)

        self.dobBox.grid(pady = 5, column = 3, row = 4)
        self.mobBox.grid(pady = 5, column = 3, row = 5)
        self.yobBox.grid(pady = 5, column = 3, row = 6)
        self.genderBox.grid(pady = 5, column = 3, row = 7)
        self.bloodGroupBox.grid(pady = 5, column = 3, row = 11)

        # Button widgets
        tkinter.Button(self.window, width = 20, text = "Update", command = self.Update).grid(pady = 15, padx = 5, column = 1, row = 14)
        tkinter.Button(self.window, width = 20, text = "Reset", command = self.Reset).grid(pady = 15, padx = 5, column = 2, row = 14)
        tkinter.Button(self.window, width = 20, text = "Close", command = self.window.destroy).grid(pady = 15, padx = 5, column = 3, row = 14)

        self.window.mainloop()

    def File(self):
        file_path = tkinter.filedialog.askopenfilename(filetypes=(("All files", "*.*"),
                                       ("All files", "*.*") ))
        self.doctorEntry.delete(0, tkinter.END)
        self.doctorEntry.insert(0, file_path)

    def Update(self):
        self.database = Database()
        self.database.Update(self.fNameEntry.get(), self.lNameEntry.get(), self.dobBox.get(), self.mobBox.get(), self.yobBox.get(), self.genderBox.get(), self.addressEntry.get(), self.phoneEntry.get(), self.emailEntry.get(), self.bloodGroupBox.get(), self.historyEntry.get(), self.doctorEntry.get(), self.id)
        tkinter.messagebox.showinfo("Updated data", "Successfully updated the above data in the database")

    def Reset(self):
        self.fNameEntry.delete(0, tkinter.END)
        self.lNameEntry.delete(0, tkinter.END)
        self.dobBox.set("")
        self.mobBox.set("")
        self.yobBox.set("")
        self.genderBox.set("")
        self.addressEntry.delete(0, tkinter.END)
        self.phoneEntry.delete(0, tkinter.END)
        self.emailEntry.delete(0, tkinter.END)
        self.bloodGroupBox.set("")
        self.historyEntry.delete(0, tkinter.END)
        self.doctorEntry.delete(0, tkinter.END)

class DatabaseView:
    def __init__(self, data):
        self.databaseViewWindow = tkinter.Tk()
        self.databaseViewWindow.geometry("1400x600")
        self.databaseViewWindow.wm_title("Database View")

        # Label widgets
        tkinter.Label(self.databaseViewWindow, text = "Database View Window",  width = 25).grid(pady = 5, column = 1, row = 1)

        self.databaseView = tkinter.ttk.Treeview(self.databaseViewWindow)
        self.databaseView.grid(pady = 5, column = 1, row = 2)
        # for i in range(10):
        #     tkinter.Button(self.databaseViewWindow,text=str(i), command=lambda i=i: self.hi(i)).place(x=1300,y=60+20*i)
        self.databaseView["show"] = "headings"
        self.databaseView["columns"] = ("id", "fName", "lName", "dob", "mob", "yob", "gender", "address", "phone", "email", "bloodGroup", "history", "doctor","dicom")

        # Treeview column headings
        self.databaseView.heading("id", text = "ID")
        self.databaseView.heading("fName", text = "First Name")
        self.databaseView.heading("lName", text = "Last Name")
        self.databaseView.heading("dob", text = "D.O.B")
        self.databaseView.heading("mob", text = "M.O.B")
        self.databaseView.heading("yob", text = "Y.O.B")
        self.databaseView.heading("gender", text = "Gender")
        self.databaseView.heading("address", text = "Home Address")
        self.databaseView.heading("phone", text = "Phone Number")
        self.databaseView.heading("email", text = "Email ID")
        self.databaseView.heading("bloodGroup", text = "Blood Group")
        self.databaseView.heading("history", text = "History")
        self.databaseView.heading("doctor", text = "Doctor")
        self.databaseView.heading("dicom",text="dicom")

        # Treeview columns
        self.databaseView.column("id", width = 40)
        self.databaseView.column("fName", width = 100)
        self.databaseView.column("lName", width = 100)
        self.databaseView.column("dob", width = 60)
        self.databaseView.column("mob", width = 60)
        self.databaseView.column("yob", width = 60)
        self.databaseView.column("gender", width = 60)
        self.databaseView.column("address", width = 200)
        self.databaseView.column("phone", width = 100)
        self.databaseView.column("email", width = 200)
        self.databaseView.column("bloodGroup", width = 100)
        self.databaseView.column("history", width = 100)
        self.databaseView.column("doctor", width = 100)

        for record in enumerate(data):
            tkinter.Button(self.databaseViewWindow,text=str(record[0]), command=lambda i=record[0]: self.hi(i,data)).place(x=1300,y=60+20*record[0])
            l = list(record[1])
            l[13] = ""
            self.databaseView.insert('', 'end', values=(l))

        self.databaseViewWindow.mainloop()
    
    def hi(self,i,data):
        dW = DicomWindow(data[i])


def convert_to_png(file):
    ds = pydicom.dcmread(file)

    shape = ds.pixel_array.shape
    image_2d = ds.pixel_array.astype(float)
    image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0
    image_2d_scaled = np.uint8(image_2d_scaled)
    with open(f'{file.strip(".dcm")}.png', 'wb') as png_file:
        w = png.Writer(shape[1], shape[0], greyscale=True)
        w.write(png_file, image_2d_scaled)

class DicomWindow:
    def __init__(self, data):
        data = list(data)
        if data[13].endswith(".dcm"):
            convert_to_png(data[13])
            data[13] = f'{data[13].strip(".dcm")}.png'
        self.window = tkinter.Tk()
        self.window.wm_title("Dicom")
        self.window.geometry("1050x600")
        self.m = data[0]
        canvas = tkinter.Canvas(self.window, width = 600, height = 600)
        canvas.pack()
        img = ImageTk.PhotoImage(Image.open(data[13]),master = canvas)
        canvas.create_image(0, 0, anchor='nw', image=img)
        canvas.place(x=1,y=1)
        tkinter.Label(self.window, text = data[11],  width = 100).place(width=100, height=100, x=750,y=250)
        tkinter.Button(self.window, width = 20, text = "Update", command = self.Acept).place(y=500,x=620)
        tkinter.Button(self.window, width = 20, text = "Ok", command = self.Del).place(y=500,x=820)
        self.window.mainloop()
    
    def Acept(self):
        uW = UpdateWindow(self.m)

    def Del(self):
        self.window.destroy()



class SearchDeleteWindow:
    def __init__(self, task):
        window = tkinter.Tk()
        window.wm_title(task + " data")

        # Initializing all the variables
        self.id = tkinter.StringVar()
        self.fName = tkinter.StringVar()
        self.lName = tkinter.StringVar()
        self.heading = "Please enter Patient ID to " + task

        # Labels
        tkinter.Label(window, text = self.heading, width = 50).grid(pady = 20, row = 1)
        tkinter.Label(window, text = "Patient ID", width = 10).grid(pady = 5, row = 2)

        # Entry widgets
        self.idEntry = tkinter.Entry(window, width = 5, textvariable = self.id)

        self.idEntry.grid(pady = 5, row = 3)

        # Button widgets
        if (task == "Search"):
            tkinter.Button(window, width = 20, text = task, command = self.Search).grid(pady = 15, padx = 5, column = 1, row = 14)
        elif (task == "Delete"):
            tkinter.Button(window, width = 20, text = task, command = self.Delete).grid(pady = 15, padx = 5, column = 1, row = 14)

    def Search(self):
        self.database = Database()
        self.data = self.database.Search(self.idEntry.get())
        self.databaseView = DatabaseView(self.data)
    
    def Delete(self):
        self.database = Database()
        self.database.Delete(self.idEntry.get())




















class HomePage:
    def __init__(self):
        self.homePageWindow = tkinter.Tk()
        self.homePageWindow.wm_title("Patient Information System")

        tkinter.Label(self.homePageWindow, text = "Home Page",  width = 100).grid(pady = 20, column = 1, row = 1)

        tkinter.Button(self.homePageWindow, width = 20, text = "Insert", command = self.Insert).grid(pady = 15, column = 1, row = 2)
        tkinter.Button(self.homePageWindow, width = 20, text = "Update", command = self.Update).grid(pady = 15, column = 1, row = 3)
        tkinter.Button(self.homePageWindow, width = 20, text = "Search", command = self.Search).grid(pady = 15, column = 1, row = 4)
        tkinter.Button(self.homePageWindow, width = 20, text = "Delete", command = self.Delete).grid(pady = 15, column = 1, row = 5)
        tkinter.Button(self.homePageWindow, width = 20, text = "Display", command = self.Display).grid(pady = 15, column = 1, row = 6)
        tkinter.Button(self.homePageWindow, width = 20, text = "Exit", command = self.homePageWindow.destroy).grid(pady = 15, column = 1, row = 7)

        self.homePageWindow.mainloop()

    def Insert(self):
        self.insertWindow = InsertWindow()
    
    def Update(self):
        self.updateIDWindow = tkinter.Tk()
        self.updateIDWindow.wm_title("Update data")

        # Initializing all the variables
        self.id = tkinter.StringVar()

        # Label
        tkinter.Label(self.updateIDWindow, text = "Enter the ID to update", width = 50).grid(pady = 20, row = 1)

        # Entry widgets
        self.idEntry = tkinter.Entry(self.updateIDWindow, width = 5, textvariable = self.id)
        
        self.idEntry.grid(pady = 10, row = 2)
        
        # Button widgets
        tkinter.Button(self.updateIDWindow, width = 20, text = "Update", command = self.updateID).grid(pady = 10, row = 3)

        self.updateIDWindow.mainloop()

    def updateID(self):
        self.updateWindow = UpdateWindow(self.idEntry.get())
        self.updateIDWindow.destroy()

    def Search(self):
        self.searchWindow = SearchDeleteWindow("Search")

    def Delete(self):
        self.deleteWindow = SearchDeleteWindow("Delete")

    def Display(self):
        self.database = Database()
        self.data = self.database.Display()
        self.displayWindow = DatabaseView(self.data)


class loginWindow:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.wm_title("LoginWindow")

        self.id = tkinter.StringVar()
        self.fName = tkinter.StringVar()
        tkinter.Label(self.window, text = "Login",  width = 25).grid(pady = 5, column = 1, row = 1)
        tkinter.Label(self.window, text = "Password",  width = 25).grid(pady = 5, column = 1, row = 2)
        self.idEntry = tkinter.Entry(self.window,  width = 25, textvariable = self.id)
        self.fNameEntry = tkinter.Entry(self.window,show="*",  width = 25, textvariable = self.fName)
        self.idEntry.grid(pady = 5, column = 3, row = 1)
        self.fNameEntry.grid(pady = 5, column = 3, row = 2)
        tkinter.Button(self.window, width = 20, text = "Login", command = self.Login).grid(pady = 15, column = 1, row = 3)

    def Login(self):
        self.database = Database()
        if self.database.Login(self.idEntry.get(),self.fNameEntry.get()):
            global LOGIN
            LOGIN = self.idEntry.get()
            self.window.destroy()
            homePage = HomePage()
        else:
            self.window.destroy()




class regWindow:
    def __init__(self):
        self.window = tkinter.Tk()
        self.window.wm_title("RegistrationWindow")
        self.id = tkinter.StringVar()
        self.fName = tkinter.StringVar()
        self.ty = tkinter.StringVar()
        self.fi = tkinter.StringVar()
        tkinter.Label(self.window, text = "Login",  width = 25).grid(pady = 5, column = 1, row = 1)
        tkinter.Label(self.window, text = "Password",  width = 25).grid(pady = 5, column = 1, row = 2)
        tkinter.Label(self.window, text = "FIO",  width = 25).grid(pady = 5, column = 1, row = 3)
        tkinter.Label(self.window, text = "Type",  width = 25).grid(pady = 5, column = 1, row = 4)
        self.idEntry = tkinter.Entry(self.window,  width = 25, textvariable = self.id)
        self.fNameEntry = tkinter.Entry(self.window,show="*",  width = 25, textvariable = self.fName)
        self.FIO = tkinter.Entry(self.window,  width = 25, textvariable = self.ty)
        self.Type =  tkinter.Entry(self.window,  width = 25, textvariable = self.fi)
        self.idEntry.grid(pady = 5, column = 3, row = 1)
        self.fNameEntry.grid(pady = 5, column = 3, row = 2)
        self.FIO.grid(pady = 5, column = 3, row = 3)
        self.Type.grid(pady = 5, column = 3, row = 4)
        tkinter.Button(self.window, width = 20, text = "Registration", command = self.Registration).grid(pady = 15, column = 1, row = 5)
    
    def Registration(self):
        self.database = Database()
        self.database.Registration(self.idEntry.get(),self.fNameEntry.get())
        self.window.destroy()






class LoginPage:
    def __init__(self):
        self.homePageWindow = tkinter.Tk()
        self.homePageWindow.wm_title("Patient Information System")
        tkinter.Label(self.homePageWindow, text = "Login Page",  width = 100).grid(pady = 20, column = 1, row = 1)
        tkinter.Button(self.homePageWindow, width = 20, text = "Login", command = self.Login).grid(pady = 15, column = 1, row = 2)
        tkinter.Button(self.homePageWindow, width = 20, text = "Registration", command = self.Registration).grid(pady = 15, column = 1, row = 3)
        self.homePageWindow.mainloop()

    def Login(self):
        self.loginWindow = loginWindow()

    def Registration(self):
        self.regWindow = regWindow()


loginPage = LoginPage()