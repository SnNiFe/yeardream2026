-- 1. 특정 컬럼 조회
SELECT * FROM employees;
SELECT emp_no, first_name, family_name, mobile FROM employees;

-- 산술 표현(계산결과 보여주기)
-- as 는 긴 컬럼명을 단축명으로 만들어준다.(alias)
SELECT first_name, family_name, salary/10000 as 급여 FROM employees;

-- 문자열합치기
SELECT 
	CONCAT(family_name, first_name) as 이름, 
	CONCAT(salary/10000,'만원') as 급여 
FROM employees;

-- 숫자+문자를 하면 숫자가 소숫점으로 표현된다.
-- 이럴경우 TRUNCATE(숫자,남길수솟점) 을 통해 정리해 주면 된다.
SELECT 
	CONCAT(family_name, first_name) as 이름, 
	CONCAT(TRUNCATE(salary/10000,0),'만원') as 급여 
FROM employees;

-- 2. 조건(WHERE)
SELECT * FROM employees e WHERE e.family_name = '김';
SELECT * FROM employees e WHERE e.salary > 3000000;
-- AND
SELECT e.family_name, e.first_name, e.salary 
	FROM employees e WHERE e.salary >= 1000000 AND e.salary <= 5000000;

-- BETWEEN AND
-- 숫자에만 적용(잘 사용되지 않는다.) / <> 와 같은 부등호가 태그로 인식될 경우 사용
SELECT e.family_name, e.first_name, e.salary 
	FROM employees e WHERE e.salary BETWEEN 1000000 AND 5000000;

-- OR
SELECT * FROM employees e WHERE e.family_name = '김' OR e.salary = 2000000;

-- 중복제거
-- SELECT DISTINCT [출력할 컬럼] FROM [테이블]
-- DISTINCT 이후의 컬럼에 대해서 중복을 제거후 출력
SELECT e.family_name FROM employees e ORDER BY e.family_name ASC;
SELECT DISTINCT e.family_name FROM employees e ORDER BY e.family_name ASC;

SELECT e.family_name, e.salary FROM employees e ORDER BY e.family_name;

-- e.family_name 과 e.salary 를 조합한 내용이 중복된 경우만 제거
SELECT DISTINCT e.family_name, e.salary FROM employees e ORDER BY e.family_name;

-- IN 절(여러 OR 조건을 하나로 합친...)
SELECT * FROM employees e WHERE e.family_name = '김' OR e.family_name = '이' OR e.family_name = '박';

-- 장점 : 간결하다. 속도가 빠르다.
-- 한계점 : 모든 OR 가 동일한 컬럼을 대상으로 해야 한다.
SELECT * FROM employees e WHERE e.family_name IN ('김','이','박');

-- LIKE
-- 일부가 비슷한 내용을 검색
-- WHERE [컬럼명] LIKE '%문자열%'
-- ze%		: ze 이후로 아무거나 와도 된다. -> ze로 시작하는 문장
-- %com		: com 으로 끝나는 문장
-- %se%		: se 를 포함하는 문장
-- %s%e%	: s 와 e 를 포함하는 문장
SELECT e.email FROM employees e WHERE e.email LIKE 'ze%';
SELECT e.email FROM employees e WHERE e.email LIKE '%com';
SELECT e.email FROM employees e WHERE e.email LIKE '%se%';
SELECT e.email FROM employees e WHERE e.email LIKE '%s%e%';

-- 3. 정렬(ORDER BY)
-- ORDER BY [컬럼명] [ASC|DESC]
-- 조건 검색 > 정렬 순
SELECT * FROM employees e WHERE e.salary > 2000000 ORDER BY e.salary DESC;

-- salsry 로 내림차순, 동률에 대해서 first_name 오름차순
SELECT * FROM employees e WHERE e.salary > 2000000 ORDER BY e.salary DESC, e.first_name ASC;

-- GROUP BY
-- 데이터를 특정 컬럼을 기준으로 묶어서 가져온다.(통계)
SELECT DISTINCT e.depart_no FROM employees e;
SELECT * FROM employees e;
-- dev001 ~ dev005 급여총합?
SELECT e.depart_no, SUM(e.salary) FROM employees e ORDER BY e.depart_no; -- d1: 9590, d2: 9680, d3: 1840, d4: 2520, d5: 770
SELECT e.depart_no, SUM(e.salary) FROM employees e WHERE e.depart_no = 'dev001'; -- 9,590
SELECT e.depart_no, SUM(e.salary) FROM employees e WHERE e.depart_no = 'dev002'; -- 9,680
SELECT e.depart_no, SUM(e.salary) FROM employees e WHERE e.depart_no = 'dev003'; -- 1,840
SELECT e.depart_no, SUM(e.salary) FROM employees e WHERE e.depart_no = 'dev004'; -- 2,520
SELECT e.depart_no, SUM(e.salary) FROM employees e WHERE e.depart_no = 'dev005'; -- 770

-- 특정 기준으로 묶어서 보여줌(각 기준별 1row 가 나와야 하기에 연산이 꼭 들어가야 한다.)
-- 연산이 들어가지 않으면 row 의 가장 첫값을 보여준다.(원래는 에러가 나타남)
SELECT e.depart_no, SUM(e.salary) as 총급여 FROM employees e GROUP BY e.depart_no;

-- 각 부서별 급여 합계(SUM)와 인센티브(commission) 의 평균(AVG)을 구해보자
SELECT e.depart_no, SUM(e.salary) as 총급여, AVG(IFNULL(e.commission, 0)) as 평균인센티브 FROM employees e GROUP BY e.depart_no;
SELECT e.depart_no, SUM(e.salary) as 총급여, SUM(e.commission)/COUNT(*) as 평균인센티브 FROM employees e GROUP BY e.depart_no;

SELECT e.depart_no, SUM(e.salary) as 총급여, AVG(e.commission) as 평균인센티브 FROM employees e GROUP BY e.depart_no;

-- 급여평균, 인원수
SELECT e.depart_no, FLOOR(AVG(e.salary)) as 급여평균, COUNT(e.depart_no) as 인원 FROM employees e GROUP BY e.depart_no;

-- HAVING : GROUP BY 로 받아온 데이터에 대해서 조건을 주는것(WHERE)
SELECT e.depart_no, FLOOR(AVG(e.salary)) as 급여평균, COUNT(e.depart_no) as 인원 FROM employees e GROUP BY e.depart_no HAVING 급여평균 > 5000000;

-- HAVING 에 별칭이 통하지 않는 DB 도 있다.
-- 그 경우 별칭을 주기전 이름으로 사용해야 한다.
SELECT e.depart_no, FLOOR(AVG(e.salary)) as 급여평균, COUNT(e.depart_no) as 인원 FROM employees e GROUP BY e.depart_no HAVING FLOOR(AVG(e.salary)) > 5000000;