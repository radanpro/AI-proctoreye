import psycopg2
from psycopg2.extras import RealDictCursor

class PostgerDepartment:
    table_name = 'departments'

    def __init__(self, db_name="postgres"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS departments (
            department_id SERIAL PRIMARY KEY,
            department_name VARCHAR(255) NOT NULL,
            college_id INT REFERENCES colleges(college_id)
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
        query = f"INSERT INTO {self.table_name} (department_name, college_id) VALUES (%s, %s)"
        self.execute_query(query, (kwargs['department_name'], kwargs['college_id']))

    def all(self):
        query = f"SELECT * FROM {self.table_name}"
        return self.execute_read_query(query)

    def execute_read_query(self, query, params=()):
        connection = psycopg2.connect(dbname=self.db_name)
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, params)
        result = cursor.fetchall()
        connection.close()
        return result
