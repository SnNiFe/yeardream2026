-- JOIN
-- 둘 이상의 테이블을 연결하여 데이터를 검색하는 방법
-- 둘 사이에 적어도 하나이상의 공통된 컬럼이 존재해야 한다.
-- 그래서 일반적으로 부모자식간에 JOIN 이 자주 일어난다. (PK-FK)

-- JOIN 방법
-- CROSS JOIN
-- *Equi JOIN (등가조인, 내부조인, 네추럴조인)
-- Non Equi JOIN <- 거의 사용하지 않음
-- Self JOIN	 <- 특수한 경우에만 사용
-- *Outer JOIN

-- 0. CROSS JOIN
-- 카다시안 곱 수행
-- emp(10) * dept(4) = 40
-- Equi JOIN 에서 조건문이 빠진 형태로 정제되기 전 버전
SELECT e.*, d.* FROM emp e CROSS JOIN dept d;
-- CROSS 와 JOIN 은 생략 가능
SELECT e.ename, d.deptno, d.deptname FROM emp e, dept d;

-- 1. Equi JOIN
-- CROSS JOIN 에서 두 테이블이 동일하게 있는 값만 을 추출한 형태
-- emp ename 이 kim 인 사람은 deptno 가 1이지? 그러니 dept 에서 deptno 1 인 녀석과만 합쳐

-- 1) 등가조인(가장 기본적인 조인)
SELECT e.ename, d.deptno, d.deptname FROM emp e, dept d
	WHERE e.deptno = d.deptno;
-- dept 에는 deptno 3 이 있다. 하지만 emp 에는 deptno 3 이 없기에 표시되지 않는다.

-- 2) 내부조인(INNER JOIN)
-- 테이블 사이에 ',' 대신 INNER JOIN 이 들어간다. (INNER 는 생략 가능)
-- JOIN 의 조건에 WHERE 가 아닌 ON 절 사용
-- WHERE 에 필터링 조건과 조인 조건을 모두 사용하면 혼돈 발생하므로, ON 절 사용
SELECT e.ename, d.deptno, d.deptname FROM emp e INNER JOIN dept d
	ON e.deptno = d.deptno;

-- USING 을 사용하면 조인에 사용할 컬럼이나 뷰 서브쿼리 등을 사용할 수 있다.
-- deptno 를 공통으로 활용하여 테이블을 합친다.
SELECT e.ename, d.deptno, d.deptname FROM emp e JOIN dept d USING (deptno);

-- 3) 내츄럴조인(NATURAL JOIN)
-- 두 테이블 사이에 공통된 컬럼이 있으면 알아서(자연스럽게) 합친다.
SELECT e.ename, deptno, d.deptname FROM emp e NATURAL JOIN dept d;


-- 2. 외부조인(OUTER JOIN)
-- Equi JOIN 은 두 테이블 모두에 데이터카 존재해야 보여준다.
-- 외부조인은 어느 한 테이블에만 있는 데이터라 해도 보여준다.

-- 등가 조인
-- dept 에 있는 deptno = 3 은 보여주지 않는다.
SELECT e.ename, d.deptno, d.deptname
	FROM emp e JOIN dept d ON e.deptno = d.deptno;

-- 외부 조인
-- 두 테이블 중 보여줄것이 더 많은 테이블을 지목하는 형태
SELECT e.ename, d.deptno, d.deptname
	FROM emp e RIGHT OUTER JOIN dept d ON e.deptno = d.deptno;

-- dept 에는 없고 emp 에만 있는 deptno 를 넣으려고 한다.
-- dept 는 emp 의 부모이기 때문에 emp 에 없는 deptno 란 있을 수 없다.
-- 부모자식 관계를 제거할 예정(FK 제거)
-- 제약조건 삭제
-- ALTER TABLE [테이블명] DROP CONSTRAINT [제약조건 이름]
SELECT * FROM information_schema.TABLE_CONSTRAINTS WHERE TABLE_NAME = 'emp';
ALTER TABLE emp DROP CONSTRAINT fk_emp;
DESC emp;

-- emp 에 deptno 6 을 추가
INSERT INTO emp
	VALUES ('kim', 'assistant', 6, STR_TO_DATE('14-06-02','%Y-%m-%d'));

SELECT * FROM emp;

-- emp 에 있는 deptno 를 기준으로 보여줘
SELECT e.ename, e.deptno, d.deptname
	FROM emp e LEFT JOIN dept d ON e.deptno = d.deptno;

-- LEFT JOIN + RIGHT JOIN = FULL OUTER JOIN
-- mariaDB 에서는 지원하지 않는다.(다른 방법이 있어서...)






