# database/db_connection.py

import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    """
    This class handles the MySQL database connection.
    It is used by all model files to connect to the database.
    """

    def __init__(self):
        self.host     = "localhost"
        self.user     = "root"        
        self.password = "DB_PASSWORD"
        self.database = "DB_NAME"
        self.connection = None

    def connect(self):
        """Opens a connection to the MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host     = self.host,
                user     = self.user,
                password = self.password,
                database = self.database
            )
            return self.connection
        except Error as e:
            print(f"Database Connection Error: {e}")
            return None

    def get_cursor(self):
        """Returns a cursor object to execute SQL queries."""
        if self.connection and self.connection.is_connected():
            return self.connection.cursor(dictionary=True)
        return None

    def commit(self):
        """Saves (commits) the changes to the database."""
        if self.connection:
            self.connection.commit()

    def close(self):
        """Closes the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query, params=None):
        """
        Executes INSERT / UPDATE / DELETE queries.
        Returns True if successful, False if not.
        """
        try:
            conn   = self.connect()
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            last_id = cursor.lastrowid
            cursor.close()
            self.close()
            return True, last_id
        except Error as e:
            print(f"Query Error: {e}")
            return False, None

    def fetch_one(self, query, params=None):
        """
        Executes a SELECT query and returns ONE row as a dictionary.
        """
        try:
            conn   = self.connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            cursor.close()
            self.close()
            return result
        except Error as e:
            print(f"Fetch One Error: {e}")
            return None

    def fetch_all(self, query, params=None):
        """
        Executes a SELECT query and returns ALL rows as a list of dictionaries.
        """
        try:
            conn   = self.connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            self.close()
            return result
        except Error as e:
            print(f"Fetch All Error: {e}")
            return []