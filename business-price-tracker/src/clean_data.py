import pandas as pd
from pathlib import Path

def load_raw_data(file_path):
    df = pd.read_csv(file_path)
    print(f"Loaded {len(df)} rows from {file_path}")
    return df

def clean_data(df):
    # Drop duplicates
    df = df.drop_duplicates()

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    return df

if __name__ == "__main__":
    raw_path = Path("data/raw/raw_data.csv")
    df = load_raw_data(raw_path)
    clean_df = clean_data(df)
    clean_df.to_csv("data/cleaned/cleaned_data.csv", index=False)
    print("✅ Cleaned data saved!")
