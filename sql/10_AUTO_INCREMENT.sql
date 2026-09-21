-- PK 를 삼기위해 보통은 UUID 처럼 앤덤하고 중복되지 않는 값을 사용 한다.
SELECT UUID(); -- 몽고DB 의 _id

-- 자동 증가하는 auto_increment 를 사용하기도 한다.
-- auto_increment 는 키 설정이 되어 있어야만 한다.
-- 테이블 생성시 만들기
CREATE TABLE auto_inc(
	no INT(10) PRIMARY KEY auto_increment,
	name VARCHAR(10) NOT NULL
);
DESC auto_inc;

INSERT INTO auto_inc (name) VALUES ('kim');
INSERT INTO auto_inc (name) VALUES ('lee');
INSERT INTO auto_inc (name) VALUES ('park');
SELECT * FROM auto_inc;