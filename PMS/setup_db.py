from database import DatabaseManager

def setup():
    db = DatabaseManager()
    print("patients.db and 'patients' table created successfully.")

if __name__ == "__main__":
    setup()