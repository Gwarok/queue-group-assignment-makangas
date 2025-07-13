import sqlite3

class DatabaseManager:
    def __init__(self, db_name="patients.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_patient(self, name, age, gender):
        self.cursor.execute("INSERT INTO patients (name, age, gender) VALUES (?, ?, ?)", (name, age, gender))
        self.conn.commit()

    def get_all_patients(self):
        self.cursor.execute("SELECT * FROM patients")
        return self.cursor.fetchall()

    def update_patient(self, patient_id, name, age, gender):
        self.cursor.execute("UPDATE patients SET name=?, age=?, gender=? WHERE id=?", (name, age, gender, patient_id))
        self.conn.commit()

    def delete_patient(self, patient_id):
        self.cursor.execute("DELETE FROM patients WHERE id=?", (patient_id,))
        self.conn.commit()
