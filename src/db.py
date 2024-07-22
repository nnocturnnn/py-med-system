import sqlite3
from dataclasses import asdict, dataclass


@dataclass
class Patient:
    id: str
    fName: str
    lName: str
    dob: str
    gender: str
    phone: str
    email: str


@dataclass
class PatientDetails:
    patient_id: str
    mob: str
    yob: str
    address: str
    bloodGroup: str
    history: str
    doctor: str
    filec: str


class Database:
    def __init__(self):
        self.dbConnection = sqlite3.connect("dbFile.db")
        self.dbCursor = self.dbConnection.cursor()
        self.create_tables()

    def __del__(self):
        self.dbCursor.close()
        self.dbConnection.close()

    def create_tables(self):
        """Create the necessary tables if they do not exist."""
        self.dbCursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                login TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
            """
        )
        self.dbCursor.execute(
            """
            CREATE TABLE IF NOT EXISTS patients (
                id TEXT PRIMARY KEY,
                fName TEXT NOT NULL,
                lName TEXT NOT NULL,
                dob TEXT NOT NULL,
                gender TEXT NOT NULL,
                phone TEXT,
                email TEXT UNIQUE NOT NULL
            )
            """
        )
        self.dbCursor.execute(
            """
            CREATE TABLE IF NOT EXISTS patient_details (
                patient_id TEXT,
                mob TEXT NOT NULL,
                yob TEXT NOT NULL,
                address TEXT,
                bloodGroup TEXT,
                history TEXT,
                doctor TEXT NOT NULL,
                filec TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients(id),
                FOREIGN KEY (doctor) REFERENCES users(login)
            )
            """
        )

    def insert_patient(self, patient: Patient, patient_details: PatientDetails):
        """Insert a new patient record into the database."""
        try:
            self.dbCursor.execute(
                """
                INSERT INTO patients (
                    id, fName, lName, dob, gender, phone, email
                ) VALUES (:id, :fName, :lName, :dob, :gender, :phone, :email)
                """,
                asdict(patient),
            )
            self.dbCursor.execute(
                """
                INSERT INTO patient_details (
                    patient_id, mob, yob, address, bloodGroup, history, doctor, filec
                ) VALUES (:patient_id, :mob, :yob, :address, :bloodGroup, :history, :doctor, :filec)
                """,
                asdict(patient_details),
            )
            self.dbConnection.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def update_patient(self, patient: Patient, patient_details: PatientDetails):
        """Update an existing patient record in the database."""
        try:
            self.dbCursor.execute(
                """
                UPDATE patients
                SET fName = :fName, lName = :lName, dob = :dob, gender = :gender, phone = :phone, email = :email
                WHERE id = :id
                """,
                asdict(patient),
            )
            self.dbCursor.execute(
                """
                UPDATE patient_details
                SET mob = :mob, yob = :yob, address = :address, bloodGroup = :bloodGroup, history = :history, doctor = :doctor, filec = :filec
                WHERE patient_id = :patient_id AND doctor = :doctor
                """,
                asdict(patient_details),
            )
            self.dbConnection.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def search_patient(self, id: str, doctor: str):
        """Search for a patient record by ID and doctor."""
        try:
            self.dbCursor.execute(
                """
                SELECT p.*, pd.mob, pd.yob, pd.address, pd.bloodGroup, pd.history, pd.filec
                FROM patients p
                JOIN patient_details pd ON p.id = pd.patient_id
                WHERE p.id = ? AND pd.doctor = ?
                """,
                (id, doctor),
            )
            searchResults = self.dbCursor.fetchall()
            return searchResults
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []

    def delete_patient(self, id: str, doctor: str):
        """Delete a patient record by ID and doctor."""
        try:
            self.dbCursor.execute(
                "DELETE FROM patient_details WHERE patient_id = ? AND doctor = ?",
                (id, doctor),
            )
            self.dbCursor.execute("DELETE FROM patients WHERE id = ?", (id,))
            self.dbConnection.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def display_patients(self, doctor: str):
        """Display all patient records for a given doctor."""
        try:
            self.dbCursor.execute(
                """
                SELECT p.*, pd.mob, pd.yob, pd.address, pd.bloodGroup, pd.history, pd.filec
                FROM patients p
                JOIN patient_details pd ON p.id = pd.patient_id
                WHERE pd.doctor = ?
                """,
                (doctor,),
            )
            records = self.dbCursor.fetchall()
            return records
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []

    def login(self, login: str, password: str):
        """Validate user login credentials."""
        try:
            self.dbCursor.execute(
                "SELECT password FROM users WHERE login = ?", (login,)
            )
            record = self.dbCursor.fetchone()
            if record is None:
                return False
            return record[0] == password
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return False

    def registration(self, login: str, password: str):
        """Register a new user."""
        try:
            self.dbCursor.execute(
                "INSERT INTO users (login, password) VALUES (?, ?)", (login, password)
            )
            self.dbConnection.commit()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
