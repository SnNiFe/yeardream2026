-- 트랜잭션 : 쪼갤수없는 논리적 업무 단위
-- 실제로는 여러 단계이지만 한단계로 가정하는 것
-- 송금은 출금과 입금 두단계 이지만, 둘중 하나라도 실패 하면 송금은 취소된다.
-- 이때 작업을 확정 하는것을 commit
-- 작업을 취소하는 것을 rollback
-- SQL 에선 무조건 commit 을 해야 작업이 확정 된다.(그런데 한번도 한적이 없다?)

-- 1) AUTOCOMMIT 이 설정되어있어서 이다.
SELECT @@AUTOCOMMIT; -- 1: 설정 / 0: 미설정

-- 2) AUTOCOMMIT 변경
SET @@AUTOCOMMIT = 0;

COMMIT; -- 지금까지의 상태를 저장
DELETE FROM employees;
ROLLBACK; -- 이전 상태로 되돌리기
SELECT * FROM employees e;