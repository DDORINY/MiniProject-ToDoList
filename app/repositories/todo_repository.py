from app.db import get_connection


class TodoRepository:
    @staticmethod
    def count_summary(member_id: int):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                            SELECT
                              COUNT(*) AS total,
                              SUM(CASE WHEN is_done = 0 THEN 1 ELSE 0 END) AS todo,
                              SUM(CASE WHEN is_done = 1 THEN 1 ELSE 0 END) AS done,
                              SUM(CASE WHEN is_done = 0 AND due_date IS NOT NULL AND due_date < CURDATE() THEN 1 ELSE 0 END) AS overdue
                            FROM todos
                            WHERE member_id = %s AND active = 1
                        """
                cursor.execute(sql, (member_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def list_due_today(member_id: int, limit: int = 5):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                            SELECT *
                            FROM todos
                            WHERE member_id = %s
                              AND active = 1
                              AND due_date = CURDATE()
                            ORDER BY is_done ASC, created_at DESC
                            LIMIT %s
                        """
                cursor.execute(sql, (member_id, limit))
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def list_overdue(member_id: int, limit: int = 5):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                            SELECT *
                            FROM todos
                            WHERE member_id = %s
                              AND active = 1
                              AND is_done = 0
                              AND due_date IS NOT NULL
                              AND due_date < CURDATE()
                            ORDER BY due_date ASC, created_at DESC
                            LIMIT %s
                        """
                cursor.execute(sql, (member_id, limit))
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def list_by_member(member_id: int, filter_done: str | None = None, q: str | None = None):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT *
                    FROM todos
                    WHERE member_id = %s
                      AND active = 1
                """
                params = [member_id]

                if filter_done == "done":
                    sql += " AND is_done = 1"
                elif filter_done == "todo":
                    sql += " AND is_done = 0"

                if q:
                    sql += " AND (title LIKE %s OR memo LIKE %s)"
                    like = f"%{q}%"
                    params.extend([like, like])

                sql += """
                    ORDER BY
                      is_done ASC,
                      (due_date IS NULL) ASC,
                      due_date ASC,
                      created_at DESC
                """

                cursor.execute(sql, params)
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def create(member_id: int, title: str, memo=None, due_date=None):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO todos (member_id, title, memo, due_date) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (member_id, title, memo, due_date))
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def toggle_done(todo_id: int, member_id: int):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE todos
                    SET is_done = NOT is_done
                    WHERE id = %s
                      AND member_id = %s
                      AND active = 1
                """
                cursor.execute(sql, (todo_id, member_id))
                conn.commit()
                return cursor.rowcount
        finally:
            conn.close()

    @staticmethod
    def update(todo_id: int, member_id: int, title: str, memo=None, due_date=None):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE todos
                    SET title = %s,
                        memo = %s,
                        due_date = %s
                    WHERE id = %s
                      AND member_id = %s
                      AND active = 1
                """
                cursor.execute(sql, (title, memo, due_date, todo_id, member_id))
                conn.commit()
                return cursor.rowcount
        finally:
            conn.close()

    @staticmethod
    def soft_delete(todo_id: int, member_id: int):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    UPDATE todos
                    SET active = 0
                    WHERE id = %s
                      AND member_id = %s
                      AND active = 1
                """
                cursor.execute(sql, (todo_id, member_id))
                conn.commit()
                return cursor.rowcount
        finally:
            conn.close()

    @staticmethod
    def get_by_id(todo_id: int, member_id: int):
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT *
                    FROM todos
                    WHERE id = %s
                      AND member_id = %s
                      AND active = 1
                """
                cursor.execute(sql, (todo_id, member_id))
                return cursor.fetchone()
        finally:
            conn.close()
