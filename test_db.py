import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    """
    Singleton-style DB connector.
    Call DatabaseConnection.get_connection() anywhere to get a live MySQL connection.
    """

    
    HOST = "localhost"
    USER = "root"         
    PASSWORD = ""         
    DATABASE = "fee_management"

    @staticmethod
    def get_connection():
        """Returns a fresh MySQL connection object."""
        try:
            connection = mysql.connector.connect(
                host=DatabaseConnection.HOST,
                user=DatabaseConnection.USER,
                password=DatabaseConnection.PASSWORD,
                database=DatabaseConnection.DATABASE
            )
            return connection
        except Error as e:
            print(f"[DB ERROR] Could not connect to MySQL: {e}")
            return None