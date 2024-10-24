import tkinter as tk
from tkinter import messagebox

class AddStudentInterface:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # حفظ الكائن app
        self.frame = tk.Frame(self.root)

        # إعداد واجهة إضافة الطلاب
        # لا نقوم بـ pack هنا لضمان أنها لن تظهر في البداية

        tk.Label(self.frame, text="Add New Student", font=("Arial", 16)).pack(pady=10)

        self.name_entry = tk.Entry(self.frame, width=50)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Enter Student Name")

        self.submit_button = tk.Button(self.frame, text="Add Student", command=self.add_student)
        self.submit_button.pack(pady=5)

        self.back_button = tk.Button(self.frame, text="Back to Main", command=self.go_back)
        self.back_button.pack(pady=5)

    def add_student(self):
        student_name = self.name_entry.get()
        if student_name:  # تأكد من وجود اسم
            messagebox.showinfo("Success", f"Student '{student_name}' added successfully!")
            self.name_entry.delete(0, tk.END)  # مسح حقل الإدخال
        else:
            messagebox.showerror("Error", "Please enter a student name.")

    def go_back(self):
        self.frame.pack_forget()  # إخفاء واجهة إدخال الطلاب
        self.app.show_main_interface()  # العودة إلى الواجهة الرئيسية

    def show(self):
        self.frame.pack(fill="both", expand=True)  # استخدم هذه الدالة عند الحاجة لإظهار الواجهة
