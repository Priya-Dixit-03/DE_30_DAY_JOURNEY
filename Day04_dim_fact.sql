
-- Create Dimension: Products
CREATE TABLE dim_product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL
);

-- Create Dimension: Customers
CREATE TABLE dim_customer (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL
);

-- Create Dimension: Dates
CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE NOT NULL,
    month VARCHAR(10) NOT NULL,
    year INT NOT NULL
);

-- Create Fact Table: Sales
CREATE TABLE fact_sales (
    sale_id INT PRIMARY KEY,
    date_id INT REFERENCES dim_date(date_id),
    customer_id INT REFERENCES dim_customer(customer_id),
    product_id INT REFERENCES dim_product(product_id),
    quantity INT NOT NULL,
    amount NUMERIC(10, 2) NOT NULL
);

-- Insert data into dim_product
INSERT INTO dim_product (product_id, product_name, category) VALUES
(1, 'Laptop', 'Electronics'),
(2, 'Phone', 'Electronics'),
(3, 'Desk', 'Furniture'),
(4, 'Chair', 'Furniture');

-- Insert data into dim_customer
INSERT INTO dim_customer (customer_id, customer_name, city) VALUES
(1, 'Amit', 'Indore'),
(2, 'Priya', 'Pune'),
(3, 'Rahul', 'Indore');

-- Insert data into dim_date
INSERT INTO dim_date (date_id, full_date, month, year) VALUES
(1, '2026-01-10', 'Jan', 2026),
(2, '2026-01-20', 'Jan', 2026),
(3, '2026-02-05', 'Feb', 2026);

-- Insert data into fact_sales
INSERT INTO fact_sales (sale_id, date_id, customer_id, product_id, quantity, amount) VALUES
(1, 1, 1, 1, 5, 50000),
(2, 1, 2, 3, 1, 8000),
(3, 2, 3, 2, 2, 40000),
(4, 2, 1, 4, 1, 6000),
(5, 3, 2, 1, 1, 50000),
(6, 3, 3, 3, 2, 16000);

--Total revenue per category.
select p.category, SUM(s.amount) as total_rev
from fact_sales s
join dim_product p
on s.product_id  = p.product_id 
group by p.category ;


--Total revenue per city.
select c.city, SUM(s.amount) as total_revenue
from fact_sales s
join dim_customer c 
on s.customer_id  = c.customer_id 
group by c.city;


--Total revenue per Month.
SELECT 
    d.year,
    d.month, 
    SUM(s.amount) AS total_revenue
FROM fact_sales s
JOIN dim_date d ON s.date_id = d.date_id
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

--top customer by revenue
WITH RankedCustomers AS (
    SELECT 
        c.customer_name, 
        SUM(s.amount) AS total_revenue,
        DENSE_RANK() OVER (ORDER BY SUM(s.amount) DESC) AS rnk
    FROM fact_sales s
    JOIN dim_customer c ON s.customer_id = c.customer_id
    GROUP BY c.customer_id, c.customer_name
)
SELECT customer_name, total_revenue
FROM RankedCustomers
WHERE rnk = 1;



-- Drop old tables if they exist
DROP TABLE IF EXISTS fact_sales CASCADE;
DROP TABLE IF EXISTS dim_customer CASCADE;

-- 1. Create SCD Type 2 Customer Dimension Table
CREATE TABLE dim_customer (
    customer_sk INT PRIMARY KEY,          -- Surrogate Key (Unique per version)
    customer_id INT NOT NULL,             -- Natural Key (Remains constant for the person)
    customer_name VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_current BOOLEAN NOT NULL
);

-- 2. Create Fact Sales Table referencing the Surrogate Key
CREATE TABLE fact_sales (
    sale_id INT PRIMARY KEY,
    date_id INT NOT NULL,
    customer_sk INT REFERENCES dim_customer(customer_sk), -- Points to the version active at the time of sale
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    amount NUMERIC(10, 2) NOT NULL
);

-- Insert customer versions (Notice Priya has two records: one for Pune, one for Indore)
INSERT INTO dim_customer (customer_sk, customer_id, customer_name, city, start_date, end_date, is_current) VALUES
(1, 1, 'Amit', 'Indore', '2026-01-01', '9999-12-31', TRUE),
(2, 2, 'Priya', 'Pune', '2026-01-01', '2026-02-28', FALSE),   -- Old version (Pune)
(3, 2, 'Priya', 'Indore', '2026-03-01', '9999-12-31', TRUE), -- New version (Indore)
(4, 3, 'Rahul', 'Indore', '2026-01-01', '9999-12-31', TRUE);

-- Insert sales (Sale 3 points to Priya's Pune SK, Sale 7 points to Priya's new Indore SK)
INSERT INTO fact_sales (sale_id, date_id, customer_sk, product_id, quantity, amount) VALUES
(3, 2, 2, 2, 2, 40000),  -- Sale 3: Happened Feb 2026, linked to Priya's Pune record (customer_sk = 2)
(7, 3, 3, 1, 1, 50000);  -- Sale 7: Happened April 2026, linked to Priya's Indore record (customer_sk = 3)




SELECT 
    c.city, 
    SUM(s.amount) AS total_revenue
FROM fact_sales s
JOIN dim_customer c ON s.customer_sk = c.customer_sk
GROUP BY c.city
ORDER BY total_revenue DESC;
