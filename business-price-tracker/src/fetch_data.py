import requests
import json
import pandas as pd
from utils import log_info, log_error
import os
import time

def fetch_api_data():
    url = os.getenv("DATA_SOURCE_URL")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # throws error for bad status
        data = response.json()
        log_info(f"Fetched {len(data)} items from API.")
        return data
    except requests.RequestException as e:
        log_error(f"Error fetching data: {e}")
        return None
    
def fetch_with_retry(retries=3, delay=5):
    for attempt in range(1, retries + 1):
        log_info(f"Starting attempt: {attempt}")
        data = fetch_api_data()
        if data:
            log_info(f"Succeeded attempt: {attempt}")
            return data
        log_error(f"Failed attempt: {attempt}")
        sleep_time = max(delay * attempt, 1)
        time.sleep(sleep_time)

    log_error(f"Failed all {retries} attempts")
    return None

def save_json(data):
    """Save fetched data as JSON file."""
    if data:
        path = os.getenv("RAW_DATA_PATH")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        log_info(f"Saved raw data to {path}")

def save_csv(data):
    """Save fetched data as CSV file."""
    if data:
        path = os.getenv("RAW_DATA_CSV_PATH", "data/raw/raw_data.csv")
        try:
            df = pd.DataFrame(data)
            df.to_csv(path, index=False, encoding="utf-8")
            log_info(f"Saved raw data to {path}")
        except Exception as e:
            log_error(f"Error saving CSV: {e}")

if __name__ == "__main__":
    data = fetch_with_retry(retries=2, delay=10)
    save_csv(data)
