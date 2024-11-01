import tkinter as tk
from interfaces.main_interface import MainInterface
from interfaces.comparison_interface import ComparisonInterface
from interfaces.students_interface import StudentsInterface
from interfaces.add_student_interface import AddStudentInterface
from database.database_manager import DatabaseManager

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Identity Verification")
        self.root.geometry("800x600")

        # Create instances of the interfaces
        self.main_interface = MainInterface(self.root, self, self.show_comparison_interface, self.check_db_connection)
        self.comparison_interface = ComparisonInterface(self.root, self.show_main_interface)
        self.students_interface = StudentsInterface(self.root, self.show_main_interface)
        self.add_student_interface = AddStudentInterface(self.root, self)  # إنشاء واجهة إضافة الطلاب

        # Show the main interface initially
        self.main_interface.show()  # تأكد من استدعاء هذه الدالة فقط

    def show_main_interface(self):
        self.comparison_interface.hide()
        self.students_interface.hide()
        self.add_student_interface.frame.pack_forget()  # إخفاء واجهة إضافة الطلاب
        self.main_interface.show()

    def show_comparison_interface(self):
        self.main_interface.hide()
        self.students_interface.hide()
        self.add_student_interface.frame.pack_forget()  # إخفاء واجهة إضافة الطلاب
        self.comparison_interface.show()

    def show_students_interface(self):
        self.main_interface.hide()
        self.comparison_interface.hide()
        self.add_student_interface.frame.pack_forget()  # إخفاء واجهة إضافة الطلاب
        self.students_interface.show()

    def show_add_student_interface(self):
        self.main_interface.hide()
        self.comparison_interface.hide()
        self.students_interface.hide()
        self.add_student_interface.show()
        # أعادة تحميل واجهة عرض الطلاب لضمان تحديثها
        self.students_interface.load_students()


    def check_db_connection(self):
        try:
            db_manager = DatabaseManager(host="localhost", user="root", password="password", database="students_db")
            connection = db_manager.connect()
            if connection.is_connected():
                connection.close()
                return True
            else:
                return False
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
