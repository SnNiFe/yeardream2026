CREATE TABLE dept(
  deptno VARCHAR(10) PRIMARY KEY,
  deptname VARCHAR(20),
  loc VARCHAR(10)
);

-- 직원 테이블 생성
CREATE TABLE emp(
  ename varchar(20),
  job varchar(50),
  deptno VARCHAR(10),
  hiredate date
);

-- 키 설정
ALTER TABLE emp ADD CONSTRAINT fk_emp FOREIGN KEY(deptno) REFERENCES dept(deptno);


-- 데이터 삽입
INSERT INTO dept (deptno,deptname,loc)values(1, 'sales', 'NEWYORK');
INSERT INTO dept (deptno,deptname,loc)values(2, 'dev01', 'LA');
INSERT INTO dept (deptno,deptname,loc)values(3, 'personnel', 'NEWYORK');
INSERT INTO dept (deptno,deptname,loc)values(4, 'delevery', 'BOSTON');
SELECT * FROM dept;

INSERT INTO emp (ename,job,deptno,hiredate)values('kim', 'manager', 1, STR_TO_DATE('26/01/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('lee', 'staff', 1, STR_TO_DATE('25/01/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('han', 'staff', 1, STR_TO_DATE('26/03/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('kim', 'assistant', 1, STR_TO_DATE('15/09/22','%Y/%m/%d'));

INSERT INTO emp (ename,job,deptno,hiredate)values('ahn', 'staff', 2, STR_TO_DATE('25/11/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('hwang', 'manager', 2, STR_TO_DATE('25/08/12','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('cha', 'assistant', 2, STR_TO_DATE('22/03/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('hong', 'staff', 2, STR_TO_DATE('24/08/02','%Y/%m/%d'));
INSERT INTO emp (ename,job,deptno,hiredate)values('gang', 'staff', 2, STR_TO_DATE('26/01/02','%Y/%m/%d'));

INSERT INTO emp (ename,job,deptno,hiredate)values('nam', 'leader', 4, STR_TO_DATE('20/01/02','%Y/%m/%d'));
SELECT * FROM emp;