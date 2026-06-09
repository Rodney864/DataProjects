from ingestion import fetch_data
import pandas as pd

def clean_data(df):
    df =df.dropna()
    print(df.index)
    return df


if __name__ == "__main__":
    df = fetch_data("AAPL")  # get the data
    cleaned = clean_data(df)  # pass it to your cleaner
    print(cleaned.head())