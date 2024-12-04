from fastapi import APIRouter, Form, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
import cv2
import os
from services_v2.embedding_storage import EmbeddingStorage
from services_v2.identity_verifier import IdentityVerifier
from services_v2.embedding_generator import EmbeddingGenerator
from database.database_manager import DatabaseManager
from deepface import DeepFace

from services.image_comparer import ImageComparer  # تأكد من أنك قد أنشأت هذه الخدمة بشكل صحيح
from database.database_manager import DatabaseManager
import face_recognition


router = APIRouter()

# تهيئة الكلاسات
embedding_storage = EmbeddingStorage()
identity_verifier = IdentityVerifier()
embedding_generator = EmbeddingGenerator()

@router.post("/compare_image_deepface")
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
                            "average_similarity": result1,
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


@router.post("/compare_image_recognition")
async def compare_image(registration_number: str = Form(...), captured_image: UploadFile = File(...)):
    try:
        # قراءة البيانات الخاصة بالصورة الملتقطة
        print('captured_image_data dddd')  # تعليق لتتبع البيانات
        captured_image_data = np.frombuffer(await captured_image.read(), np.uint8)
        # print('captured_image_data',captured_image_data) 
        captured_image_array = cv2.imdecode(captured_image_data, cv2.IMREAD_COLOR)
        # print('captured_image_array',captured_image_array)  
        if captured_image_array is None:
            raise HTTPException(status_code=400, detail="Invalid image file. Unable to process the uploaded file.")

        stored_embedding = embedding_storage.get_embedding(registration_number)
        # print('stored_embedding : ',stored_embedding)

        if stored_embedding is not None:
            # توليد الـ embedding من الصورة الملتقطة
            print('stored_embedding is not none : ')
            # print('image_extension : ',image_extension)
            captured_image_path = f"./temp_captured_image.jpg"
            cv2.imwrite(captured_image_path, captured_image_array)
            # print('captured_image_path : ',captured_image_path)

            captured_embedding = embedding_generator.generate_embedding(captured_image_path)
            # حذف الصورة المؤقتة بعد توليد الـ embedding
            if os.path.exists(captured_image_path):
                os.remove(captured_image_path)

            # print('captured_embedding : ',captured_embedding)
            # print('stored_embedding : ',stored_embedding)
            if captured_embedding:
                # مقارنة الـ embeddings باستخدام IdentityVerifier
                match, similarity = identity_verifier.verify_identity(stored_embedding, captured_embedding)
                print('match', match)
                print('similarity', similarity)
                if match:
                    return JSONResponse(content={"status": "success", "message": "Student match found", "similarity": similarity}, status_code=200)
                else:
                    return JSONResponse(content={"status": "success", "message": "No match found", "similarity": similarity}, status_code=200)
            else:
                return JSONResponse(content={"status": "error", "message": "Failed to generate embedding for captured image"}, status_code=500)
        else:
            return JSONResponse(content={"status": "error", "message": "Student not found or no embedding available"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": f"Error occurred: {str(e)}"}, status_code=500)

