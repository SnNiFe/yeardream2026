-- 1. 참조제약조건
-- FOREIGN KEY(외래키 - 내것이 아닌 키를 가져다 씀)
-- 1) 만들면서 설정
-- 부모
CREATE TABLE parent_table(
	user_id VARCHAR(30) PRIMARY KEY,
	user_name VARCHAR(20),
	user_phone VARCHAR(10),
	user_addr VARCHAR(100)
);
DESC parent_table;

-- 자식
CREATE TABLE child_table(
	order_id INT(10),
	user_id VARCHAR(30),
	product_name VARCHAR(30),
	price INT(10),
	qty VARCHAR(5)
	-- ,FOREIGN KEY(user_id) REFERENCES parent_table(user_id)
);
DESC child_table;

-- 2) 테이블 생성 후 추가
-- 부모의 PK 를 나의 PK 로 사용하고 있지 않다.(비식별 관계)
-- ALTER TABLE [테이블명] ADD CONSTRAINT [제약조건종류](적용컬럼) REFERENCES [테이블](컬럼)
ALTER TABLE child_table ADD CONSTRAINT 
	FOREIGN KEY (user_id) REFERENCES parent_table(user_id);

-- 3) 식별관계 추가
-- 부모의 PK 를 나의 PK 로 사용(굉장히 특수한 경우)
CREATE TABLE iden_table(
	order_id INT(10),
	user_id VARCHAR(30) PRIMARY KEY,
	product_name VARCHAR(30),
	price INT(10),
	qty VARCHAR(5),
	FOREIGN KEY(user_id) REFERENCES parent_table(user_id)
);
DESC iden_table;

-- 데이터 추가
INSERT INTO parent_table (user_id, user_name, user_phone, user_addr)
	VALUES ('user01', '김철수', '0212341234', '서울 영등포구');

INSERT INTO parent_table (user_id, user_name, user_phone, user_addr)
	VALUES ('user02', '홍길동', '0212341234', '서울 영등포구');

INSERT INTO parent_table (user_id, user_name, user_phone, user_addr)
	VALUES ('user03', '박영수', '0212341234', '서울 영등포구');

SELECT * FROM parent_table;

-- 데이터 추가(자식)
INSERT INTO child_table (order_id, user_id, product_name, price, qty)
	VALUES (1, 'user01', '의류', 6000, 1);

INSERT INTO child_table (order_id, user_id, product_name, price, qty)
	VALUES (2, 'user02', '의류', 6000, 1);

INSERT INTO child_table (order_id, user_id, product_name, price, qty)
	VALUES (3, 'user03', '의류', 6000, 1);

SELECT * FROM child_table;

-- 모든 컬럼에 값이 들어갈 경우 컬럼명 생략 가능(비추)
-- 에러가 나는데, 이유는 user04는 부모에게 없는 값 이기 때문
-- 연계 참고 무결성 제약조건
INSERT INTO child_table VALUES (4, 'user04', '의류', 6000, 1);

-- 반대로 부모가 지워지려고 할때 자식이 있는경우 지울수 없다.(****)
-- 이 경우 자식을 먼저 다 지우고, 이후에 부모를 지워야 한다.(간단하게 할 수 있는 방법 -> 마지막에)
DELETE FROM parent_table WHERE user_id = 'user01';

-- 식별관계의 독특한 상황
INSERT INTO iden_table VALUES (1, 'user01', '의류', 6000, 1);
INSERT INTO iden_table VALUES (2, 'user02', '의류', 6000, 1);
INSERT INTO iden_table VALUES (3, 'user03', '의류', 6000, 1);

INSERT INTO iden_table VALUES (4, 'user01', '신발', 6000, 1);

SELECT * FROM iden_table;


-- 자식테이블 삭제 후 부모테이블 삭제
DROP TABLE iden_table;
DROP TABLE child_table;
DROP TABLE parent_table;

-- ON DELETE CASCADE 옵션을 넣으면
-- 부모 데이터를 지울때 자식데이터를 먼저 지우고 이후 부모데이터를 지운다.
-- 그래서 연계참조무결성 제약조건을 위배하지 않고 데이터를 지울수 있게 된다.
CREATE TABLE parent_table(
	user_id VARCHAR(30) PRIMARY KEY,
	user_name VARCHAR(20),
	user_phone VARCHAR(11),
	user_addr VARCHAR(100)
);
DESC parent_table;

CREATE TABLE child_table(
	order_id INT(10),
	user_id VARCHAR(30),
	product_name VARCHAR(30),
	price INT(10),
	qty VARCHAR(5),
	FOREIGN KEY(user_id) REFERENCES parent_table(user_id)
	ON DELETE CASCADE
);
DESC child_table;

-- 이제 부모를 지울때 자식이 자동으로 먼저 지워진다.
DELETE FROM parent_table WHERE user_id = 'user01';

-- 2. 유니크 제약 조건(중복을 허용하지 않는 제약조건)
-- 테이블에 여러개 존개 가능
-- 유니크 + NOT NULL = 기본키
-- 유니크 제약조건(유니크 키) 는 언제든지 기본키가 될 준비가 되어있다.
-- ALTER TABLE [테이블명] ADD CONSTRAINT [제약조건명] (컬럼)
ALTER TABLE child_table ADD CONSTRAINT UNIQUE (order_id);

SELECT * FROM child_table;
DESC child_table;

-- 3. 체크 제약 조건(80~90년대 만들어진 소스의 경우 가끔 있다.)
-- 특정한 조건이 맞을 경우 입력시켜 준다.
-- ALTER TABLE [테이블명] ADD CONSTRAINT CHECK (조건)
-- 물품 가격이 5000~10000원 사이만 받겠다. 아니면 에러
ALTER TABLE child_table ADD CONSTRAINT CHECK (price BETWEEN 5000 AND 10000);
-- 단점 1. 체크제약조건이 걸려있는지 확인이 어렵다.
DESC child_table;
SELECT * FROM information_schema.CHECK_CONSTRAINTS cc;
INSERT INTO child_table VALUES (4, 'user02', '신발', 10000, 1);
-- 단점 2. 에러 발생시 원인파악이 쉽지 않다.
INSERT INTO child_table VALUES (5, 'user02', '신발', 11000, 1);
-- 단점 3. 조건 변경시 테이블 구조(속성)를 변경해야 한다.
