import os
import cv2
import numpy as np
from fastapi import APIRouter, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from services.student_data_handler import StudentDataHandler
from database.database_manager import DatabaseManager

# إعداد الاتصال بقاعدة البيانات
db_manager = DatabaseManager(host="localhost", user="root", password="", database="exam_proctoring")

router = APIRouter()

@router.post("/add_student")
async def add_student(name: str = Form(...), registration_number: str = Form(...), image_array: UploadFile = File(...)):
    try:
        print(f"Received data: name={name}, registration_number={registration_number}, image_array={image_array.filename}")
        
        # قراءة البيانات من الملف وتحويلها إلى numpy array
        image_array_data = np.frombuffer(await image_array.read(), np.uint8)
        image = cv2.imdecode(image_array_data, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file. Unable to process the uploaded file.")

        # حفظ الصورة في مجلد images
        image_extension = os.path.splitext(image_array.filename)[1]
        image_path = f"images/{registration_number}{image_extension}"
        cv2.imwrite(image_path, image)
        
        # إنشاء بيانات الطالب
        student_data = {
            'registration_number': registration_number,
            'name': name,
            'image_path': image_path,
            'image_array': image_path,
        }
        
        # إنشاء كائن من StudentDataHandler
        student_data_handler = StudentDataHandler()

        # التحقق من وجود الرقم المسجل في قاعدة البيانات
        try:
            student_data['student_id'] = student_data_handler.generate_student_id()
            if student_data_handler.is_registration_number_exists(registration_number):
                raise HTTPException(status_code=400, detail="Student with this registration number already exists.")
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # حفظ بيانات الطالب في قاعدة البيانات
        result = student_data_handler.save_student(student_data)
        if not result:
            raise HTTPException(status_code=500, detail="Failed to save student data to the database.")

        return JSONResponse(content={"status": "success", "message": "Student added successfully"}, status_code=201)
    
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@router.get("/students")
async def get_students():
    connection = db_manager.connect()
    if not connection.is_connected():
        raise HTTPException(status_code=500, detail="MySQL Connection not available")
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT registration_number, name, image_path FROM students")
    students = cursor.fetchall()
    cursor.close()
    db_manager.close()
    
    # تعديل المسار لإضافة رابط الصورة الكامل
    for student in students:
        student['image_url'] = f"http://127.0.0.1:8000/{student['image_path']}"
    
    return JSONResponse(content=students, status_code=200)
