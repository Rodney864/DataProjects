from ingestion import fetch_data
import pandas as pd

def clean_data(df):
    df = df.copy()
    essential = ["Open", "High", "Low", "Close", "Volume"]
    cols = [c for c in essential if c in df.columns]
    df = df.dropna(subset=cols)
    return df

if __name__ == "__main__":
    df = fetch_data("AAPL")  
    cleaned = clean_data(df)  
    print(cleaned.head())