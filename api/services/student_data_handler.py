import os
from services.image_vectorizer import ImageVectorizer
from database.database_manager import DatabaseManager
import cv2

class StudentDataHandler:
    def __init__(self):
        self.vectorizer = ImageVectorizer()
        self.db_manager = DatabaseManager()

    def generate_student_id(self):
        connection = None
        cursor = None
        try:
            connection = self.db_manager.connect()
            cursor = connection.cursor()
            
            # التحقق من وجود بيانات في قاعدة البيانات
            cursor.execute("SELECT COUNT(*) FROM students")
            student_count = cursor.fetchone()[0]
            
            # إذا كانت قاعدة البيانات فارغة، بدأ من الرقم 0
            if student_count == 0:
                return 0

            # إذا كانت هناك بيانات، استخدم آخر student_id
            cursor.execute("SELECT MAX(student_id) FROM students")
            last_id = cursor.fetchone()[0]
            return (last_id + 1) if last_id is not None else 0

        except Exception as e:
            print(f"Error generating student ID: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                self.db_manager.close()

    def is_registration_number_exists(self, registration_number):
        connection = None
        cursor = None
        try:
            connection = self.db_manager.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM students WHERE registration_number = %s", (registration_number,))
            count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            print(f"Error checking registration number: {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                self.db_manager.close()

    def save_student(self, student_data):
        connection = None
        cursor = None
        try:
            # التحقق من وجود الرقم المسجل في قاعدة البيانات
            if self.is_registration_number_exists(student_data['registration_number']):
                raise ValueError(f"Student with registration number {student_data['registration_number']} already exists.")

            student_data['student_id'] = self.generate_student_id()
            if student_data['student_id'] is None:
                return False
            face_embedding = self.vectorizer.image_to_vector(cv2.imread(student_data['image_array']))
            # print("face_embedding",face_embedding)
            student_data['face_embedding'] = face_embedding.tolist()

            connection = self.db_manager.connect()
            cursor = connection.cursor()
            sql = """
            INSERT INTO students (student_id, registration_number, name, image_path, face_embedding)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                student_data['student_id'],
                student_data['registration_number'],
                student_data['name'],
                student_data['image_path'],
                str(student_data['face_embedding'])
            ))
            connection.commit()
            return True
        except Exception as e:
            error_message = f"Error saving student data: {str(e)}"
            raise ValueError(error_message)
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                self.db_manager.close()

    def fetch_students(self):
        connection = None
        cursor = None
        try:
            connection = self.db_manager.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT student_id, registration_number, name, image_path FROM students")
            students = cursor.fetchall()
            return students
        except Exception as e:
            print(f"Error fetching student data: {e}")
            return []
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                self.db_manager.close()
