import tkinter as tk
from tkinter import messagebox
from database.database_manager import DatabaseManager

class StudentsInterface:
    def __init__(self, root, show_main_callback):
        self.root = root
        self.show_main_callback = show_main_callback
        self.frame = tk.Frame(self.root)

        # إعداد واجهة عرض الطلاب
        tk.Label(self.frame, text="Students", font=("Arial", 24)).pack(pady=10)

        # زر العودة للواجهة الرئيسية
        tk.Button(self.frame, text="Back", command=self.show_main_callback).pack(pady=10)

        self.students_list_frame = tk.Frame(self.frame)
        self.students_list_frame.pack()

        # تحميل بيانات الطلاب
        self.load_students()

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()

    def load_students(self):
        db_manager = DatabaseManager()
        connection = db_manager.connect()

        cursor = connection.cursor()
        cursor.execute("SELECT student_id, student_registration_number, name, image_path FROM students")
        students = cursor.fetchall()

        for student in students:
            student_id, registration_number, name, image_path = student

            student_frame = tk.Frame(self.students_list_frame, bd=2, relief="solid")
            student_frame.pack(pady=5, padx=5, fill="x")

            img = tk.PhotoImage(file=image_path)  # Assuming image_path is the path to the image
            img_label = tk.Label(student_frame, image=img)
            img_label.image = img  # Keep a reference to avoid garbage collection
            img_label.pack(side="left", padx=10)

            info = f"ID: {student_id}, Reg No: {registration_number}, Name: {name}"
            label = tk.Label(student_frame, text=info, anchor="w")
            label.pack(side="left", padx=10)

        cursor.close()
        db_manager.close()
