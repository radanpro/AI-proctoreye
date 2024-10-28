import os
from services.image_vectorizer import ImageVectorizer
from database.database_manager import DatabaseManager

class StudentDataHandler:
    def __init__(self):
        self.vectorizer = ImageVectorizer()
        self.db_manager = DatabaseManager()

    def generate_student_id(self):
        """
        يقوم بتوليد student_id تلقائيًا كرقم متزايد.
        
        Returns:
            int: معرف الطالب الجديد.
        """
        connection = None
        cursor = None
        try:
            connection = self.db_manager.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT MAX(student_id) FROM students")  # جلب آخر student_id
            last_id = cursor.fetchone()[0]
            return (last_id + 1) if last_id is not None else 1
        except Exception as e:
            print(f"Error generating student ID: {e}")
            return None  # إرجاع None في حال وجود خطأ
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                self.db_manager.close()

    def save_student(self, student_data):
        """
        يحفظ بيانات الطالب في قاعدة البيانات بما في ذلك متجه ميزات الوجه.
        
        Args:
            student_data (dict): بيانات الطالب، مع مسار الصورة.
        
        Returns:
            bool: True إذا تم الحفظ بنجاح، False إذا كان هناك خطأ.
        """
        try:
            # توليد student_id تلقائيًا
            student_data['student_id'] = self.generate_student_id()
            if student_data['student_id'] is None:
                return False  # إذا فشل توليد معرف الطالب، أعد False
            
            # تحويل الصورة إلى متجه وتخزينها
            face_embedding = self.vectorizer.image_to_vector(student_data['image_path'])
            student_data['face_embedding'] = face_embedding.tolist()

            # الاتصال بقاعدة البيانات وحفظ البيانات
            connection = self.db_manager.connect()
            with connection:
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
                    str(student_data['face_embedding'])  # تأكد من تحويل المتجه إلى سلسلة نصية
                ))
                connection.commit()  # تأكد من تنفيذ العملية في قاعدة البيانات
            return True
        except Exception as e:
            print(f"Error saving student data: {e}")
            return False
