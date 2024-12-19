from fastapi import APIRouter, Form, File, UploadFile, Response, HTTPException
from fastapi.responses import JSONResponse
import numpy as np
import cv2
import os
import json
from datetime import datetime
from services_v2.embedding_storage import EmbeddingStorage
from services_v2.identity_verifier import IdentityVerifier
from services_v2.embedding_generator import EmbeddingGenerator
from services_v2.identity_recognizer import FiassEmbeddingSearch
from database.database_manager import DatabaseManager
from deepface import DeepFace
from io import BytesIO
import base64 


import face_recognition


router = APIRouter()

def send_exam_status_to_api(student, next_exam_date, message, status_code=403):
    content={
        "status": "error",
        "message":message,
        "student_data":{
            "name":student[1],
            "registration_number":student[2],
            "college":student[3],
            "level":student[4],
            "specialization":student[5],
        },
        "next_exam_date":next_exam_date,
    }
    return Response(content=json.dumps(content), media_type="application/json", status_code=status_code)

@router.post("/compare_image_deepface")
async def compare_image(registration_number: str = Form(...), captured_image: UploadFile = File(...)):
    # تهيئة الكلاسات
    embedding_storage = EmbeddingStorage()
    identity_verifier = IdentityVerifier()
    embedding_generator = EmbeddingGenerator()
    try:
        db_manager = DatabaseManager()
        db_manager.connect()
        db_manager.create_tables()
        print('captured_image_data dddd')  # تعليق لتتبع البيانات
        student_data = db_manager.student_db.find(Number=registration_number)
        if not student_data:
            db_manager.close()
            return Response(
                content=json.dumps({"status": "error", "message": "Student not found."}),media_type="application/json",status_code=404
            )
        student = student_data[0]  # بيانات الطالب
        student_college = student[3]  # الكلية
        student_level = student[4]  # المستوى
        student_specialization = student[5]  # التخصص
        
        # التحقق من جدول الامتحانات
        today = datetime.today().strftime("%Y-%m-%d")
        # print('student_specialization',student_specialization)
        # print('student_data',student_data)
        # print('student_level',student_level)
        # print('student_level',type(student_level))
        # print('today',today)
        # print(type(today))

        exam_data = db_manager.exam_db.find(
            Date=today, Specialization=student_specialization, Level=student_level
        )
        # print('exam_data')
        # print(exam_data)
        # print('today',today)
        if not exam_data:
            # العثور على أقرب امتحان
            upcoming_exam = db_manager.exam_db.all(
                Specialization=student_specialization, Level=student_level
            )
            next_exam_date = min([exam[1] for exam in upcoming_exam]) if upcoming_exam else "No upcoming exams"
            db_manager.close()
            print("next_exam_date",next_exam_date)
            return send_exam_status_to_api(student, next_exam_date, f"Today is not the exam date. Next exam is on {next_exam_date}.", 403)
        
        # for exam in exam_data:
        #     print(f"Exam found: {exam}")
        captured_image_data = np.frombuffer(await captured_image.read(), np.uint8)
        # print('captured_image_data',captured_image_data)  # تعليق لفحص بيانات الصورة
        captured_image_array = cv2.imdecode(captured_image_data, cv2.IMREAD_COLOR)
        # print('captured_image_array',captured_image_array)  # تعليق لفحص الصورة المحوَّلة

        if captured_image_array is None:
            print("db_manager.close()")
            db_manager.close()
            raise HTTPException(status_code=400, detail="Invalid image file.")

        # استرجاع الـ embedding المخزن
        stored_embedding = embedding_storage.get_embedding(registration_number)
        # print('stored_embedding',stored_embedding)
        if not stored_embedding:
            db_manager.close()
            return JSONResponse(
                content={
                    "status": "error",
                    "message": "No embedding found for the student.",
                    "student_data":{
                        "name":student[1],
                        "registration_number":student[2],
                        "college":student[3],
                        "level":student[4],
                        "specialization":student[5],
                    },
                },
                status_code=404,
            )

        
        # حفظ الصورة المؤقتة على القرص لاستخدامها مع DeepFace
        temp_image_path = "temp_captured_image.jpg"
        cv2.imwrite(temp_image_path, captured_image_array)
        if not cv2.imwrite(temp_image_path, captured_image_array):
            raise ValueError("Failed to write captured image to disk.")
        print('asdfasdf')

        captured_embedding = embedding_generator.generate_embedding(temp_image_path)
        # print('captured_embedding',captured_embedding)
        os.remove(temp_image_path)
        
        if not captured_embedding:
            return JSONResponse(
                content={"status": "error", "message": "Failed to generate embedding."},
                status_code=500,
            )
        
        # مقارنة الـ embeddings
        match, similarity = identity_verifier.verify_identity(
            stored_embedding, captured_embedding
        )

        if match:
            db_manager.close()
            return JSONResponse(
                content={
                    "status": "success",
                    "message": "Student verified successfully.",
                    "similarity": similarity,
                    "student_data":{
                        "name":student[1],
                        "registration_number":student[2],
                        "college":student[3],
                        "level":student[4],
                        "specialization":student[5],
                    },
                },
                status_code=200,
            )
        else:
            db_manager.close()
            return JSONResponse(
                content={
                    "status": "error",
                    "message": "Student verification failed.",
                    "student_data":{
                        "name":student[1],
                        "registration_number":student[2],
                        "college":student[3],
                        "level":student[4],
                        "specialization":student[5],
                    },
                    "similarity": similarity,
                },
                status_code=401,
            )
    except Exception as e:
        db_manager.close()
        return JSONResponse(content={"status": "error", "message": f"Error occurred: {str(e)}"}, status_code=500)
    


@router.post("/compare_image_recognition")
async def compare_image(registration_number: str = Form(...), captured_image: UploadFile = File(...)):
    # تهيئة الكلاسات
    embedding_storage = EmbeddingStorage()
    identity_verifier = IdentityVerifier()
    embedding_generator = EmbeddingGenerator()
    

    try:
        db_manager = DatabaseManager()
        db_manager.connect()
        db_manager.create_tables()
        print("captured_image_data ssdsd")
        # استرجاع بيانات الطالب
        student_data = db_manager.student_db.find(Number=registration_number)
        print("student_data : ", student_data)

        if not student_data:
            db_manager.close()
            return JSONResponse(
                content={"status": "error", "message": "Student not found."},
                status_code=404,
            )
        
        student = student_data[0]  # بيانات الطالب
        student_level = student[4]  # المستوى
        student_specialization = student[5]  # التخصص

        # التحقق من جدول الامتحانات
        today = datetime.today().strftime("%Y-%m-%d")
        exam_data = db_manager.exam_db.find(
            Date=today, Specialization=student_specialization, Level=student_level
        )

        if not exam_data:
            # العثور على أقرب امتحان
            upcoming_exam = db_manager.exam_db.all(
                Specialization=student_specialization, Level=student_level
            )
            next_exam_date = min([exam[1] for exam in upcoming_exam]) if upcoming_exam else "No upcoming exams"
            db_manager.close()
            print('next_exam_date', next_exam_date)
            return send_exam_status_to_api(student, next_exam_date, f"Today is not the exam date. Next exam is on {next_exam_date}.")

        # قراءة البيانات الخاصة بالصورة الملتقطة
        captured_image_data = np.frombuffer(await captured_image.read(), np.uint8)
        captured_image_array = cv2.imdecode(captured_image_data, cv2.IMREAD_COLOR)
        if captured_image_array is None:
            db_manager.close()
            raise HTTPException(status_code=400, detail="Invalid image file.")

        # استرجاع الـ embedding المخزن
        stored_embedding = embedding_storage.get_embedding(registration_number)
        if not stored_embedding:
            db_manager.close()
            return JSONResponse(
                content={
                    "status": "error",
                    "message": "No embedding found for the student.",
                    "student_data":{
                        "name":student[1],
                        "registration_number":student[2],
                        "college":student[3],
                        "level":student[4],
                        "specialization":student[5],
                    },
                },
                status_code=404,
            )

        # توليد embedding للصورة الملتقطة
        captured_image_path = "temp_captured_image.jpg"
        cv2.imwrite(captured_image_path, captured_image_array)
        captured_embedding = embedding_generator.generate_embedding(
            captured_image_path
        )
        os.remove(captured_image_path)  # حذف الصورة المؤقتة

        if not captured_embedding:
            db_manager.close()
            return JSONResponse(
                content={"status": "error", "message": "Failed to generate embedding."},
                status_code=500,
            )

        # مقارنة الـ embeddings باستخدام IdentityVerifier
        match, similarity = identity_verifier.verify_identity(
            stored_embedding, captured_embedding
        )
        if match:
            db_manager.close()
            return JSONResponse(
                content={
                    "status": "success",
                    "message": "Student verified successfully.",
                    "student_data":{
                        "name":student[1],
                        "registration_number":student[2],
                        "college":student[3],
                        "level":student[4],
                        "specialization":student[5],
                    },
                    "similarity": similarity,
                },
                status_code=200,
            )
        else:
            db_manager.close()
            return JSONResponse(
                content={
                    "status": "error",
                    "message": "Student verification failed.",
                    "student_data":{
                        "name":student[1],
                        "registration_number":student[2],
                        "college":student[3],
                        "level":student[4],
                        "specialization":student[5],
                    },
                    "similarity": similarity,
                },
                status_code=401,
            )

    except Exception as e:
        db_manager.close()
        return JSONResponse(
            content={"status": "error", "message": f"Error occurred: {str(e)}"},
            status_code=500,
        )

@router.post("/search_image")
async def search_image(captured_image:UploadFile = File(...)):
    print("captured_image")
    # تهيئة الكلاسات
    embedding_storage = EmbeddingStorage()
    embedding_generator = EmbeddingGenerator()
    fiass_embedding_search = FiassEmbeddingSearch(embedding_storage)
    try:
        print('caputred_image_data ss')
        search_image_data = np.frombuffer(await captured_image.read(), np.uint8)
        search_image_array = cv2.imdecode(search_image_data,cv2.IMREAD_COLOR)

        # print("search_image_array",search_image_array)
        if search_image_array is None:
            raise HTTPException(status_code=400, detail="Invalid image file.")

        # حفظ الصورة مؤقتًا لتوليد الـ embedding
        temp_image_path = "temp_search_image.jpg"
        cv2.imwrite(temp_image_path, search_image_array)
        # print("temp_image_path",temp_image_path)

        # توليد الـ embedding للصورة الملتقطة
        captured_embedding = embedding_generator.generate_embedding(temp_image_path)
        # print('captured_embedding',captured_embedding)
        os.remove(temp_image_path)

        if not captured_embedding:
            return JSONResponse(
                content={"status": "error", "message":"Failed to generate embedding."},
                status_code=500,
            )
        
        # print("captured_embedding",captured_embedding)
        # تحميل جميع الـ embeddings إلى Fiass
        fiass_embedding_search.load_embeddings()
        
        print("captured_embedding")
        # البحث عن أقرب Embedding
        search_results = fiass_embedding_search.search(captured_embedding, top_k=10)
        print("search_results", search_results)

        if not search_results:
            return JSONResponse(
                content={"status":"error", "message":"No matching embedding found."},
                status_code=404,
            )

        # إعداد النتيجة النهائية
        print(search_results[0][0])
        
        retult = {
            "status": "success",
            "data": [
                {
                    "registration_number": entry[0],
                    "distance": float(entry[1])
                } for entry in search_results
            ]
        }
        print('hello')

        return Response(content=json.dumps(retult), media_type="application/json", status_code=200)

    except Exception as e:
        return JSONResponse(
            content={"status":"error", "message":str(e)},
            status_code=500,
        )

@router.post('/detect_face')
async def detect_face(image: UploadFile = File(...)):
    try:
        # قراءة بيانات الصورة
        # print('image', image)
        image_data = await image.read()
        search_image = np.frombuffer(image_data, np.uint8)
        search_image_array = cv2.imdecode(search_image, cv2.IMREAD_COLOR)

        if search_image_array is None:
            raise HTTPException(status_code=400, detail="Invalid image file.")
        # print("search_image_array", search_image_array)
        # تهيئة الكلاسات (الكشف عن الهوية)
        embedding_storage = EmbeddingStorage()
        embedding_generator = EmbeddingGenerator()
        fiass_embedding_search = FiassEmbeddingSearch(embedding_storage)

        # حفظ الصورة مؤقتًا لتوليد الـ embedding
        temp_image_path = "temp_search_image.jpg"
        cv2.imwrite(temp_image_path, search_image_array)

        # توليد الـ embedding للصورة
        captured_embedding = embedding_generator.generate_embedding(temp_image_path)
        os.remove(temp_image_path)

        if not captured_embedding:
            return JSONResponse(
                content={"status": "error", "message": "Failed to generate embedding."},
                status_code=500,
            )

        # تحميل جميع الـ embeddings إلى Fiass
        fiass_embedding_search.load_embeddings()

        # البحث عن أقرب Embedding
        search_results = fiass_embedding_search.search(captured_embedding, top_k=1)

        if not search_results:
            return JSONResponse(
                content={"status": "error", "message": "No matching embedding found."},
                status_code=404,
            )

        # الحصول على بيانات الشخص
        person_data = search_results[0]
        name = person_data[0]  # اسم الشخص

        # تحديد نقاط الوجه
        face_coordinates = detect_face_coordinates(search_image_array)

        # إضافة النصوص والنقاط إلى الصورة
        image_with_annotations = annotate_image(search_image_array, face_coordinates, name)

        # تحويل الصورة المعدلة إلى Base64
        _, buffer = cv2.imencode('.jpg', image_with_annotations)
        image_bytes = buffer.tobytes()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        # print("image_base64",image_base64)
        return JSONResponse(
            content={
                "status": "success",
                "name": name,
                "points": face_coordinates,
                "image": f"data:image/jpeg;base64,{image_base64}",
            },
            status_code=200,
        )

    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500,
        )


def detect_face_coordinates(image):

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    coordinates = [{"x": int(x), "y": int(y), "w": int(w), "h": int(h)} for (x, y, w, h) in faces]
    return coordinates


def annotate_image(image, face_coordinates, name):
    annotated_image = image.copy()
    for face in face_coordinates:
        x, y, w, h = face["x"], face["y"], face["w"], face["h"]
        # رسم مستطيل حول الوجه
        cv2.rectangle(annotated_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # إضافة الاسم فوق الوجه
        cv2.putText(annotated_image, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return annotated_image