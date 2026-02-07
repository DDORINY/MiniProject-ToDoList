from app.repositories.member_repository import MemberRepository
class AuthService:
    @staticmethod
    def login(uid:str,pw:str)->dict:
        uid = uid.strip()
        row = MemberRepository.find_by_uid(uid)

        if not row:
            raise ValueError ("아이디가 맞지 않습니다.")

        if not bool (row.get("active",True)):
            raise ValueError ("비활성화 계정입니다.")

        if row.get("password") != pw:
            raise ValueError("비밀번호가 맞지 않습니다.")

        return row