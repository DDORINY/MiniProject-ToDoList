from app.repositories.todo_repository import TodoRepository

class TodoService:
    @staticmethod
    def get_dashboard(member_id: int):
        if not member_id:
            raise ValueError("로그인 후 이용해주세요.")

        summary = TodoRepository.count_summary(member_id)
        due_today = TodoRepository.list_due_today(member_id, limit=5)
        overdue = TodoRepository.list_overdue(member_id, limit=5)
        for row in (due_today + overdue):
            if row.get("memo") is None:
                row["memo"] = ""

        return {
            "summary": summary,
            "due_today": due_today,
            "overdue": overdue
        }

    @staticmethod
    def get_list(member_id: int, filter_done: str | None = None, q: str | None = None):
        # 일정 목록 조회
        if not member_id:
            raise ValueError("로그인 후 이용해주세요.")

        todos = TodoRepository.list_by_member(member_id, filter_done=filter_done, q=q)

        for t in todos:
            if t.get("memo") is None:
                t["memo"] = ""

        return todos

    @staticmethod
    def add(member_id: int, title: str, memo: str = "", due_date: str | None = None):
        # 일정 생성
        if not member_id:
            raise ValueError("로그인 후 이용해주세요.")

        title = (title or "").strip()
        if not title:
            raise ValueError("제목은 필수입니다.")
        if len(title) > 200:
            raise ValueError("제목은 200자 이내로 작성해주세요.")

        memo = (memo or "").strip()
        due_date = (due_date or "").strip() or None

        new_id = TodoRepository.create(
            member_id=member_id,
            title=title,
            memo=memo,
            due_date=due_date
        )
        return new_id

    @staticmethod
    def get_detail(member_id: int, todo_id: int):
        # 일정 상세조회
        if not member_id:
            raise ValueError("로그인 후 이용해주세요.")
        if not todo_id:
            raise ValueError("잘못된 요청입니다.")

        todo_row = TodoRepository.get_by_id(todo_id=todo_id, member_id=member_id)
        if not todo_row:
            raise ValueError("할 일을 찾을 수 없습니다.")

        if todo_row.get("memo") is None:
            todo_row["memo"] = ""

        return todo_row

    @staticmethod
    def edit(member_id: int, todo_id: int, title: str, memo: str = "", due_date: str | None = None):
        # 일정 수정
        if not member_id:
            raise ValueError("로그인 후 이용해주세요.")
        if not todo_id:
            raise ValueError("잘못된 요청입니다.")

        title = (title or "").strip()
        if not title:
            raise ValueError("제목은 필수입니다.")
        if len(title) > 200:
            raise ValueError("제목은 200자 이하로 입력하세요.")

        memo = (memo or "").strip()
        due_date = (due_date or "").strip() or None

        changed = TodoRepository.update(
            todo_id=todo_id,
            member_id=member_id,
            title=title,
            memo=memo,
            due_date=due_date
        )

        if changed == 0:
            raise ValueError("수정할 수 없습니다. (존재하지 않거나 권한이 없습니다.)")

        return changed

    @staticmethod
    def toggle(member_id: int, todo_id: int):
        # 완료토글 (완료 ↔ 미완료)
        if not member_id:
            raise ValueError("로그인 후 이용해주세요.")
        if not todo_id:
            raise ValueError("잘못된 요청입니다.")

        changed = TodoRepository.toggle_done(todo_id=todo_id, member_id=member_id)
        if changed == 0:
            raise ValueError("토글할 수 없습니다. (존재하지 않거나 권한이 없습니다.)")

        return changed

    @staticmethod
    def delete(member_id: int, todo_id: int):
        # 일정 삭제 (soft delete)
        if not member_id:
            raise ValueError("로그인 후 이용해주세요.")
        if not todo_id:
            raise ValueError("잘못된 요청입니다.")

        changed = TodoRepository.soft_delete(todo_id=todo_id, member_id=member_id)
        if changed == 0:
            raise ValueError("삭제할 수 없습니다. (존재하지 않거나 권한이 없습니다.)")

        return changed
