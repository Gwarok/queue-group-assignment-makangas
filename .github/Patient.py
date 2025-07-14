class Patient:
    def _init_(self, patient_id, name, age, gender):
        self.id = patient_id
        self.name = name
        self.age = age
        self.gender = gender

    def _str_(self):
        return f"{self.id}: {self.name}, {self.age}, {self.gender}"