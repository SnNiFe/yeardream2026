-- [QUERY] [UNION | UNION ALL | INTERSECT] [QUERY]
-- 동일한 컬림이 있어야 SET 연산이 가능하다.
SELECT deptno FROM dept
UNION
SELECT deptno FROM emp;

-- LEFT JOIN + RIGHT JOIN 효과를 UNION 으로 줘 보자
SELECT e.ename, e.deptno, d.deptname FROM emp e LEFT OUTER JOIN dept d ON e.deptno  = d.deptno
UNION
SELECT e.ename, d.deptno, d.deptname FROM emp e RIGHT OUTER JOIN dept d ON e.deptno  = d.deptno;

-- 교집합(INTERSECT) == 등가조인과 같은 효과
SELECT deptno FROM dept
INTERSECT
SELECT deptno FROM emp;

-- 차집합(MINUS) NOT IN
-- IN : 0 또는 0
-- NOT IN : IN 에 해당하는 것은 제외
SELECT DISTINCT deptno FROM dept; -- 1,2,3,4
SELECT DISTINCT deptno FROM emp; -- 1,2,4,6

-- dept - emp = 3
SELECT deptno FROM dept WHERE deptno NOT IN (SELECT DISTINCT deptno FROM emp);
-- emp - dept = 6
SELECT deptno FROM emp WHERE deptno NOT IN (SELECT DISTINCT deptno FROM dept);