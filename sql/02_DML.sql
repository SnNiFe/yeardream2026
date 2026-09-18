/* 문자열 캐릭턴셋 변경 (latin1 -> utf8mb4)
sudo vim /etc/my.cnf
[mysqld]
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci
추가 후 :wq

sudo systemctl restart mariadb
sudo systemctl status mariadb
*/

SHOW VARIABLES LIKE 'character_set%';

-- 캐릭터셋이 바뀌기 전에 만들어져버린 database 와 table 에 대해서 변경
ALTER DATABASE mydb CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
ALTER TABLE employees CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE mydb;
-- INSERT
-- INSERT INTO [테이블명]([컬럼명,...])VALUES([값,...]);
INSERT INTO employees(
	emp_no, first_name, family_name, email, mobile, salary, depart_no, commission
)VALUES(
	111, '지훈', '김', 'zero0box@naver.com', '01020343054', 90000000,'dev001', 90
);

INSERT INTO employees(
	emp_no, first_name, family_name, email, mobile, salary
)VALUES(
	112, '태근', '김', 'email@naver.com', '01020343054', 90000000
);

INSERT INTO employees(
	emp_no, family_name, email, mobile, salary
)VALUES(
	113, '김', 'email@naver.com', '01020343054', 90000000
);

SELECT * FROM employees as e;

-- UPDATE
-- UPDATE [테이블] SET [열]=[값] WHERE [조건]
UPDATE employees SET depart_no = 'dev002' WHERE depart_no IS NULL;
UPDATE employees SET commission = 10 WHERE commission IS NULL;

-- DELETE
-- DELETE FROM [테이블명] WHERE [조건]
DELETE FROM employees WHERE first_name IS NULL;
SELECT * FROM employees as e;

-- UPSERT(나중에 자세하게...)
-- 값이 있으면 UPDATE, 없으면 INSERT
-- 키가 중복되면 UPDATE, 중복되지 않으면 INSERT
-- 키가 없으면 실행할 수 없다.
INSERT INTO employees(emp_no, first_name, family_name, email, mobile, salary)
	VALUES(112, '태근', '김', 'email@naver.com', '01012341234', 50000000)
		ON DUPLICATE KEY UPDATE first_name='태곤', family_name='박';


DESC employees;
