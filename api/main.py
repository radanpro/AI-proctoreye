import os
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database.database_manager import DatabaseManager
from services.student_data_handler import StudentDataHandler
from services.image_vectorizer import ImageVectorizer
import cv2
import numpy as np

# تأكد من أن مجلد images موجود
if not os.path.exists("images"):
    os.makedirs("images")

app = FastAPI()

# إضافة CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# إعداد مسار ثابت لخدمة الصور
app.mount("/images", StaticFiles(directory="images"), name="images")

# إعداد الاتصال بقاعدة البيانات
db_manager = DatabaseManager(host="localhost", user="root", password="", database="exam_proctoring")

@app.get("/check_db_connection")
async def check_db_connection():
    try:
        connection = db_manager.connect()
        if connection.is_connected():
            db_manager.close()
            return JSONResponse(content={"status": "success", "message": "Connected to database"}, status_code=200)
        else:
            return JSONResponse(content={"status": "error", "message": "Failed to connect to database"}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

@app.post("/add_student")
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
            # إذا كان الرقم المسجل موجودًا مسبقًا
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

@app.get("/students")
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


@app.post("/compare_image")
async def compare_image(registration_number: str = Form(...), captured_image: UploadFile = File(...)):
    comparer = ImageComparer()
    captured_image_data = np.frombuffer(await captured_image.read(), np.uint8)
    captured_image_array = cv2.imdecode(captured_image_data, cv2.IMREAD_COLOR)

    connection = db_manager.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT image_path FROM students WHERE registration_number = %s", (registration_number,))
    result = cursor.fetchone()
    cursor.close()

    if result:
        stored_image_path = result[0]
        stored_encoding = comparer.image_to_vector(stored_image_path)
        face_locations = face_recognition.face_locations(captured_image_array)
        face_encodings = face_recognition.face_encodings(captured_image_array, face_locations)

        if face_encodings:
            captured_encoding = face_encodings[0]
            similarity_percentage = comparer.compare_vectors(stored_encoding, captured_encoding)
            return JSONResponse(content={"status": "success", "similarity": similarity_percentage}, status_code=200)
        else:
            return JSONResponse(content={"status": "error", "message": "No faces detected"}, status_code=400)
    return JSONResponse(content={"status": "error", "message": "Student not found"}, status_code=404)

@app.get("/")
async def home():
    return "Welcome to the Home Page!"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
