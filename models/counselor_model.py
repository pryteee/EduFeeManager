from database.db_connection import DatabaseConnection


class CounselorModel:
    """Handles all database operations related to Counselor."""

    def __init__(self):
        self.db = DatabaseConnection()

    def register_counselor(self, name, email, contact, username, password):
        query = """
            INSERT INTO counselor (name, email, contact, username, password)
            VALUES (%s, %s, %s, %s, %s)
        """
        success, counselor_id = self.db.execute_query(
            query, (name, email, contact, username, password)
        )
        return success, counselor_id

    def login_counselor(self, username, password):
        query = "SELECT * FROM counselor WHERE username=%s AND password=%s"
        return self.db.fetch_one(query, (username, password))

    def get_counselor_by_id(self, counselor_id):
        query = "SELECT * FROM counselor WHERE counselor_id=%s"
        return self.db.fetch_one(query, (counselor_id,))

    def get_all_counselors(self):
        query = "SELECT * FROM counselor ORDER BY counselor_id"
        return self.db.fetch_all(query)

    def update_counselor(self, counselor_id, name, email, contact, username, password):
        query = """
            UPDATE counselor
            SET name=%s, email=%s, contact=%s, username=%s, password=%s
            WHERE counselor_id=%s
        """
        success, _ = self.db.execute_query(
            query, (name, email, contact, username, password, counselor_id)
        )
        return success

    def delete_counselor(self, counselor_id):
        query = "DELETE FROM counselor WHERE counselor_id=%s"
        success, _ = self.db.execute_query(query, (counselor_id,))
        return success

    def validate_forgot_password(self, username, email_or_contact):
        query = """
            SELECT * FROM counselor
            WHERE username=%s AND (email=%s OR contact=%s)
        """
        return self.db.fetch_one(query, (username, email_or_contact, email_or_contact))

    def update_password_by_username(self, username, new_password):
        query = "UPDATE counselor SET password=%s WHERE username=%s"
        success, _ = self.db.execute_query(query, (new_password, username))
        return success

    def change_password(self, counselor_id, username, old_password, new_password):
        check = self.db.fetch_one(
            "SELECT * FROM counselor WHERE counselor_id=%s AND username=%s AND password=%s",
            (counselor_id, username, old_password)
        )
        if check:
            query = "UPDATE counselor SET password=%s WHERE counselor_id=%s"
            success, _ = self.db.execute_query(query, (new_password, counselor_id))
            return success
        return False

    def username_exists(self, username):
        result = self.db.fetch_one(
            "SELECT counselor_id FROM counselor WHERE username=%s", (username,)
        )
        return result is not None

    def email_exists(self, email):
        result = self.db.fetch_one(
            "SELECT counselor_id FROM counselor WHERE email=%s", (email,)
        )
        return result is not None

    def contact_exists(self, contact):
        result = self.db.fetch_one(
            "SELECT counselor_id FROM counselor WHERE contact=%s", (contact,)
        )
        return result is not None
