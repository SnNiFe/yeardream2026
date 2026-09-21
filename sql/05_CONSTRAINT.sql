-- 1) PRIMARY KEY(PK, 기본키)
-- 중복되지 않고, NULL 을 허용하지 않는다.
-- 테이블 종속적이다. (이 테이블 소속외에는 할수 없다.)
-- 테이블당 1개만 가능하며 하나이상의 컬럼으로 구성된다.(16개까지 조합이 가능)
-- 만약에 부득이하게 여러개의 컬럼으로 키를 만들경우(복합키)


-- 테이블을 생성하면서 기본키 생성(가장 많이 활용하는 방식)
CREATE TABLE pk_test(
	first_col INT(3) PRIMARY KEY,
	second_col VARCHAR(4)
);
DESC pk_test;

-- 이미 생성된 테이블에 키를 추가하는 방법(employees)
SELECT * FROM employees e ORDER BY emp_no;
DESC employees;
-- ALTER TABLE [테이블명] ADD CONSTRAINT [제약조건종류] [적용할 컬럼]
ALTER TABLE employees ADD CONSTRAINT PRIMARY KEY (emp_no);
-- 축약형
ALTER TABLE employees ADD PRIMARY KEY (emp_no);

-- 키가 중복되는 데이터 넣기
INSERT INTO employees (emp_no, first_name, family_name)	VALUES (112, '태곤', '박');

-- UPSERT
INSERT INTO employees (emp_no, first_name, family_name)
	VALUES (112, '태곤', '박')
		ON DUPLICATE KEY UPDATE first_name='태곤', family_name='박';

SELECT * FROM employees;

-- 복합키
CREATE TABLE pk_two_test(
	first_col INT(5),
	second_col VARCHAR(10),
	third_col DATE,
	PRIMARY KEY (first_col, second_col)
);
DESC pk_two_test;

-- 2) NOT NULL(NULL 허용하지 않음)
-- 속성 취급
-- ALTER TABLE [테이블명] ADD CONSTRAINT [제약조건종류] [적용할 컬럼]
ALTER TABLE pk_test MODIFY COLUMN second_col VARCHAR(4) NOT NULL;
DESC pk_test;

-- 3) 제약조건 삭제
-- ALTER TABLE [테이블명] DROP [제약조건 종류]
ALTER TABLE pk_test DROP PRIMARY KEY;