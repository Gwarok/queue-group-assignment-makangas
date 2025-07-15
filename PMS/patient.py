class Patient:
    def __init__(self, patient_id, name, age, gender):
        self.id = patient_id
        self.name = name
        self.age = age
        self.gender = gender

    def __str__(self):
        return f"{self.id}: {self.name}, {self.age}, {self.gender}"