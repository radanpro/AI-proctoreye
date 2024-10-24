import mysql.connector

class DatabaseManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def connect(self, host='localhost', user='root', password='', database='exam_proctoring'):
        if self._connection is None:
            try:
                self._connection = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
                )
                print("Database connection successful")
            except mysql.connector.Error as err:
                print(f"Database connection error: {err}")
                self._connection = None
        return self._connection

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None
            print("Database connection closed")

# Example of using the DatabaseManager class
if __name__ == "__main__":
    db = DatabaseManager()
    connection = db.connect(host='localhost', user='root', password='', database='exam_proctoring')

    # Perform a sample query
    if connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM students")  # مثال على الاستعلام
        results = cursor.fetchall()
        for row in results:
            print(row)
        cursor.close()

    db.close()
