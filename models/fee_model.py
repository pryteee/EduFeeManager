from database.db_connection import DatabaseConnection


class FeeModel:
    """Handles all database operations related to Fee."""

    def __init__(self):
        self.db = DatabaseConnection()

    def create_fee_record(self, student_id, course_fee):
        """
        Called when a student is added by counselor.
        Checks if fee record already exists to avoid duplicate.
        """
        existing = self.db.fetch_one(
            "SELECT fee_id FROM fee WHERE student_id=%s",
            (student_id,)
        )

        if existing:
            pending = course_fee
            query = """
                UPDATE fee
                SET course_fee=%s, pending_amount=%s,
                    status='Pending'
                WHERE student_id=%s
            """
            success, _ = self.db.execute_query(
                query, (course_fee, pending, student_id)
            )
            return success, existing['fee_id']
        else:
            # New record
            pending = course_fee
            query = """
                INSERT INTO fee
                (student_id, course_fee, paid_amount,
                 pending_amount, status)
                VALUES (%s, %s, 0.00, %s, 'Pending')
            """
            success, fee_id = self.db.execute_query(
                query, (student_id, course_fee, pending)
            )
            return success, fee_id

    def get_fee_by_student_id(self, student_id):
        """Fetches fee record for a specific student."""
        query = "SELECT * FROM fee WHERE student_id=%s"
        return self.db.fetch_one(query, (student_id,))

    def update_fee(self, student_id, course_fee,
                   paid_amount, pending_amount, status):
        """Updates fee record."""
        query = """
            UPDATE fee
            SET course_fee=%s, paid_amount=%s,
                pending_amount=%s, status=%s
            WHERE student_id=%s
        """
        success, _ = self.db.execute_query(
            query,
            (course_fee, paid_amount, pending_amount,
             status, student_id)
        )
        return success

    def calculate_status(self, paid_amount, pending_amount):
        """Business rule: determines fee status."""
        paid    = float(paid_amount)
        pending = float(pending_amount)
        if pending == 0:
            return "Fully Paid"
        elif paid > 0 and pending > 0:
            return "Partial Paid"
        else:
            return "Pending"

    def get_fee_with_student(self, student_id):
        """
        Joins student and fee table to show full details.
        Uses LEFT JOIN so student shows even if fee row
        has missing data.
        """
        query = """
            SELECT
                s.student_id,
                s.name,
                s.course,
                s.academic_year,
                COALESCE(f.course_fee,     0.00) AS course_fee,
                COALESCE(f.paid_amount,    0.00) AS paid_amount,
                COALESCE(f.pending_amount, 0.00) AS pending_amount,
                COALESCE(f.status, 'Pending')    AS status
            FROM student s
            LEFT JOIN fee f ON s.student_id = f.student_id
            WHERE s.student_id = %s
        """
        return self.db.fetch_one(query, (student_id,))
    def get_all_students_fee_report(self):
        """
        Returns all students with their complete fee details.
        Used for detailed report view.
        """
        query = """
            SELECT
                s.student_id,
                s.name,
                s.course,
                s.academic_year,
                COALESCE(f.course_fee,     0.00) AS course_fee,
                COALESCE(f.paid_amount,    0.00) AS paid_amount,
                COALESCE(f.pending_amount, 0.00) AS pending_amount,
                COALESCE(f.status,      'Pending') AS status
            FROM student s
            LEFT JOIN fee f ON s.student_id = f.student_id
            ORDER BY
                CASE f.status
                    WHEN 'Pending'      THEN 1
                    WHEN 'Partial Paid' THEN 2
                    WHEN 'Fully Paid'   THEN 3
                    ELSE 4
                END,
                s.student_id
        """
        return self.db.fetch_all(query)

    def get_reports(self):
        """
        Returns summary report data using SQL aggregates.

        FIX EXPLANATION:
        ─────────────────────────────────────────────────
        Before: SUM(f.pending_amount)
        Problem: pending_amount stored in fee table is wrong
                 for self-registered students because it was
                 set to 0.00 at registration time.

        After: SUM(f.course_fee - f.paid_amount)
        Reason: Always calculate pending as course_fee minus
                paid_amount at query time — this is always
                accurate regardless of what is stored in
                pending_amount column.

        Also: total_collection = SUM of paid_amount only
              from students who actually HAVE a fee record
              with course_fee > 0 (ignores blank registrations)

        total_pending = SUM(course_fee - paid_amount)
                        only for non-fully-paid students
        ─────────────────────────────────────────────────
        """
        query = """
            SELECT
                COUNT(s.student_id) AS total_students,

                SUM(
                    CASE WHEN f.status = 'Fully Paid'
                    THEN 1 ELSE 0 END
                ) AS fully_paid,

                SUM(
                    CASE WHEN f.status = 'Partial Paid'
                    THEN 1 ELSE 0 END
                ) AS partial_paid,

                SUM(
                    CASE
                        WHEN f.status = 'Pending'
                        OR   f.status IS NULL
                        THEN 1 ELSE 0
                    END
                ) AS pending,

                COALESCE(
                    SUM(f.paid_amount), 0
                ) AS total_collection,

                COALESCE(
                    SUM(
                        CASE
                            WHEN f.course_fee > 0
                            THEN f.course_fee - f.paid_amount
                            ELSE 0
                        END
                    ), 0
                ) AS total_pending

            FROM student s
            LEFT JOIN fee f ON s.student_id = f.student_id
        """
        return self.db.fetch_one(query)
