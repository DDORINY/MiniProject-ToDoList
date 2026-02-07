from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from app.repositories import MemberRepository
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)


# 로그인
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # 이미 로그인 상태인지 로그인 상태이면  todo 목록으로
    if session.get("member_id"):
        return redirect((url_for("todo.list_page")))

    if request.method == "GET":
        return render_template("auth/login.html")
    # POST → 로그인 시도
    uid = request.form.get("uid", "").strip()
    pw = request.form.get("pw", "")

    try:
        member = AuthService.login(uid, pw)
        session["member_id"] = member["id"]
        session["member_uid"] = member["uid"]
        session["member_name"] = member["name"]

        flash("로그인 성공")
        return redirect(url_for("todo.list_page"))

    except ValueError as e:
        flash(str(e))
        return render_template("auth/login.html")


# 로그아웃
@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("로그아웃되었습니다.")
    return redirect(url_for("auth.login"))

# 회원가입
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if session.get("member_id"):
        return redirect(url_for("todo.list_page"))

    if request.method == "GET":
        return render_template("auth/signup.html")

    uid = (request.form.get("uid") or "").strip()
    pw = (request.form.get("pw") or "")
    pw2 = (request.form.get("pw2") or "")
    name = (request.form.get("name") or "").strip()

    try:
        if not uid:
            raise ValueError("아이디(uid)는 필수입니다.")
        if len(uid) > 50:
            raise ValueError("아이디(uid)는 50자 이내로 입력하세요.")
        if not name:
            raise ValueError("이름(name)은 필수입니다.")
        if len(name) > 50:
            raise ValueError("이름(name)은 50자 이내로 입력하세요.")
        if not pw:
            raise ValueError("비밀번호는 필수입니다.")
        if pw != pw2:
            raise ValueError("비밀번호 확인이 일치하지 않습니다.")

        if MemberRepository.find_by_uid(uid):
            raise ValueError("이미 사용 중인 아이디입니다.")

        MemberRepository.create_member(uid=uid, password=pw, name=name, role="user")

        flash("회원가입 완료! 로그인 해주세요.")
        return redirect(url_for("auth.login"))

    except ValueError as e:
        flash(str(e))
        return render_template("auth/signup.html")