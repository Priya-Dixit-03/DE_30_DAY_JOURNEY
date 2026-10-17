import os
import sys
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text
from transform import transform_data
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL")

load_dotenv(Path(__file__).resolve().parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
import os
print("DATABASE_URL set:", os.getenv("DATABASE_URL") is not None)
print(".env exists:", (Path(__file__).resolve().parent / ".env").exists())

if not DATABASE_URL:
    print("Error: DATABASE_URL not found in environment variables.", file=sys.stderr)
    sys.exit(1)


def get_part_of_day(hour):
    """Categorizes an hour (0-23) into a part of day."""
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"


def load_data():
    try:
        # 1. Fetch the transformed DataFrame
        df = transform_data()
        
        # 2. Establish SQLAlchemy engine
        engine = create_engine(DATABASE_URL)
        
        # 3. Prepare dimension data
        # dim_date rows
        dates_df = df[["obs_date"]].drop_duplicates().copy()
        dates_df["date_id"] = pd.to_datetime(dates_df["obs_date"]).dt.strftime("%Y%m%d").astype(int)
        dates_df["year"] = pd.to_datetime(dates_df["obs_date"]).dt.year
        dates_df["month"] = pd.to_datetime(dates_df["obs_date"]).dt.month
        dates_df["day"] = pd.to_datetime(dates_df["obs_date"]).dt.day
        
        # dim_hour rows (0 to 23)
        hours_data = [{"hour_id": h, "part_of_day": get_part_of_day(h)} for h in range(24)]
        hours_df = pd.DataFrame(hours_data)
        
        # Map date_id and hour_id back onto the main dataframe for the fact table
        df["date_id"] = pd.to_datetime(df["obs_date"]).dt.strftime("%Y%m%d").astype(int)
        df["hour_id"] = df["obs_hour"]
        
        facts_df = df[[
            "observed_at", "date_id", "hour_id", "temperature_c", "humidity_pct"
        ]].copy()
        
        # 4. Insert data into database idempotently using explicit SQL upserts
        with engine.begin() as conn:
            # Insert into dim_date (ON CONFLICT DO NOTHING)
            for _, row in dates_df.iterrows():
                conn.execute(
                    text("""
                        INSERT INTO weather.dim_date (date_id, full_date, year, month, day)
                        VALUES (:date_id, :full_date, :year, :month, :day)
                        ON CONFLICT (date_id) DO NOTHING;
                    """),
                    {
                        "date_id": row["date_id"],
                        "full_date": str(row["obs_date"]),
                        "year": int(row["year"]),
                        "month": int(row["month"]),
                        "day": int(row["day"])
                    }
                )
            
            # Insert into dim_hour (ON CONFLICT DO NOTHING)
            for _, row in hours_df.iterrows():
                conn.execute(
                    text("""
                        INSERT INTO weather.dim_hour (hour_id, part_of_day)
                        VALUES (:hour_id, :part_of_day)
                        ON CONFLICT (hour_id) DO NOTHING;
                    """),
                    {
                        "hour_id": int(row["hour_id"]),
                        "part_of_day": row["part_of_day"]
                    }
                )
            
            # Insert into fact_weather (Idempotent UPSERT on observed_at)
            loaded_count = 0
            for _, row in facts_df.iterrows():
                conn.execute(
                    text("""
                        INSERT INTO weather.fact_weather 
                            (observed_at, date_id, hour_id, temperature_c, humidity_pct)
                        VALUES 
                            (:observed_at, :date_id, :hour_id, :temperature_c, :humidity_pct)
                        ON CONFLICT (observed_at) DO UPDATE SET
                            temperature_c = EXCLUDED.temperature_c,
                            humidity_pct = EXCLUDED.humidity_pct;
                    """),
                    {
                        "observed_at": row["observed_at"],
                        "date_id": int(row["date_id"]),
                        "hour_id": int(row["hour_id"]),
                        "temperature_c": float(row["temperature_c"]),
                        "humidity_pct": float(row["humidity_pct"])
                    }
                )
                loaded_count += 1
                
        print(f"Successfully loaded/upserted {loaded_count} records into fact_weather.")

    except Exception as e:
        print(f"Error occurred during data loading: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    load_data()