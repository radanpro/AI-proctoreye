import os
import cv2
import face_recognition
import numpy as np
## FastAPI
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
## files
from database.database_manager import DatabaseManager
from services.student_data_handler import StudentDataHandler
from services.image_vectorizer import ImageVectorizer
from services.image_comparer import ImageComparer 
# routes
from routes.compare_image import router as compare_image_router
from routes.students import router as students_router


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

# إضافة المسار (router) الخاص بالمقارنة
app.include_router(compare_image_router, prefix="/api", tags=["compare_image"])

# إضافة المسار (router) الخاص بالطلاب
app.include_router(students_router, prefix="/api", tags=["students"])


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


@app.get("/")
async def home():
    return "Welcome to the Home Page!"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
