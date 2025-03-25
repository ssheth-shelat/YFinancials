import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect("stock_sectors.db")
cursor = conn.cursor()

# Create or recreate the stocks table
cursor.execute("DROP TABLE IF EXISTS stocks")
cursor.execute("""
    CREATE TABLE stocks (
        ticker TEXT PRIMARY KEY,
        sector TEXT NOT NULL
    )
""")

# Read the Excel file
xl = pd.ExcelFile("stock_sectors.xlsx")
print(f"Found sheets: {xl.sheet_names}")

# Import tickers from each sheet
for sector in xl.sheet_names:
    df = pd.read_excel(xl, sheet_name=sector)
    tickers = df["Symbol"].tolist()  # Assumes column header is "Ticker"
    if not tickers:
        print(f"No tickers found in '{sector}'")
        continue
    for ticker in tickers:
        cursor.execute("INSERT OR IGNORE INTO stocks (ticker, sector) VALUES (?, ?)", (ticker, sector))
    print(f"Imported {len(tickers)} tickers into sector '{sector}'")

# Commit and close
conn.commit()
conn.close()
print("Created stock_sectors.db from stock_sectors.xlsx")