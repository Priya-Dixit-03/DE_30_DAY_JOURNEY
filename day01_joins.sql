CREATE SCHEMA IF NOT EXISTS de_practice;
SET search_path TO de_practice;



CREATE TABLE departments (dept_id INT PRIMARY KEY, dept_name VARCHAR(50));
CREATE TABLE employees (
    emp_id INT PRIMARY KEY, name VARCHAR(50),
    dept_id INT, salary INT, manager_id INT, hire_date DATE
);

INSERT INTO departments VALUES (1,'Engineering'),(2,'Sales'),(3,'HR'),(4,'Finance');
INSERT INTO employees VALUES
(1,'Amit',1,90000,NULL,'2020-01-15'),
(2,'Priya',1,75000,1,'2021-03-10'),
(3,'Rahul',2,60000,1,'2021-07-01'),
(4,'Sneha',2,60000,3,'2022-02-20'),
(5,'Rohan',3,50000,1,'2022-08-12'),
(6,'Neha',1,82000,1,'2023-01-05'),
(7,'Vikram',NULL,45000,3,'2023-06-18');



select * from departments;


select * from employees;


select e.name, d.dept_name from departments d
inner join employees e
on d.dept_id = e.dept_id;

select * from employees e
left join departments d
on d.dept_id = e.dept_id;

select d.dept_name from departments d
left join employees e
on d.dept_id = e.dept_id;


select * from departments  d
left join  employees e 
on d.dept_id = e.dept_id
where e.dept_id is null;


select e.name as employee, m.name as Manager from employees e
left join employees m
on e.manager_id = m.emp_id


   SELECT d.dept_name, AVG(e.salary) AS avg_salary
   FROM de_practice.departments d
   JOIN employees e ON d.dept_id = e.dept_id
   GROUP BY d.dept_name
HAVING AVG(e.salary) > 60000;




