select name, salary,
dense_rank() over (partition by dept_id order by salary desc) as rnk
from employees;


with High_sal as(
select name, dept_id, salary, 
dense_rank() over (order by salary desc) rnk
from employees)
select name, dept_id, salary from High_sal
where rnk = 2;


with High_sal as(
select name, dept_id, salary,
dense_rank() over (partition by dept_id order by salary desc) rnk
from employees)
select name, dept_id, salary from High_sal
where rnk = 1;

select name, salary,
row_number() over (order by salary desc)  as rnk 
from employees; 


select name, salary,
rank() over (order by salary desc)  as rnk 
from employees; 


select name, salary,
dense_rank() over (order by salary desc)  as rnk 
from employees; 


select name, salary, hire_date,
LAG(name) over (order by hire_date) as prev_name,
salary - LAG(salary) over(order by hire_date) as salary_diff
from employees;
