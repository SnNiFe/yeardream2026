-- test_data 를 서버에 이동(filezilla 활용)
-- dump 복원 작업 (dump 란? DB 데이터 전체를 저장해 놓은 것을 말함)
-- dump 는 최소 월 1회정도는 권장
-- 이 덤프는 어떤 데이터베이스를 가지고 있는가? employees
CREATE DATABASE employees; -- database 를 먼저 만들어 주자
-- DB 가 있는 곳에서 복구 명령어 실행
-- putty 를 통해 서버에 접근
-- [mysql|mariadb] -u root -p [넣을 데이터 베이스] < [실행할 sql 경로]
mysql -u root -p employees < test_data/employees.sql

USE employees;
SHOW tables;

SELECT * FROM current_dept_emp LIMIT 5;		-- 현재 사원별 소속 팀 : emp_no(int) , dept_no , from_date , to_date
DESC current_dept_emp;

SELECT * FROM departments LIMIT 5;			-- 팀 정보 : dept_no , dept_name
SELECT * FROM dept_emp LIMIT 5;				-- 사원별 소속 팀(현재뿐 아니라 과거정보도 있나?) : emp_no , dept_no , from_date , to_date
SELECT * FROM dept_emp_latest_date LIMIT 5;	-- 부서별 사원 최신(current_dept_emp 와 비슷?) : emp_no , from_date , to_date
SELECT * FROM dept_manager LIMIT 5;			-- 부서별 매니저(담당자) : emp_no , dept_no , from_date , to_date
SELECT * FROM employees LIMIT 5;			-- 사원 : emp_no , birth_date , first_name , last_name , gender , hire_date
SELECT * FROM salaries LIMIT 5;				-- 급여 : emp_no , salary , from_date(gmt+a) , to_date
SELECT * FROM titles LIMIT 5;				-- 직책 : emp_no , title , from_date(gmt+a) , to_date


-- 문제 1번 : 사원들의 이름(썽과 이름을 합쳐서)과 입사일, 직책을 입사일이 빠른 순으로 보여주시오

SELECT CONCAT(e.last_name, ' ', e.first_name) AS name, e.hire_date FROM employees e;
SELECT t.emp_no, t.title FROM titles t;

SELECT CONCAT(e.last_name, ' ', e.first_name) AS name, e.hire_date, t.title FROM employees e JOIN titles t ON e.emp_no = t.emp_no ORDER BY e.hire_date ASC;

-- 직책은 기간이 지남에 따라 변경될 수 있기에 titles 에 히스토리처럼 쌓인다.
-- 최신의 title 만 나오도록 수정

SELECT * FROM titles t WHERE t.to_date = '9999-01-01';

SELECT CONCAT(e.last_name, ' ', e.first_name) AS name, e.hire_date, t.title
FROM employees e JOIN titles t ON e.emp_no = t.emp_no WHERE t.to_date = '9999-01-01'
ORDER BY e.hire_date ASC;


-- dept_emp 를 보면 사원이 여러 팀을 옮겨다닌 경우가 있다는 것을 알 수 있다.
SELECT COUNT(emp_no) FROM employees; -- 300,024
SELECT COUNT(emp_no) FROM dept_emp;  -- 331,603


-- 문제 2 : 팀 이동이 있었던 사원의 이름을 가져오세요

SELECT * FROM dept_emp de WHERE de.to_date != '9999-01-01' AND de.emp_no IN (SELECT de.emp_no FROM dept_emp de WHERE de.to_date = '9999-01-01');
SELECT de.emp_no FROM dept_emp de WHERE de.to_date = '9999-01-01';
SELECT CONCAT(e.last_name, ' ', e.first_name) AS name FROM employees e;

SELECT DISTINCT e.emp_no, CONCAT(e.last_name, ' ', e.first_name) AS name FROM employees e 
JOIN (SELECT * FROM dept_emp dee WHERE dee.to_date != '9999-01-01' AND dee.emp_no IN (SELECT d.emp_no FROM dept_emp d WHERE d.to_date = '9999-01-01')) de
ON e.emp_no =de.emp_no; -- 0.174s

-- 1 단계 : 부서이동이 있는 사람의 사원번호 추출
SELECT de.emp_no, COUNT(de.emp_no) AS cnt FROM dept_emp de GROUP BY de.emp_no HAVING cnt > 1;

-- 2 단계 : 이렇게 추출한 emp_no 로 employees 에서 이름 가져오기
-- 서브쿼리를 조건으로
SELECT e.emp_no, CONCAT(e.first_name, ', ', e.last_name) AS name FROM employees e WHERE e.emp_no 
IN (SELECT de.emp_no FROM dept_emp de GROUP BY de.emp_no HAVING COUNT(de.emp_no) > 1); -- 0.09s

-- 서브쿼리를 상하관계 쿼리로 활용하여 조인
SELECT e.emp_no, CONCAT(e.first_name, ', ', e.last_name) AS name FROM employees e 
JOIN (SELECT de.emp_no FROM dept_emp de GROUP BY de.emp_no HAVING COUNT(de.emp_no) > 1) d ON e.emp_no = d.emp_no; -- 0.244s


-- 문제 3 : 각 인원들이 어느팀에서 어느팀으로 이동했는지 알아보기
-- 이름, 팀명, from_date, to_date

SELECT e.emp_no, CONCAT(e.first_name, ', ', e.last_name) AS name, d2.dept_name, d.from_date, d.to_date 
FROM employees e JOIN dept_emp d ON e.emp_no = d.emp_no JOIN departments d2 ON d.dept_no = d2.dept_no 
WHERE -- d.to_date = '9999-01-01' AND 
e.emp_no IN (SELECT de.emp_no FROM dept_emp de GROUP BY de.emp_no HAVING COUNT(de.emp_no) > 1); -- 0.089s 미완성..?

-- 이름 팀명은 모르지만, 이동 순서대로 정렬
-- 서브쿼리
SELECT
	-- 이후 emp_no 와 dept_no 를 통해 서브쿼리로 원하는 데이터 추출
	(SELECT CONCAT(first_name, ', ', last_name) FROM employees WHERE emp_no = de.emp_no) AS name,
	(SELECT dept_name FROM departments WHERE dept_no = de.dept_no) AS team_name,
	de.from_date,
	de.to_date
FROM dept_emp de WHERE de.emp_no
IN (SELECT de.emp_no FROM dept_emp de GROUP BY emp_no HAVING COUNT(de.emp_no) > 1)
ORDER BY emp_no, from_date; -- 0.227s

-- JOIN 이용
-- 1) departments 와 dept_emp JOIN
SELECT 
	d.dept_name,
	de.emp_no,
	de.from_date,
	de.to_date 
FROM departments d JOIN dept_emp de ON d.dept_no = de.dept_no;


SELECT
	de.emp_no,
	de.dept_no,
	de.from_date,
	de.to_date
FROM dept_emp de JOIN departments d ON de.dept_no = d.dept_no JOIN employees e ON de.emp_no = e.emp_no
WHERE de.emp_no
IN (SELECT de.emp_no FROM dept_emp de GROUP BY emp_no HAVING COUNT(de.emp_no) > 1)
ORDER BY emp_no, from_date;








