from database import query

# Average closing price per ticker
print(query("""
    SELECT ticker,
           ROUND(AVG(Close), 2) AS avg_close,
           ROUND(MAX(Close), 2) AS high,
           ROUND(MIN(Close), 2) AS low,
           COUNT(*) AS trading_days
    FROM prices
    GROUP BY ticker
    ORDER BY avg_close DESC
"""))

# Highest single-day closing price across all stocks
print(query("""
    SELECT ticker, Date, Close
    FROM prices
    ORDER BY Close DESC
    LIMIT 5
"""))