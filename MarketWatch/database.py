import sqlite3
import pandas as pd

DB_PATH = "market_data.db"


def get_connection(db_path: str = DB_PATH):
    return sqlite3.connect(db_path)


def save_data(df: pd.DataFrame, db_path: str = DB_PATH, table: str = "prices"):
    """Write the tidy DataFrame to a SQLite table."""
    df = df.copy()
    # SQLite has no native datetime — store dates as text (ISO format)
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")

    with get_connection(db_path) as conn:
        df.to_sql(table, conn, if_exists="replace", index=False)
        # Index speeds up ticker/date lookups — good habit to show
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_ticker ON {table}(ticker)")
    print(f"Saved {len(df)} rows to '{table}' in {db_path}")


def load_data(tickers=None, db_path: str = DB_PATH, table: str = "prices") -> pd.DataFrame:
    """Query data back out, optionally filtered by ticker."""
    with get_connection(db_path) as conn:
        if tickers:
            placeholders = ",".join("?" for _ in tickers)
            query = f"SELECT * FROM {table} WHERE ticker IN ({placeholders})"
            df = pd.read_sql_query(query, conn, params=tickers)
        else:
            df = pd.read_sql_query(f"SELECT * FROM {table}", conn)

    df["Date"] = pd.to_datetime(df["Date"])
    return df


def query(sql: str, db_path: str = DB_PATH, params=None) -> pd.DataFrame:
    """Run an arbitrary SQL query — handy for analysis."""
    with get_connection(db_path) as conn:
        return pd.read_sql_query(sql, conn, params=params)


if __name__ == "__main__":
    # Quick demo
    from ingestion import fetch_many
    from cleaner import clean_data

    df = fetch_many(["AAPL", "MSFT", "SPY"])
    df = clean_data(df)
    save_data(df)

    loaded = load_data(["AAPL", "MSFT"])
    print(loaded.head())
    print(loaded["ticker"].value_counts())