import tkinter as tk
from tkinter import messagebox
from database.database_manager import DatabaseManager
from PIL import Image, ImageTk
from services.student_data_handler import StudentDataHandler

class StudentsInterface:
    def __init__(self, root, show_main_callback):
        self.root = root
        self.show_main_callback = show_main_callback
        self.frame = tk.Frame(self.root)
        self.data_handler = StudentDataHandler()

        # إعداد واجهة عرض الطلاب
        tk.Label(self.frame, text="Students", font=("Arial", 24)).pack(pady=10)

        # زر العودة للواجهة الرئيسية
        tk.Button(self.frame, text="Back", command=self.show_main_callback).pack(pady=10)

        self.students_list_frame = tk.Frame(self.frame)
        self.students_list_frame.pack()

        # تحميل بيانات الطلاب
        self.load_students()

    def hide(self):
        self.frame.pack_forget()

    def show(self):
        self.frame.pack(fill="both", expand=True)
        self.load_students()  # إعادة تحميل البيانات عند العرض

    def load_students(self):
        for widget in self.students_list_frame.winfo_children():
            widget.destroy()

        students = self.data_handler.fetch_students()

        for student in students:
            student_id, registration_number, name, image_path = student

            student_frame = tk.Frame(self.students_list_frame, bd=2, relief="solid")
            student_frame.pack(pady=5, padx=5, fill="x")

            try:
                img = Image.open(image_path)
                img = img.resize((100, 100))  # تغيير حجم الصورة حسب الحاجة
                img = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Failed to load image {image_path}: {e}")
                img = None  # تعيين None في حالة فشل التحميل
            img_label = tk.Label(student_frame, image=img)
            img_label.image = img  # Keep a reference to avoid garbage collection
            img_label.pack(side="left", padx=10)

            info = f"ID: {student_id}, Reg No: {registration_number}, Name: {name}"
            label = tk.Label(student_frame, text=info, anchor="w")
            label.pack(side="left", padx=10)
