SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

SELECT name
FROM employees
WHERE dept_id in
(SELECT dept_id FROM departments
WHERE dept_name = 'Sales');

-- get 0 rows
SELECT dept_name FROM departments
WHERE dept_id NOT in
(SELECT dept_id FROM employees);


SELECT name, salary,
       CASE WHEN salary >= 80000 THEN 'High'
            WHEN salary >= 60000 THEN 'Mid'
            ELSE 'Low' END AS band
FROM employees;


SELECT e.name, COALESCE(d.dept_name, 'Unassigned') AS dept
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.dept_id;


SELECT name, hire_date,
       EXTRACT(YEAR FROM hire_date) AS hire_year,
       CURRENT_DATE - hire_date AS days_since_hire
FROM employees;