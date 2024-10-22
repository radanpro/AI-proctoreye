from flask import Flask, request, redirect, url_for, flash, render_template, send_from_directory
import os
from utils.database import DatabaseConnection
from flask import jsonify
import uuid


app = Flask(__name__, static_folder='.')
app.secret_key = 'your_secret_key'  # Required for flash messages

# Database connection
db_connection = DatabaseConnection().connect()

# Serve index.html
@app.route('/')
def serve_index():
    return render_template('index.html')

# Serve new_student.html
@app.route('/new_student', methods=['GET', 'POST'])
def serve_new_student():
    if request.method == 'POST':
        name = request.form['name']
        image = request.files['image']

        # Create the images folder if it doesn't exist
        image_folder = 'images'
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)

        # Save the image
        image_path = os.path.join(image_folder, image.filename)
        image.save(image_path)

        # Insert the student into the database
        try:
            cursor = db_connection.cursor()
            cursor.execute("INSERT INTO students (name, image_path) VALUES (%s, %s)", (name, image_path))
            db_connection.commit()
            cursor.close()

            # Flash success message and redirect to home
            flash('تم إضافة الطالب بنجاح!', 'success')
            return redirect(url_for('serve_index'))
        except Exception as e:
            flash(f'خطأ في إضافة الطالب: {str(e)}', 'danger')
            return redirect(url_for('serve_new_student'))

    return render_template('new_student.html')

# Serve static files (e.g., JS and CSS)
@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('.', path)

# Display students
@app.route('/students')
def students():
    try:
        cursor = db_connection.cursor()
        cursor.execute("SELECT name, image_path FROM students")
        student_list = [{"name": row[0], "image": row[1]} for row in cursor.fetchall()]
        cursor.close()
        return render_template('students.html', students=student_list)
    except Exception as e:
        flash(f'خطأ في جلب الطلاب: {str(e)}', 'danger')
        return render_template('students.html', students=[])

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    image = request.files['image']

    # Create the images folder if it doesn't exist
    image_folder = 'frontend/images/'
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # Generate a unique filename
    unique_filename = f"{uuid.uuid4().hex}_{image.filename}"  # Generates a unique ID and appends the original filename

    # Save the image with the new unique filename
    image_path = os.path.join(image_folder, unique_filename)
    image.save(image_path)

    # Insert the student into the database
    try:
        cursor = db_connection.cursor()
        cursor.execute("INSERT INTO students (name, image_path) VALUES (%s, %s)", (name, unique_filename))  # Store the unique filename
        db_connection.commit()
        cursor.close()

        # Flash success message and redirect to home
        flash('Student added successfully!', 'success')
        return redirect(url_for('serve_index'))
    except Exception as e:
        flash(f'Error adding student: {str(e)}', 'danger')
        return redirect(url_for('serve_new_student'))

@app.route('/list_images')
def list_images():
    images = os.listdir('images')
    return jsonify(images)  # إرجاع قائمة بجميع الصور


@app.route('/images/<path:filename>')
def serve_image(filename):
    print(f"Serving image: {filename}")  # طباعة اسم الملف
    try:
        return send_from_directory('images', filename)
    except Exception as e:
        print(f"Error serving image: {str(e)}")
        return "Error serving image", 500
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
