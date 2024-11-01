import os
from services.image_vectorizer import ImageVectorizer
from database.database_manager import DatabaseManager

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
            cursor.execute("SELECT MAX(student_id) FROM students")
            last_id = cursor.fetchone()[0]
            return (last_id + 1) if last_id is not None else 1
        except Exception as e:
            print(f"Error generating student ID: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                self.db_manager.close()

    def save_student(self, student_data):
        connection = None
        cursor = None
        try:
            student_data['student_id'] = self.generate_student_id()
            if student_data['student_id'] is None:
                return False
            
            face_embedding = self.vectorizer.image_to_vector(student_data['image_array'])
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
            print(f"Error saving student data: {e}")
            return False
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
