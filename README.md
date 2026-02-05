# MiniProject-ToDoList
Flask + MySQL ToDo List Mini Project
# Flask + MySQL ToDo List Mini Project

간단한 할 일 관리(ToDo List) 웹 애플리케이션입니다.
Flask 기반 백엔드 구조와 MySQL DB 연동을 연습하기 위한 미니 프로젝트입니다.

---

# 프로젝트 목적

* Flask 웹 구조 이해
* Blueprint 라우팅 분리
* Service / Repository 레이어 구조 적용
* MySQL DB 설계 및 권한 분리
* 사용자별 ToDo CRUD 구현

---

# 기술 스택

* Python 3.x
* Flask
* MySQL
* PyMySQL
* HTML / CSS

---

# 프로젝트 구조

```
todo-list-flask/
├─ app/
│  ├─ repositories/        # DB 접근 계층 (SQL)
│  │   └─ todo_repository.py
│  ├─ services/            # 비즈니스 로직
│  │   └─ todo_service.py
│  ├─ routes/              # URL 라우팅 (Blueprint)
│  │   ├─ auth_routes.py
│  │   └─ todo_routes.py
│  ├─ templates/           # HTML 템플릿
│  ├─ static/              # CSS / JS
│  ├─ db.py                # DB 연결
│  ├─ config.py            # 설정
│  └─ __init__.py          # create_app()
│
├─ sql/
│  ├─ 01_create_tables.sql
│  └─ 02_create_user.sql
│
├─ run.py                  # 서버 실행
├─ requirements.txt
├─ .env.example
└─ README.md
```

---

# 데이터베이스 설계

## Database

```
todo_list
```

## members 테이블

| 컬럼         | 설명              |
| ---------- | --------------- |
| id         | PK              |
| uid        | 로그인 ID (UNIQUE) |
| password   | 비밀번호            |
| name       | 이름              |
| role       | admin / user    |
| active     | 활성 여부           |
| created_at | 생성시각            |
| updated_at | 수정시각            |

---

## todos 테이블

| 컬럼         | 설명          |
| ---------- | ----------- |
| id         | PK          |
| member_id  | 작성자 FK      |
| title      | 할 일 제목      |
| memo       | 메모          |
| is_done    | 완료 여부       |
| due_date   | 마감일         |
| active     | soft delete |
| created_at | 생성시각        |
| updated_at | 수정시각        |

---

# DB 계정 정책

앱 전용 계정을 생성하여
**todo_list DB에만 접근 권한**을 부여했습니다.

```
CREATE USER 'todo_user'@'localhost';
GRANT ALL ON todo_list.* TO 'todo_user'@'localhost';
```

---

# 실행 방법 (로컬)

## 1️ 가상환경 생성

```
python -m venv .venv
.venv\Scripts\activate
```

---

## 2️ 패키지 설치

```
pip install -r requirements.txt
```

---

## 3️ DB 생성

```
sql/01_create_tables.sql 실행
sql/02_create_user.sql 실행
```

---

## 4️ 환경변수 설정

`.env.example`을 복사해서 `.env` 생성

```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=todo_list
DB_USER=todo_user
DB_PASSWORD=비밀번호
SECRET_KEY=아무값
```

---

## 5️ 서버 실행

```
python run.py
```

접속:

```
http://localhost:5000
```

---

# 주요 기능

* 회원 로그인 / 로그아웃
* 사용자별 ToDo 목록
* 할 일 추가
* 할 일 수정
* 완료 토글
* soft delete
* 관리자 계정 지원

---

# 설계 포인트

* Flask Blueprint 분리
* Repository → Service → Route 계층 구조
* DB 권한 최소화
* Soft delete 패턴 적용
* created_at / updated_at 자동 관리

---

# 향후 확장 아이디어

* 검색 / 필터
* 우선순위
* 태그
* REST API 버전 추가
* React 프론트 분리

---

# 라이선스

학습 및 포트폴리오 용도

```
```
