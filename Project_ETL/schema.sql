-- Grain of fact_weather: One record per observed timestamp per location (hourly weather measurement).

CREATE SCHEMA IF NOT EXISTS weather;

CREATE TABLE IF NOT EXISTS weather.dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    year INT NOT NULL,
    month INT NOT NULL,
    day INT NOT NULL
);

CREATE TABLE IF NOT EXISTS weather.dim_hour (
    hour_id INT PRIMARY KEY,
    part_of_day VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS weather.fact_weather (
    observed_at TIMESTAMP PRIMARY KEY,
    date_id INT NOT NULL REFERENCES weather.dim_date(date_id),
    hour_id INT NOT NULL REFERENCES weather.dim_hour(hour_id),
    temperature_c NUMERIC(5, 2) NOT NULL,
    humidity_pct NUMERIC(5, 2) NOT NULL
);

SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'weather';


select * from dim_date;

select * from weather.dim_hour;

select * from weather.fact_weather;


 SELECT COUNT(*) FROM weather.fact_weather; --168

SELECT COUNT(*) FROM weather.dim_date;  -- 7
SELECT COUNT(*) FROM weather.dim_hour; --24


   SELECT h.part_of_day, ROUND(AVG(f.temperature_c)::numeric, 1) AS avg_temp
   FROM weather.fact_weather f
   JOIN weather.dim_hour h ON f.hour_id = h.hour_id
   GROUP BY h.part_of_day
   ORDER BY avg_temp DESC;
