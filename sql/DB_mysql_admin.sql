CREATE USER 'todo_user'@'localhost'
IDENTIFIED BY 'ChangeThisPassword!';

CREATE USER 'todo_user'@'127.0.0.1'
IDENTIFIED BY 'ChangeThisPassword!';

GRANT ALL PRIVILEGES
ON todo_list.*
TO 'todo_user'@'localhost';

GRANT ALL PRIVILEGES
ON todo_list.*
TO 'todo_user'@'127.0.0.1';

FLUSH PRIVILEGES;
SHOW GRANTS FOR 'todo_user'@'localhost';