import psycopg2
from psycopg2.extras import RealDictCursor

class PostgerStudent:
    table_name = 'students'

    def __init__(self, db_name="postgres"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS students (
            student_id SERIAL PRIMARY KEY,
            student_enrollment_number VARCHAR(100) UNIQUE NOT NULL,
            department_id INT REFERENCES departments(department_id),
            embedding FLOAT8[]
        )
        """
        self.execute_query(query)

    def execute_query(self, query, params=()):
        connection = psycopg2.connect(dbname=self.db_name)
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        connection.close()

    def create(self, **kwargs):
        query = f"INSERT INTO {self.table_name} (student_enrollment_number, department_id, embedding) VALUES (%s, %s, %s)"
        self.execute_query(query, (kwargs['student_enrollment_number'], kwargs['department_id'], kwargs['embedding']))

    def all(self):
        query = f"SELECT * FROM {self.table_name}"
        return self.execute_read_query(query)

    def first(self, **filters):
        result = self.all(**filters)
        return result[0] if result else None

    def last(self, **filters):
        result = self.all(**filters)
        return result[-1] if result else None

    def find(self, **kwargs):
        query = f"SELECT * FROM {self.table_name}"
        if kwargs:
            conditions = ' AND '.join([f"{key} = %s" for key in kwargs])
            query += f" WHERE {conditions}"
            return self.execute_read_query(query, tuple(kwargs.values()))
        return None

    def update(self, identifier, **kwargs):
        set_clause = ', '.join([f"{key} = %s" for key in kwargs])
        query = f"UPDATE {self.table_name} SET {set_clause} WHERE student_id = %s"
        self.execute_query(query, tuple(kwargs.values()) + (identifier,))

    def delete(self, **kwargs):
        query = f"DELETE FROM {self.table_name} WHERE "
        conditions = ' AND '.join([f"{key} = %s" for key in kwargs])
        query += conditions
        self.execute_query(query, tuple(kwargs.values()))

    def exists(self, **kwargs):
        query = f"SELECT COUNT(*) FROM {self.table_name} WHERE "
        conditions = ' AND '.join([f"{key} = %s" for key in kwargs])
        query += conditions
        result = self.execute_read_query(query, tuple(kwargs.values()))
        return result[0][0] > 0

    def execute_read_query(self, query, params=()):
        connection = psycopg2.connect(dbname=self.db_name)
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, params)
        result = cursor.fetchall()
        connection.close()
        return result
