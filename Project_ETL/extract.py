from datetime import date
import json
import os
import sys
import requests


def extract_weather():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 22.7,
        "longitude": 75.8,
        "hourly": "temperature_2m,relative_humidity_2m",
        "timezone": "auto",
    }
    
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred during weather extraction: {e}")
        sys.exit(1)


if __name__ == "__main__":
    data = extract_weather()
    
    os.makedirs("raw", exist_ok=True)
    name = f"raw/weather_{date.today()}.json"
    
    with open(name, "w") as f:
        json.dump(data, f)
        
    print(len(data["hourly"]["time"]))



# import requests
# import json, os
# from datetime import date


# url ="https://api.open-meteo.com/v1/forecast"

# r = requests.get(url, params={
#     "latitude": 22.7,
#     "longitude": 75.8,
#     "hourly": "temperature_2m,relative_humidity_2m",
#     "timezone": "auto",
# }, timeout=10)
# print(r.url)
# r.raise_for_status()
# data = r.json()


# os.makedirs("raw", exist_ok=True)
# with open("raw/weather.json", "w") as f:
#     json.dump(data, f)
    
# name = f"raw/weather_{date.today()}.json"
# print(data.keys())
# print(name)


