import mysql.connector

class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def __init__(self, host='localhost', user='root', password='', database='exam_proctoring'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        if self._connection is None or not self._connection.is_connected():
            try:
                self._connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password
                )
                self._create_database_if_not_exists()
                self._connection.database = self.database
                self._create_table_if_not_exists()
                print("Database connection successful")
            except mysql.connector.Error as err:
                print(f"Database connection error: {err}")
                self._connection = None
        return self._connection

    def _create_database_if_not_exists(self):
        cursor = self._connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        cursor.close()

    def _create_table_if_not_exists(self):
        cursor = self._connection.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS students (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                registration_number VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                image_path VARCHAR(255),
                face_embedding BLOB
            )
        """)
        cursor.close()

    def close(self):
        if self._connection is not None and self._connection.is_connected():
            self._connection.close()
            self._connection = None
            print("Database connection closed")
