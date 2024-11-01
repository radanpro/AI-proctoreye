import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import threading
import face_recognition
import mysql
from database.database_manager import DatabaseManager
from services.image_comparer import ImageComparer

class ComparisonInterface:
    def __init__(self, root, show_main_callback):
        self.root = root
        self.show_main_callback = show_main_callback
        self.frame = tk.Frame(self.root)
        
        # Camera Variables
        self.cap = None
        self.video_thread = None
        self.is_camera_open = False

        # Create two frames for layout
        self.left_frame = tk.Frame(self.frame, bg="lightgray", width=400)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = tk.Frame(self.frame, bg="white", width=400)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.image_label = tk.Label(self.left_frame, bg="black")
        self.image_label.pack(padx=10, pady=10)

        tk.Label(self.right_frame, text="Enter student registration_number").pack(pady=10)
        self.registration_number = tk.Entry(self.right_frame)
        self.registration_number.pack(pady=5)

        tk.Button(self.right_frame, text="Open Camera", command=self.start_camera).pack(pady=5)
        tk.Button(self.right_frame, text="Capture Image", command=self.capture_image).pack(pady=5)
        tk.Button(self.right_frame, text="Compare Image", command=self.compare_images).pack(pady=5)
        tk.Button(self.right_frame, text="Back", command=self.show_main_callback).pack(pady=10)

        self.captured_image = None

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()
        self.stop_camera()

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.is_camera_open = True
        self.video_thread = threading.Thread(target=self.update_video)
        self.video_thread.start()

    def stop_camera(self):
        if self.cap is not None:
            self.is_camera_open = False
            self.cap.release()
            self.cap = None
            self.image_label.config(image='')

    def update_video(self):
        while self.is_camera_open:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.image_label.configure(image=imgtk)
                self.image_label.image = imgtk
            else:
                break

    def capture_image(self):
        if self.cap is not None and self.is_camera_open:
            ret, frame = self.cap.read()
            if ret:
                self.captured_image = frame
                self.stop_camera()
                img = Image.fromarray(cv2.cvtColor(self.captured_image, cv2.COLOR_BGR2RGB))
                imgtk = ImageTk.PhotoImage(image=img)
                self.image_label.configure(image=imgtk)
                self.image_label.image = imgtk
            else:
                messagebox.showerror("Error", "Failed to capture image")

    def compare_images(self):
        student_id = self.registration_number.get()
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter a student ID.")
            return

        db_manager = DatabaseManager()
        connection = db_manager.connect()
        if connection is not None:
            cursor = connection.cursor()
            try:
                cursor.execute("SELECT image_path FROM students WHERE student_id = %s", (student_id,))
                result = cursor.fetchone()
                if result:
                    image_path = result[0]

                    if self.captured_image is not None:
                        rgb_image = cv2.cvtColor(self.captured_image, cv2.COLOR_BGR2RGB)
                        face_locations = face_recognition.face_locations(rgb_image)
                        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

                        if face_encodings:
                            captured_encoding = face_encodings[0]
                            stored_encoding = ImageComparer.image_to_vector(image_path)

                            similarity_percentage = ImageComparer.compare_vectors(stored_encoding, captured_encoding)

                            if similarity_percentage > 60:  # مثال على العتبة، يمكنك تعديلها حسب الحاجة
                                messagebox.showinfo("Match Result", f"The captured image matches the stored student image with {similarity_percentage:.2f}% similarity.")
                            else:
                                messagebox.showinfo("Match Result", f"The captured image does not match the stored student image. Similarity: {similarity_percentage:.2f}%.")
                        else:
                            messagebox.showerror("Error", "No faces detected in the captured image.")
                    else:
                        messagebox.showerror("Error", "No image captured for comparison.")
                else:
                    messagebox.showerror("Error", "Student not found in the database.")
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"An error occurred: {err}")
            finally:
                cursor.close()
                db_manager.close()
        else:
            messagebox.showerror("Error", "Failed to connect to the database.")
