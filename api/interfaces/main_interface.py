import tkinter as tk
from tkinter import messagebox
from database.database_manager import DatabaseManager

class MainInterface:
    def __init__(self, root, app, show_comparison_callback, check_db_connection_callback):
        self.root = root
        self.app = app  # حفظ الكائن app
        self.show_comparison_callback = show_comparison_callback
        self.check_db_connection_callback = check_db_connection_callback
        self.frame = tk.Frame(self.root)

        # تقسيم الواجهة إلى Header, Main, Footer
        self.header = tk.Frame(self.frame, bg="lightblue", height=50)
        self.main = tk.Frame(self.frame, bg="white", height=400)
        self.footer = tk.Frame(self.frame, bg="lightgray", height=30)

        # إعداد الـ Header
        self.header.pack(fill="x")
        tk.Button(self.header, text="Go to Comparison", command=self.show_comparison_callback).pack(side="left", padx=10, pady=5)
        tk.Button(self.header, text="Check DB Connection", command=self.check_db_connection).pack(side="left", padx=10, pady=5)
        tk.Button(self.header, text="View Students", command=self.show_students_callback).pack(side="left", padx=10, pady=5)  # زر جديد
        tk.Button(self.header, text="Add Student", command=self.add_student_callback).pack(side="left", padx=10, pady=5)  # زر لإضافة الطلاب

        # إعداد الـ Main
        self.main.pack(fill="both", expand=True)
        self.status_label = tk.Label(self.main, text="Welcome to the Student Verification System", bg="white")
        self.status_label.pack(pady=20)

        # إعداد الـ Footer
        self.footer.pack(fill="x")
        tk.Label(self.footer, text="Footer - Student Verification System", bg="lightgray").pack(pady=5)

    def show_students_callback(self):
        self.app.show_students_interface()  # استخدام الكائن app
    
    def add_student_callback(self):
        self.app.show_add_student_interface()  # استخدام الكائن app
    
    def show_comparison_callback(self):
        self.app.show_comparison_interface()  # استخدام الكائن app

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()

    def check_db_connection(self):
        # تحقق من الاتصال بقاعدة البيانات
        is_connected = self.check_db_connection_callback()
        if is_connected:
            self.status_label.config(text="Connected to the database successfully.", fg="green")
            messagebox.showinfo("Connection Status", "Connected to the database successfully.")
        else:
            self.status_label.config(text="Failed to connect to the database.", fg="red")
            messagebox.showerror("Connection Status", "Failed to connect to the database.")
