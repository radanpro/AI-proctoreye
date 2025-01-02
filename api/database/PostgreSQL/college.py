import psycopg2
from psycopg2.extras import RealDictCursor

class PostgerCollege:
    table_name = 'colleges'

    def __init__(self, db_name="postgres"):
        self.db_name = db_name
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS colleges (
            college_id SERIAL PRIMARY KEY,
            college_name VARCHAR(255) NOT NULL
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
        query = f"INSERT INTO {self.table_name} (college_name) VALUES (%s)"
        self.execute_query(query, (kwargs['college_name'],))

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
