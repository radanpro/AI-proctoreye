# frontend/utils/database.py

import mysql.connector

class DatabaseConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DatabaseConnection, cls).__new__(cls, *args, **kwargs)
            cls._instance._connection = None
        return cls._instance

    def connect(self, host='localhost', user='root', password='', database='exam_proctoring'):
        if self._connection is None:
            self._connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        return self._connection

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None
