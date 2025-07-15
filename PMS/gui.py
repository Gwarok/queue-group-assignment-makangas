# File: gui.py
import tkinter as tk
from tkinter import messagebox, ttk
from database import DatabaseManager
from patient import Patient
from datastructures.queue import Queue

class PatientApp:
    def __init__(self, root):
        self.db = DatabaseManager()
        self.root = root
        self.root.title("Patient Management System")

        self.appointment_queue = Queue()  # initialize the queue

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
        self.add_btn.grid(row=3, column=0, pady=10)

        self.update_btn = tk.Button(form_frame, text="Update Patient", command=self.update_patient)
        self.update_btn.grid(row=3, column=1, pady=10)

        # Table Frame
        table_frame = tk.LabelFrame(root, text="Patient Records", padx=10, pady=10)
        table_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Age", "Gender"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Gender", text="Gender")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<ButtonRelease-1>", self.select_patient)

        # Delete Button
        self.delete_btn = tk.Button(root, text="Delete Selected Patient", command=self.delete_patient)
        self.delete_btn.pack(pady=5)

        # View Queue Button
        self.queue_btn = tk.Button(root, text="View Appointment Queue", command=self.view_queue)
        self.queue_btn.pack(pady=5)

        self.selected_id = None
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
        self.appointment_queue.enqueue(f"{name} ({gender}, {age})")  # add to queue
        messagebox.showinfo("Success", "Patient added and added to appointment queue")
        self.clear_form()
        self.load_patients()

    def update_patient(self):
        if not self.selected_id:
            messagebox.showerror("Error", "No patient selected to update")
            return

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

        self.db.update_patient(self.selected_id, name, age, gender)
        messagebox.showinfo("Success", "Patient updated successfully")
        self.clear_form()
        self.load_patients()

    def delete_patient(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "No patient selected")
            return

        values = self.tree.item(selected, 'values')
        patient_id = values[0]

        confirm = messagebox.askyesno("Confirm Delete", f"Delete patient {values[1]}?")
        if confirm:
            self.db.delete_patient(patient_id)
            messagebox.showinfo("Deleted", "Patient deleted successfully")
            self.clear_form()
            self.load_patients()

    def select_patient(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected, 'values')
        self.selected_id = values[0]
        self.name_var.set(values[1])
        self.age_var.set(values[2])
        self.gender_var.set(values[3])

    def clear_form(self):
        self.name_var.set("")
        self.age_var.set("")
        self.gender_var.set("")
        self.selected_id = None

    def load_patients(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.db.get_all_patients():
            self.tree.insert("", "end", values=row)

    def view_queue(self):
        queue_window = tk.Toplevel(self.root)
        queue_window.title("Appointment Queue")

        tk.Label(queue_window, text="Patients in Queue:", font=("Arial", 12)).pack(pady=10)
        queue_listbox = tk.Listbox(queue_window, width=40)
        queue_listbox.pack(padx=10, pady=10)

        for item in self.appointment_queue.display():
            queue_listbox.insert(tk.END, item)