# models/student_model.py

from database.db_connection import DatabaseConnection


class StudentModel:
    """Handles all database operations related to Student."""

    def __init__(self):
        self.db = DatabaseConnection()

    def register_student(
            self,
            name,
            email,
            contact,
            course,
            username,
            password,
            academic_year,
            total_fee=0.00        # defaults to 0.00
    ):
        # ── Step 1: Insert into student table ─────────────
        query = """
            INSERT INTO student
            (
                name,
                email,
                contact,
                course,
                academic_year,
                username,
                password,
                total_fee
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """
        success, student_id = self.db.execute_query(
            query,
            (
                name,
                email,
                contact,
                course,
                academic_year,
                username,
                password,
                total_fee
            )
        )

        # ── Step 2: Auto-create fee record ─────────────────
        # This ensures fee table always has a row for every
        # student — whether registered by student or counselor.
        # Without this, JOIN in get_fee_with_student returns
        # nothing and shows "student not found".
        if success and student_id:
            fee_query = """
                INSERT INTO fee
                (student_id, course_fee, paid_amount,
                 pending_amount, status)
                VALUES (%s, %s, 0.00, %s, 'Pending')
            """
            self.db.execute_query(
                fee_query,
                (student_id, total_fee, total_fee)
            )

        return success, student_id

    def login_student(self, student_id, username, password):
        query = """
            SELECT * FROM student
            WHERE student_id=%s
            AND username=%s
            AND password=%s
        """
        return self.db.fetch_one(query, (student_id, username, password))

    def get_student_by_id(self, student_id):
        query = "SELECT * FROM student WHERE student_id=%s"
        return self.db.fetch_one(query, (student_id,))

    def get_all_students(self):
        query = "SELECT * FROM student ORDER BY student_id"
        return self.db.fetch_all(query)

    def update_student(self, student_id, name, course,
                       contact, email, academic_year):
        query = """
            UPDATE student
            SET name=%s, course=%s, contact=%s,
                email=%s, academic_year=%s
            WHERE student_id=%s
        """
        success, _ = self.db.execute_query(
            query,
            (name, course, contact, email, academic_year, student_id)
        )
        return success

    def delete_student(self, student_id):
        query = "DELETE FROM student WHERE student_id=%s"
        success, _ = self.db.execute_query(query, (student_id,))
        return success

    def validate_forgot_password(self, student_id, email):
        query = """
            SELECT * FROM student
            WHERE student_id=%s AND email=%s
        """
        return self.db.fetch_one(query, (student_id, email))

    def update_password_by_id(self, student_id, new_password):
        query = "UPDATE student SET password=%s WHERE student_id=%s"
        success, _ = self.db.execute_query(
            query, (new_password, student_id)
        )
        return success

    def change_password(self, student_id, old_password, new_password):
        check = self.db.fetch_one(
            "SELECT * FROM student WHERE student_id=%s AND password=%s",
            (student_id, old_password)
        )
        if check:
            query = "UPDATE student SET password=%s WHERE student_id=%s"
            success, _ = self.db.execute_query(
                query, (new_password, student_id)
            )
            return success
        return False

    def username_exists(self, username):
        result = self.db.fetch_one(
            "SELECT student_id FROM student WHERE username=%s",
            (username,)
        )
        return result is not None

    def email_exists(self, email):
        result = self.db.fetch_one(
            "SELECT student_id FROM student WHERE email=%s",
            (email,)
        )
        return result is not None

    def contact_exists(self, contact):
        result = self.db.fetch_one(
            "SELECT student_id FROM student WHERE contact=%s",
            (contact,)
        )
        return result is not None