from database.db_connection import DatabaseConnection


class AdminModel:
    """Handles all database operations related to Admin."""

    def __init__(self):
        self.db = DatabaseConnection()

    def register_admin(self, name, username, password, email_id, contact):
        """Inserts a new admin record into the database."""
        query = """
            INSERT INTO admin (name, username, password, email_id, contact)
            VALUES (%s, %s, %s, %s, %s)
        """
        success, admin_id = self.db.execute_query(
            query, (name, username, password, email_id, contact)
        )
        return success, admin_id

    def login_admin(self, username, password):
        """Checks username and password. Returns admin record if valid."""
        query = "SELECT * FROM admin WHERE username=%s AND password=%s"
        return self.db.fetch_one(query, (username, password))

    def get_admin_by_username(self, username):
        """Fetches admin record by username."""
        query = "SELECT * FROM admin WHERE username=%s"
        return self.db.fetch_one(query, (username,))

    def validate_forgot_password(self, username, email_id_or_contact):
        """Validates admin by username and email_id or contact."""
        query = """
            SELECT * FROM admin
            WHERE username=%s AND (email_id=%s OR contact=%s)
        """
        return self.db.fetch_one(query, (username, email_id_or_contact, email_id_or_contact))

    def update_password_by_username(self, username, new_password):
        """Updates admin password using username."""
        query = "UPDATE admin SET password=%s WHERE username=%s"
        success, _ = self.db.execute_query(query, (new_password, username))
        return success

    def change_password(self, admin_id, username, old_password, new_password):
        """Changes admin password after verifying old password."""
        check = self.db.fetch_one(
            "SELECT * FROM admin WHERE admin_id=%s AND username=%s AND password=%s",
            (admin_id, username, old_password)
        )
        if check:
            query = "UPDATE admin SET password=%s WHERE admin_id=%s"
            success, _ = self.db.execute_query(query, (new_password, admin_id))
            return success
        return False

    def username_exists(self, username):
        """Returns True if username already exists."""
        result = self.db.fetch_one(
            "SELECT admin_id FROM admin WHERE username=%s", (username,)
        )
        return result is not None

    def email_id_exists(self, email_id):
        """Returns True if email_id already exists."""
        result = self.db.fetch_one(
            "SELECT admin_id FROM admin WHERE email_id=%s", (email_id,)
        )
        return result is not None

    def contact_exists(self, contact):
        """Returns True if contact already exists."""
        result = self.db.fetch_one(
            "SELECT admin_id FROM admin WHERE contact=%s", (contact,)
        )
        return result is not None
