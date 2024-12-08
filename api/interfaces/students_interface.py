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

        # إضافة Canvas و Scrollbar
        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # تغليف `scrollable_frame` لضمان التوسيط
        self.center_frame = tk.Frame(self.scrollable_frame)
        self.center_frame.pack(expand=True, fill="both")

        # إعداد وزن الأعمدة لجعلها مرنة
        num_students_per_row = 4  # عدد الطلاب في الصف الواحد
        for col in range(num_students_per_row):
            self.center_frame.grid_columnconfigure(col, weight=1)

        # تحميل بيانات الطلاب
        self.load_students()

    def hide(self):
        self.frame.pack_forget()

    def show(self):
        self.frame.pack(fill="both", expand=True)
        self.load_students()  # إعادة تحميل البيانات عند العرض

    def load_students(self):
        # مسح محتويات center_frame قبل إعادة التحميل
        for widget in self.center_frame.winfo_children():
            widget.destroy()

        students = self.data_handler.fetch_students()
        num_students_per_row = 4  # عدد الطلاب في الصف الواحد

        for index, student in enumerate(students):
            student_id, registration_number, name, image_path = student

            # إنشاء إطار الطالب ووضعه في الشبكة
            student_frame = tk.Frame(self.center_frame, bd=2, relief="solid", bg="#e0f7fa", highlightbackground="#00bcd4", highlightthickness=2)
            student_frame.grid(row=index // num_students_per_row, column=index % num_students_per_row, padx=5, pady=5, sticky="nsew")

            # تمديد كل طالب لملء المساحة المتاحة
            self.center_frame.grid_rowconfigure(index // num_students_per_row, weight=1)

            try:
                img = Image.open(image_path)
                img = img.resize((150, 150))  # تغيير حجم الصورة ليكون مرنًا لاحقًا
                img = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Failed to load image {image_path}: {e}")
                img = None  # تعيين None في حالة فشل التحميل

            img_label = tk.Label(student_frame, image=img)
            img_label.image = img  # Keep a reference to avoid garbage collection
            img_label.pack(pady=5, expand=True, fill="both")

            name_label = tk.Label(student_frame, text=name, font=("Arial", 14, "bold"), bg="#e0f7fa")
            name_label.pack(pady=2)

            reg_number_label = tk.Label(student_frame, text=f"Reg No: {registration_number}", font=("Arial", 12), bg="#e0f7fa")
            reg_number_label.pack(pady=2)
