import tkinter as tk
from tkinter import messagebox, ttk
from database import DatabaseManager
from patient import Patient

class PatientApp:
    def __init__(self, root):
        self.db = DatabaseManager()
        self.root = root
        self.root.title("Patient Management System")

        # Form Frame
        form_frame = tk.LabelFrame(root, text="Add / Update Patient", padx=10, pady=10)
        form_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="e")
        tk.Label(form_frame, text="Age:").grid(row=1, column=0, sticky="e")
        tk.Label(form_frame, text="Gender:").grid(row=2, column=0, sticky="e")

        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.gender_var = tk.StringVar()

        tk.Entry(form_frame, textvariable=self.name_var).grid(row=0, column=1)
        tk.Entry(form_frame, textvariable=self.age_var).grid(row=1, column=1)
        tk.Entry(form_frame, textvariable=self.gender_var).grid(row=2, column=1)

        self.add_btn = tk.Button(form_frame, text="Add Patient", command=self.add_patient)
        self.add_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # Table Frame
        table_frame = tk.LabelFrame(root, text="Patient Records", padx=10, pady=10)
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Age", "Gender"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Gender", text="Gender")
        self.tree.pack(fill="both", expand=True)

        self.load_patients()

    def add_patient(self):
        name = self.name_var.get().strip()
        age = self.age_var.get().strip()
        gender = self.gender_var.get().strip()

        if not name or not age or not gender:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Error", "Age must be a number")
            return

        self.db.add_patient(name, age, gender)
        messagebox.showinfo("Success", "Patient added successfully")
        self.name_var.set("")
        self.age_var.set("")
        self.gender_var.set("")
        self.load_patients()

    def load_patients(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.db.get_all_patients():
            self.tree.insert("", "end", values=row)


if __name__ == "__main__":
    root = tk.Tk()
    app = PatientApp(root)
    root.mainloop()
