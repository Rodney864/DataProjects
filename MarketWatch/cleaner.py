from ingestion import fetch_data
import pandas as pd

def clean_data(df):
    df = df.copy()
    df =df.dropna()
    return df


if __name__ == "__main__":
    df = fetch_data("AAPL")  
    cleaned = clean_data(df)  
    print(cleaned.head())