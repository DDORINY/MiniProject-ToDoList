/* =========================================================
   ToDo List Mini Project - MySQL 초기 세팅
   - DB: todo_list
   - Tables: members, todos
   - Admin 계정 생성 포함
========================================================= */

-- 0) DB 생성
CREATE DATABASE IF NOT EXISTS todo_list
	DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_general_ci;
    
-- 사용할 DB를 USE로 선택
USE todo_list;

-- 테이블 삭제 (수정용)
drop table members;

-- 1) members 테이블을 생성 [id(pk), uid, password, name, role, active, created_at, updated_at]
CREATE TABLE IF NOT EXISTS members (
    id INT AUTO_INCREMENT PRIMARY KEY, -- PK
    uid VARCHAR(50) NOT NULL UNIQUE,   -- 로그인 ID
    password VARCHAR(255) NOT NULL,    -- 비밀번호(해시 저장 권장)
    name VARCHAR(50) NOT NULL,         -- 이름
    
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user', -- 권한
    
    active BOOLEAN NOT NULL DEFAULT TRUE, -- 활성 여부
    
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 생성시간
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP -- 수정시간 자동갱신
) ENGINE=InnoDB;

-- 2) todos 테이블을 생성 [id (PK),member_id (FK), title (할 일 제목), memo , is_done (완료 여부: 0/1), due_date(마감일), active (삭제 여부: 0/1), created_at, updated_at]
CREATE TABLE IF NOT EXISTS todos (
    id INT AUTO_INCREMENT PRIMARY KEY,

    member_id INT NOT NULL, -- FK (작성자)

    title VARCHAR(200) NOT NULL, -- 할일 제목
    memo TEXT NOT NULL, -- 메모
    
    is_done BOOLEAN NOT NULL DEFAULT FALSE, -- 완료 여부
    due_date DATE NULL, -- 마감일 (선택)
    
    active BOOLEAN NOT NULL DEFAULT TRUE, -- 삭제 여부 (soft delete)

    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP 
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_todos_member
        FOREIGN KEY (member_id)
        REFERENCES members(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;

  
