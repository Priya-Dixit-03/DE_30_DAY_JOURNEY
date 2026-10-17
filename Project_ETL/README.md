Project 1: Weather ETL Pipeline
Summary
This project is an automated ETL (Extract, Transform, Load) pipeline designed to fetch weather data from an API, clean and process it locally, and load it into a cloud-hosted PostgreSQL database (Neon) using a star schema. The pipeline ensures data reliability by validating records before insertion and maintaining idempotency so that repeated runs do not create duplicate entries. It automates data flow from raw ingestion to analytics-ready tables suitable for reporting and querying.

Architecture Diagram
Plaintext
 [ Weather API ]
        │
        ▼ (Extract)
   [ raw/ data ]
        │
        ▼ (Transform)
  [ clean/ data ]
        │
        ▼ (Load & Validate)
 [ Neon PostgreSQL (Star Schema) ]
   ├── dim_date
   ├── dim_location
   └── fact_weather
Database Schema & Grain
The database uses a star schema comprising three main tables:

dim_date: Stores unique date and time attributes.

dim_location: Stores geographic and location-specific details.

fact_weather: Stores quantitative weather metrics (e.g., temperature, humidity) tied to foreign keys from the dimension tables.

Grain of fact_weather: Each row represents a single weather measurement observation for a specific location at a specific date and time.

How to Run It
1. Prerequisites & Installation
Ensure you have Python installed, then install the required packages:

Bash
pip install requests python-dotenv psycopg2-binary pandas
2. Configure Environment Variables
Create a .env file in your project root directory. Use the following fake example format with your actual Neon credentials:

Code snippet
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
3. Initialize the Database
Run the schema.sql script in your PostgreSQL client (like DBeaver or via command line) to create the necessary tables and schema.

4. Execute the Pipeline
Run the load script to process and load the data:

Bash
python load.py
Key Design Decisions
Idempotent Loading: The load script is designed to handle duplicate executions safely (e.g., checking for existing records before inserting). Running load.py multiple times will consistently yield the same row count (168 records in fact_weather) rather than multiplying duplicates.

Validation Before Loading: Data types, missing values, and constraints are checked prior to database insertion. This prevents corrupt or malformed data from polluting the data warehouse.

Fail-Fast with sys.exit(1): Critical errors (such as missing environment variables, connection failures, or failed validations) immediately halt execution using sys.exit(1) with a clean, concise error message, avoiding unhandled tracebacks or password leaks.

Results & Analysis
Part of the Day Temperature Analysis
Querying the average temperature grouped by different parts of the day yielded the following output:
