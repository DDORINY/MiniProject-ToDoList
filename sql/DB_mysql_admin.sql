-- 사용자 계정 생성 
create user 'kdh'@'localhost' identified by '123';

-- 사용자 권한 부여
GRANT ALL PRIVILEGES ON todo_list.* TO 'kdh'@'localhost';
