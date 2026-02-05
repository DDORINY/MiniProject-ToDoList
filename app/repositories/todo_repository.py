from app.db import get_connection
class TodoRepository:
    @staticmethod
    def list_by_member(member_id:int):
        # 이 사용자(member_id)의 todo 목록을 가져온다
        conn=get_connection()
        try:
            with conn.cursor() as cursor:
                sql="select * from todos where member_id = %s and active = 1 ORDER BY created_at DESC"
                cursor.execute(sql,(member_id,))
                return cursor.fetchall()
        finally:
            conn.close()


    @staticmethod
    def create(member_id:int,title:str,memo=None,due_date=None):
        # 새로운 일정(할일) 생성
        conn=get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO todos (member_id, title, memo, due_date) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql,(member_id,title,memo,due_date))
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()

    @staticmethod
    def toggle_done(todo_id: int, member_id: int):
        # 토완료 ↔ 미완료 상태 뒤집기
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE todos SET is_done = NOT is_done WHERE id = %s AND member_id = %s AND active = 1"
                cursor.execute(sql, (todo_id, member_id))
                conn.commit()
                return cursor.rowcount
        finally:
            conn.close()




    @staticmethod
    def update(todo_id: int, member_id: int, title: str, memo=None, due_date=None):
        # 일정 수정
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """UPDATE todos 
                SET title = %s,
                 memo = %s,
                 due_date = %s
                 WHERE id = %s 
                 AND member_id = %s 
                 AND active = 1"""
                cursor.execute(sql, (title,memo,due_date,todo_id, member_id))
                conn.commit()
                return cursor.rowcount
        finally:
            conn.close()

    @staticmethod
    def soft_delete(todo_id:int,member_id:int):
        # 진짜 삭제가 아니라 “숨김 처리”
        conn=get_connection()
        try:
            with conn.cursor() as cursor:
                sql="UPDATE todos SET active = 0 WHERE id =%s AND member_id =%s AND active = 1 "
                cursor.execute(sql,(todo_id,member_id))
                conn.commit()
                return cursor.rowcount
        finally:
            conn.close()

    @staticmethod
    def get_by_id(todo_id:int,member_id:int):
        # 수정화면용
        conn=get_connection()
        try:
            with conn.cursor() as cursor:
                sql ="SELECT * FROM todos WHERE id = %s AND member_id = %s AND active =1 "
                cursor.execute(sql,(todo_id,member_id))
                return cursor.fetchone()
        finally:
            conn.close()