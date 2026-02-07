# MiniProject-ToDoList

Flask + MySQL 기반 ToDo List 웹 애플리케이션 미니 프로젝트입니다.  
레이어드 아키텍처(Repository–Service–Route) 구조와 Blueprint 분리를 적용하여  
실무형 백엔드 구조를 연습하는 것을 목표로 했습니다.

---

# 프로젝트 목적

- Flask 웹 애플리케이션 구조 이해
- Blueprint 라우팅 분리
- Service / Repository 계층 구조 적용
- MySQL DB 설계 및 계정 권한 분리
- 사용자별 ToDo CRUD 구현
- Dashboard 요약 화면 구현

---

# 기술 스택

- Python 3.x
- Flask
- MySQL
- PyMySQL
- cryptography (MySQL sha2 인증)
- HTML / CSS
- Bootstrap 5

---

# 주요 기능

- 회원가입 / 로그인 / 로그아웃
- 사용자별 ToDo 목록
- 할 일 추가 / 수정 / 삭제 (Soft Delete)
- 완료 / 미완료 토글
- 마감일 관리
- 필터 (전체 / 완료 / 미완료)
- 검색 (제목 / 메모)
- Dashboard 요약 카드
  - 전체 개수
  - 미완료
  - 완료
  - 마감 초과(overdue)

---

# 프로젝트 구조
```
MiniProject-ToDoList/
├─ app/
│ ├─ init.py # create_app(), Blueprint 등록
│ ├─ config.py
│ ├─ db.py # MySQL 연결 함수
│ │
│ ├─ routes/
│ │ ├─ init.py
│ │ ├─ auth_routes.py # 로그인/회원가입
│ │ └─ todo_routes.py # dashboard + todo CRUD
│ │
│ ├─ services/
│ │ ├─ init.py
│ │ ├─ auth_service.py
│ │ └─ todo_service.py
│ │
│ ├─ repositories/
│ │ ├─ init.py
│ │ ├─ member_repository.py
│ │ └─ todo_repository.py
│ │
│ ├─ templates/
│ │ ├─ base.html
│ │ ├─ auth/
│ │ │ ├─ login.html
│ │ │ └─ signup.html
│ │ └─ todo/
│ │ ├─ dashboard.html
│ │ ├─ list.html
│ │ └─ edit.html
│ │
│ └─ static/
│ └─ css/style.css
│
├─ sql/
│ ├─ DB_mysql.sql
│ └─ DB_mysql_admin.sql
│
├─ requirements.txt
├─ run.py
└─ README.md
```

---

# 데이터베이스 설계

## Database
- todo_list


## members

| 컬럼 | 설명 |
|------|------|
id | PK |
uid | 로그인 ID (UNIQUE) |
password | 비밀번호 |
name | 사용자 이름 |
role | admin / user |
active | 활성 여부 |
created_at | 생성 시각 |
updated_at | 수정 시각 |

---

## todos

| 컬럼 | 설명 |
|------|------|
id | PK |
member_id | 작성자 FK |
title | 할 일 제목 |
memo | 메모 |
is_done | 완료 여부 |
due_date | 마감일 |
active | soft delete |
created_at | 생성 시각 |
updated_at | 수정 시각 |

---

# 실행 방법 (로컬)

## 가상환경
```
python -m venv .venv
.venv\Scripts\activate
```

---

## 패키지 설치
```
pip install -r requirements.txt
```

---

## DB 생성
```
sql/DB_mysql.sql 실행
sql/DB_mysql_admin.sql 실행
```

---

## 환경변수 (.env)

`.env.example` 복사 후 `.env` 생성

```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=todo_list
DB_USER=todo_user
DB_PASSWORD=비밀번호
SECRET_KEY=아무값
```

---

## 서버 실행
`python run.py`
[접속 : http://localhost:5000](http://localhost:5000)


---

# 설계 포인트

- Flask Blueprint 분리
- Repository → Service → Route 계층 구조
- DB 전용 계정 사용 (권한 최소화)
- Soft Delete 패턴 적용
- created_at / updated_at 자동 관리
- 인증 → 서비스 → 저장소 역할 분리

---

# 향후 확장 아이디어

- 우선순위 필드
- 태그 시스템
- REST API 제공
- React / Vue 프론트 분리
- 통계 차트 위젯
- 알림 기능

---

# 라이선스

학습 및 포트폴리오 용도






