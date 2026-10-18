# Project 1: Weather ETL Pipeline  

 # Summary   
 This project is an automated ETL (Extract, Transform, Load) pipeline designed to fetch weather data from an API, clean and process it locally, and load it into a cloud-hosted PostgreSQL database (Neon) using a star schema. The pipeline ensures data reliability by validating records during transformation prior to database insertion, and maintains idempotency using upserts to prevent duplicate entries on repeated runs. It automates the data flow from raw ingestion to analytics-ready tables suitable for reporting and querying.  

# Architecture Diagram
Plaintext 
[ Weather API ]
        │
        ▼ (Extract)
   [ raw/ data ]
        │
        ▼ (Transform & Validate)
  [ clean/ data ]
        │
        ▼ (Load)
 [ Neon PostgreSQL (Star Schema) ]
   ├── dim_date
   ├── dim_hour
   └── fact_weather

# Database Schema & Grain
The database uses a star schema comprising three main tables:
dim_date: Stores unique date attributes.
dim_hour: Stores hour definitions and part-of-day categories. (Note: Parts of the day are defined as Morning: 05:00 - 11:59, Afternoon: 12:00 - 16:59, Evening: 17:00 - 20:59, and Night: 21:00 - 04:59).
fact_weather: Stores quantitative weather metrics (e.g., forecast temperature, humidity) tied via foreign keys to the dimension tables.
Grain of fact_weather: Each row represents a single hourly forecast observation for a specific location (Indore), keyed by the observation timestamp.

# How to Run It
1. Prerequisites & InstallationEnsure you have Python installed, then install the required packages:
pip install requests python-dotenv psycopg2-binary pandas sqlalchemy
2. Configure Environment VariablesCreate a .env file inside your Project_ETL/ directory next to your scripts. Use the following fake example format with your actual Neon credentials:
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
3. Initialize the DatabaseFirst, run the schema.sql script in your PostgreSQL client (or via command line) to create the necessary tables and schema.
4. Execute the PipelineAfter initializing the schema, run the load script to process and load the data:
python load.py

# Key Design Decisions
Idempotent Loading via Upserts: The load script uses SQL ON CONFLICT upsert logic rather than manual pre-checks. Re-running load.py on the same day maintains a stable row count (168 records in fact_weather), while running it on a new day safely appends new forecast rows.
Validation Before Loading: Data types, missing values, and business constraints are thoroughly checked in transform.py prior to database insertion. This stops corrupt or malformed data before it reaches the data warehouse.
Fail-Fast with sys.exit(1): Critical errors (such as missing environment variables, connection failures, or validation failures) immediately halt execution using sys.exit(1) with a clean, concise error message, avoiding unhandled tracebacks or sensitive credential leakage.

# Results & Analysis
Part of the Day Forecast Temperature Analysis
Querying the average forecast temperature grouped by different parts of the day (defined via dim_hour) yielded the following output:

```SELECT h.part_of_day, 
ROUND(AVG(f.temperature_c)::numeric, 1) AS avg_forecast_temp
FROM weather.fact_weather f
JOIN weather.dim_hour h 
ON f.hour_id = h.hour_id
GROUP BY h.part_of_day
ORDER BY avg_forecast_temp DESC;```

| Part of day | Avg forecast temp (°C) |
|---|---|
| Afternoon | 30.2 |
| Evening | 26.6 |
| Morning | 26.0 |
| Night | 23.8 |