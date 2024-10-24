import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import threading
from database.database_manager import DatabaseManager

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

        # Setup left frame (for camera feed)
        self.image_label = tk.Label(self.left_frame, bg="black")
        self.image_label.pack(padx=10, pady=10)

        tk.Label(self.right_frame, text="Enter Student ID").pack(pady=10)
        self.student_id_entry = tk.Entry(self.right_frame)
        self.student_id_entry.pack(pady=5)

        tk.Button(self.right_frame, text="Open Camera", command=self.start_camera).pack(pady=5)
        tk.Button(self.right_frame, text="Capture Image", command=self.capture_image).pack(pady=5)
        tk.Button(self.right_frame, text="Fetch Data", command=self.fetch_student_data).pack(pady=5)  # Renamed to fetch data
        tk.Button(self.right_frame, text="Back", command=self.show_main_callback).pack(pady=10)

        self.captured_image = None

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()
        self.stop_camera()  # Stop the camera when hiding the interface

    def start_camera(self):
        # Open camera and start video streaming
        self.cap = cv2.VideoCapture(0)
        self.is_camera_open = True
        self.video_thread = threading.Thread(target=self.update_video)
        self.video_thread.start()

    def stop_camera(self):
        # Stop the camera and close the video stream
        if self.cap is not None:
            self.is_camera_open = False
            self.cap.release()
            self.cap = None
            self.image_label.config(image='')

    def update_video(self):
        while self.is_camera_open:
            ret, frame = self.cap.read()
            if ret:
                # Convert frame to RGB
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
                self.captured_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.stop_camera()
                img = Image.fromarray(self.captured_image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.image_label.configure(image=imgtk)
                self.image_label.image = imgtk
            else:
                messagebox.showerror("Error", "Failed to capture image")

    def fetch_student_data(self):
        # Check if student ID is entered
        student_id = self.student_id_entry.get()
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter a student ID.")
            return

        # Fetch student data from the database
        db_manager = DatabaseManager()
        connection = db_manager.connect()

        cursor = connection.cursor()
        cursor.execute("SELECT image_path FROM students WHERE student_id = %s", (student_id,))
        result = cursor.fetchone()

        if result:
            # Display the fetched data (you can modify this part as needed)
            stored_image_path = result[0]
            messagebox.showinfo("Data Fetched", f"Image Path: {stored_image_path}")
        else:
            messagebox.showerror("Error", "Student not found in the database.")

        cursor.close()
        db_manager.close()
