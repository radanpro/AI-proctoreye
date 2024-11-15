from fastapi import APIRouter, Form, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import cv2
from services.image_comparer import ImageComparer  # تأكد من أنك قد أنشأت هذه الخدمة بشكل صحيح
from database.database_manager import DatabaseManager
import face_recognition

router = APIRouter()

@router.post("/compare_image")
async def compare_image(registration_number: str = Form(...), captured_image: UploadFile = File(...)):
    try:
        # التحقق من وجود الكائن ImageComparer
        comparer = ImageComparer()
        
        # قراءة البيانات الخاصة بالصورة الملتقطة
        print('captured_image_data dddd')  # تعليق لتتبع البيانات
        captured_image_data = np.frombuffer(await captured_image.read(), np.uint8)
        # print('captured_image_data',captured_image_data)  # تعليق لفحص بيانات الصورة
        captured_image_array = cv2.imdecode(captured_image_data, cv2.IMREAD_COLOR)
        # print('captured_image_array',captured_image_array)  # تعليق لفحص الصورة المحوَّلة
        connection = DatabaseManager().connect()  # تأكد من استخدام db_manager بشكل صحيح
        cursor = connection.cursor()
        cursor.execute("SELECT image_path, face_embedding FROM students WHERE registration_number = %s ORDER BY student_id DESC", (registration_number,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            stored_image_path = result[0]
            # stored_image_path = result[1]
            stored_encoding = comparer.image_to_vector(stored_image_path)
            stored_face_embedding = np.array(eval(result[1]))
            # print('stored_encoding',stored_encoding)  # تعليق لفحص البيانات المخزنة

            # الكشف عن الوجوه في الصورة الملتقطة
            face_locations = face_recognition.face_locations(captured_image_array)
            face_encodings = face_recognition.face_encodings(captured_image_array, face_locations)

            if face_encodings:
                # مقارنة المتجهات
                captured_encoding = face_encodings[0]
                similarity_percentage_1 = comparer.compare_vectors(stored_encoding, captured_encoding)
                similarity_percentage_2 = comparer.compare_vectors(stored_face_embedding, captured_encoding)
                
                # حساب المتوسط بين المقارنتين
                average_similarity = (similarity_percentage_1 + similarity_percentage_2) / 2
                # print('average_similarity',average_similarity)  # تعليق لفحص المتوسط بين المقارنتين

                # تحديد العتبة لاعتبار المطابقة (مثال: 70%)
                similarity_threshold = 70  # العتبة لتحديد المطابقة

                if average_similarity >= similarity_threshold:
                    return JSONResponse(content={"status": "success", "message": "Student match found", "average_similarity": average_similarity}, status_code=200)
                else:
                    return JSONResponse(content={"status": "success", "message": "No match found", "average_similarity": average_similarity}, status_code=200)
            else:
                return JSONResponse(content={"status": "error", "message": "No faces detected in captured image"}, status_code=400)
        else:
            return JSONResponse(content={"status": "error", "message": "Student not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": f"Error occurred: {str(e)}"}, status_code=500)
