from fastapi import APIRouter, Form, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import cv2
from services_v2.embedding_storage import EmbeddingStorage
from services_v2.identity_verifier import IdentityVerifier
from database.database_manager import DatabaseManager
from deepface import DeepFace

router = APIRouter()

# تهيئة الكلاسات
embedding_storage = EmbeddingStorage()
identity_verifier = IdentityVerifier()

@router.post("/compare_image")
async def compare_image(registration_number: str = Form(...), captured_image: UploadFile = File(...)):
    try:
        
        # قراءة البيانات الخاصة بالصورة الملتقطة
        print('captured_image_data dddd')  # تعليق لتتبع البيانات
        captured_image_data = np.frombuffer(await captured_image.read(), np.uint8)
        # print('captured_image_data',captured_image_data)  # تعليق لفحص بيانات الصورة
        captured_image_array = cv2.imdecode(captured_image_data, cv2.IMREAD_COLOR)
        # print('captured_image_array',captured_image_array)  # تعليق لفحص الصورة المحوَّلة

        # حفظ الصورة المؤقتة على القرص لاستخدامها مع DeepFace
        temp_image_path = "temp_captured_image.jpg"
        cv2.imwrite(temp_image_path, captured_image_array)


        connection = DatabaseManager().connect()  # تأكد من استخدام db_manager بشكل صحيح
        cursor = connection.cursor()
        cursor.execute("SELECT image_path, face_embedding FROM students WHERE registration_number = %s ORDER BY student_id DESC", (registration_number,))
        result = cursor.fetchone()
        cursor.close()
        print('result', result)

        if result:
            stored_image_path = result[0]
            # تعليق لفحص البيانات المخزنة
            stored_image = cv2.imread(stored_image_path)

            try:
                # print('result2', stored_image)
                models = [
                    "VGG-Face", 
                    "Facenet", 
                    "Facenet512", 
                    "OpenFace", 
                    "DeepFace", 
                    "DeepID", 
                    "ArcFace", 
                    "Dlib", 
                    "SFace",
                    "GhostFaceNet",
                    ]

                print('stored_image_path', stored_image_path)
                print('temp_image_path', temp_image_path)
                # مقارنة الصورة الملتقطة مع الصورة المخزنة باستخدام DeepFace
                result1 = DeepFace.verify(img1_path =stored_image_path, img2_path =temp_image_path,model_name = models[0],)
                # حذف الصورة المؤقتة
                print('result3', result1)
                # os.remove(temp_image_path)

                # التحقق من نتيجة المقارنة
                if result1["verified"]:
                    print('dsdafasfd')
                    return JSONResponse(
                        content={
                            "status": "success",
                            "message": "Student Match found",
                            "average_similarity": result1['distance'],
                        },
                        status_code=200,
                    )
                else:
                    return JSONResponse(
                        content={
                            "status": "success",
                            "message": "No match found",
                            "average_similarity": result1["distance"],
                        },
                        status_code=200,
                    )
            except Exception as e:
                os.remove(temp_image_path)
                return JSONResponse(
                    content={"status": "error", "message": f"Error during image comparison: {str(e)}"},
                    status_code=500,
                )
        else:
            os.remove(temp_image_path)
            return JSONResponse(content={"status": "error", "message": "Student not found"}, status_code=404)

    except Exception as e:
        return JSONResponse(content={"status": "error", "message": f"Error occurred: {str(e)}"}, status_code=500)
