from app.db import get_connection
class MemberRepository:
    @staticmethod
    def find_by_uid(uid:str):
        conn=get_connection()
        try:
            with conn.cursor() as cursor:
                sql="select * from members where uid=%s and active=1"
                cursor.execute(sql,(uid,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def find_by_id(member_id:int):
        conn=get_connection()
        try:
            with conn.cursor() as cursor:
                sql="select * from members where id=%s"
                cursor.execute(sql,(member_id,))
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def create_member(uid, password, name, role='user'):
        conn=get_connection()
        try:
            with conn.cursor() as cursor:
                sql="insert into members (uid,password,name,role) values (%s,%s,%s,%s)"
                cursor.execute(sql,(uid,password,name,role))
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()