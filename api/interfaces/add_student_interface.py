import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog
from services.student_data_handler import StudentDataHandler
import cv2  # إضافة مكتبة cv2 لتحميل الصورة كـ numpy array

class AddStudentInterface:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.frame = tk.Frame(self.root)
        self.data_handler = StudentDataHandler()

        tk.Label(self.frame, text="Add New Student", font=("Arial", 16)).pack(pady=10)

        # حقل رقم تسجيل الطالب
        tk.Label(self.frame, text="Student Registration Number").pack()
        self.registration_number_entry = tk.Entry(self.frame, width=50)
        self.registration_number_entry.pack(pady=5)

        # حقل اسم الطالب
        tk.Label(self.frame, text="Student Name").pack()
        self.name_entry = tk.Entry(self.frame, width=50)
        self.name_entry.pack(pady=5)

        # حقل تحميل الصورة
        tk.Label(self.frame, text="Upload Student Image").pack()
        self.image_path = ""
        self.image_button = tk.Button(self.frame, text="Choose Image", command=self.select_image)
        self.image_button.pack(pady=5)

        # زر إضافة الطالب
        self.submit_button = tk.Button(self.frame, text="Add Student", command=self.add_student)
        self.submit_button.pack(pady=5)

        # زر العودة
        self.back_button = tk.Button(self.frame, text="Back to Main", command=self.go_back)
        self.back_button.pack(pady=5)

    def select_image(self):
        original_image_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if original_image_path:
            # تحديد المسار لحفظ الصورة داخل مجلد "images"
            save_directory = "images"
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)  # إنشاء المجلد إذا لم يكن موجودًا

            # حفظ الصورة في مجلد "images" بالاسم الأصلي
            self.image_path = os.path.join(save_directory, os.path.basename(original_image_path))
            shutil.copy2(original_image_path, self.image_path)  # نسخ الصورة

            messagebox.showinfo("Image Selected", f"Selected Image: {self.image_path}")

    def add_student(self):
        registration_number = self.registration_number_entry.get()
        student_name = self.name_entry.get()
        
        if registration_number and student_name and self.image_path:
            # قراءة الصورة كـ numpy array
            image = cv2.imread(self.image_path)
            if image is None:
                messagebox.showerror("Error", "Failed to read the image.")
                return

            # تجهيز بيانات الطالب بدون student_id (سيتم توليده تلقائيًا)
            student_data = {
                'student_id': self.data_handler.generate_student_id(),  # توليد معرف الطالب تلقائيًا
                'registration_number': registration_number,
                'name': student_name,
                'image_path': self.image_path,
                'image_array': image  # تمرير الصورة كـ numpy array
            }
            # حفظ بيانات الطالب باستخدام data_handler
            if self.data_handler.save_student(student_data):
                messagebox.showinfo("Success", f"Student '{student_name}' added successfully!")
                self.reset_fields()
            else:
                messagebox.showerror("Error", "Failed to add student.")
        else:
            messagebox.showerror("Error", "Please fill all fields and select an image.")

    def reset_fields(self):
        self.registration_number_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.image_path = ""

    def go_back(self):
        self.frame.pack_forget()
        self.app.show_main_interface()

    def show(self):
        self.frame.pack(fill="both", expand=True)
