import os
import pandas as pd
from extract import extract_weather


def transform_data():
    # 1. Fetch raw weather data using your extract script
    raw_data = extract_weather()
    h = raw_data["hourly"]
    
    # 2. Build the initial DataFrame from the 3 parallel lists
    df = pd.DataFrame({
        "time": h["time"],
        "temperature_2m": h["temperature_2m"],
        "relative_humidity_2m": h["relative_humidity_2m"]
    })
    
    # 3. Convert time to real datetime and rename columns
    df["time"] = pd.to_datetime(df["time"])
    df = df.rename(columns={
        "time": "observed_at",
        "temperature_2m": "temperature_c",
        "relative_humidity_2m": "humidity_pct"
    })
    
    # 4. Extract date and hour parts using the .dt accessor
    df["obs_date"] = df["observed_at"].dt.date
    df["obs_hour"] = df["observed_at"].dt.hour
    
    # 5. Validation checks to halt execution if data is malformed
    assert len(df) == 168, f"Expected 168 rows, got {len(df)}"
    assert df["observed_at"].is_unique, "Duplicate timestamps found in data!"
    assert df.isna().sum().sum() == 0, "NULL values detected in the dataset!"
    assert df["humidity_pct"].between(0, 100).all(), "Humidity values out of valid 0-100 range!"
    
    # 6. Save clean data to CSV using a script-relative path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    clean_dir = os.path.join(script_dir, "clean")
    os.makedirs(clean_dir, exist_ok=True)
    
    output_path = os.path.join(clean_dir, "weather_clean.csv")
    df.to_csv(output_path, index=False)
    
    print(f"Transformation successful! Cleaned data saved to {output_path}")
    print(df.head())


if __name__ == "__main__":
    transform_data()