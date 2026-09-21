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

-- 문제1> han 의 근무 부서 이름?
-- 3+4 =  7
-- 이름이 han 인 직원의 부서 번호 알아내기
SELECT deptno FROM emp WHERE ename = 'han'; -- deptno = 1
-- 7*2 = 14
-- 해당 부서 번호로 부서의 이름 알아내기
SELECT deptname FROM dept WHERE deptno = 1; -- sales

-- (3+4)*2 = 14
SELECT deptname FROM dept 
	WHERE deptno = (SELECT deptno FROM emp WHERE ename = 'han');


-- 문제 2> 부서위치가 LA 또는 BOSTON 인 부서에 속한 사람들의 이름과 직책
-- 부서위치가 LA 또는 BOSTON 의 번호
SELECT deptno FROM dept WHERE loc = 'LA' OR loc = 'BOSTON'; -- deptno = 2,4
-- 부서번호를 통해서 이름, 직책
SELECT ename, job FROM emp WHERE deptno = 2 OR deptno = 4;

SELECT ename, job FROM emp
	WHERE deptno IN (SELECT deptno FROM dept WHERE loc IN ('LA', 'BOSTON'));


-- 문제 3> sales 부서에 근무하는 사원의 이름,직책,입사일 알아보기
-- sales 부서의 deptno 알아보기
SELECT deptno FROM dept WHERE deptname = 'sales'; -- deptno = 1
-- deptno = 1 인 사람의 이름, 직책, 입사일 찾기
SELECT ename, job, hiredate FROM emp WHERE deptno = 1;

SELECT ename, job, hiredate FROM emp 
	WHERE deptno = (SELECT deptno FROM dept WHERE deptname = 'sales');


-- 문제 4> 직책이 MANAGER 인 직원들(여러명일 경우 가장 빠른사람 기준) 보다 입사일이 빠른 사람들
-- 이름, 직책, 입사일
SELECT hiredate  FROM emp WHERE job = 'manager' ORDER BY hiredate LIMIT 1; -- '2025-08-12'
SELECT ename, job, hiredate FROM emp WHERE hiredate < '2025-08-12';

SELECT ename, job, hiredate FROM emp
	WHERE hiredate < (SELECT MIN(hiredate)  FROM emp WHERE job = 'manager');


-- 문제 5> 부서별로 직원이 몇명인지 알려주세요
-- SELECT deptname, deptno FROM dept;
-- SELECT deptno, COUNT(deptno) as 인원 FROM emp WHERE deptno GROUP BY deptno;
SELECT * FROM dept;

SELECT deptname FROM dept WHERE deptno = 1;

-- 서브쿼리가 메인쿼리의 일부가 되었다.
-- 상하 관계 쿼리
-- dept 의 deptno 가 오직 1만 나타남
SELECT
	deptname,
	(SELECT COUNT(deptno) FROM emp WHERE deptno = 1) as cnt
FROM dept WHERE deptno = 1;


SELECT
	deptname,
	-- 그렇게 불러온 deptno 를 활용함
	(SELECT COUNT(deptno) FROM emp WHERE deptno = dept.deptno) as cnt
FROM dept; -- dept 의 모든 deptno 를 불러옴

-- SELECT deptname FROM dept WHERE deptno = 1
SELECT 
	e.deptno,
	(SELECT deptname FROM dept WHERE deptno = e.deptno) AS name,
	COUNT(deptno) as cnt 
FROM emp e GROUP BY e.deptno;

