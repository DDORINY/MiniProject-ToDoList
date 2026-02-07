from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.todo_service import TodoService
from datetime import date

todo_bp = Blueprint("todo", __name__)
@todo_bp.route("/dashboard")
def dashboard():
    member_id = session.get("member_id")
    if not member_id:
        return redirect(url_for("auth.login"))

    data = TodoService.get_dashboard(member_id)
    return render_template("todo/dashboard.html", **data)

@todo_bp.route("/todos")
def list_page():
    member_id = session.get("member_id")
    if not member_id:
        return redirect(url_for("auth.login"))

    filter_done = request.args.get("filter", "all")
    q = request.args.get("q", "").strip() or None

    todos = TodoService.get_list(member_id, filter_done=filter_done, q=q)

    return render_template(
        "todo/list.html",
        todos=todos,
        filter_done=filter_done,
        q=q,
        today=date.today()
    )
@todo_bp.route("/todos",methods=["POST"])
def add():
    member_id = session.get("member_id")
    if not member_id:
        return redirect(url_for("auth.login"))

    title = request.form.get("title")
    memo = request.form.get("memo")
    due_date = request.form.get("due_date")

    try:
        TodoService.add(member_id,title,memo,due_date)
        flash("할 일이 추가되었습니다.")
    except ValueError as e:
        flash(str(e))
    return redirect(url_for("todo.list_page"))


@todo_bp.route("/todos/<int:todo_id>/toggle",methods=["POST"])
def toggle(todo_id):
    member_id = session.get("member_id")
    try:
        TodoService.toggle(member_id,todo_id)
    except ValueError as e:
        flash(str(e))
    return redirect(url_for("todo.list_page"))

@todo_bp.route("/todos/<int:todo_id>/edit")
def edit_page(todo_id):
    member_id = session.get("member_id")
    try:
        todo = TodoService.get_detail(member_id,todo_id)
        return render_template("todo/edit.html",todo=todo)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("todo.list_page"))

@todo_bp.route("/todos/<int:todo_id>/edit",methods=["POST"])
def edit(todo_id):
    member_id = session.get("member_id")
    title = request.form.get("title")
    memo = request.form.get("memo")
    due_date = request.form.get("due_date")

    try:
        TodoService.edit(member_id,todo_id,title,memo,due_date)
        flash("수정되었습니다.")
    except ValueError as e:
        flash(str(e))
    return redirect(url_for("todo.list_page"))

@todo_bp.route("/todos/<int:todo_id>/delete",methods=["POST"])
def delete(todo_id):
    member_id = session.get("member_id")
    try:
        TodoService.delete(member_id,todo_id)
        flash("삭제되었습니다.")
    except ValueError as e:
        flash(str(e))

    return redirect(url_for("todo.list_page"))