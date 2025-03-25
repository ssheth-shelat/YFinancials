import sqlite3

# Connect to the database
conn = sqlite3.connect("stock_sectors.db")
cursor = conn.cursor()

# Get total number of entries
cursor.execute("SELECT COUNT(*) FROM stocks")
total = cursor.fetchone()[0]
print(f"Total entries: {total}")

# Get all distinct sectors
cursor.execute("SELECT DISTINCT sector FROM stocks")
sectors = [row[0] for row in cursor.fetchall()]
print(f"Found {len(sectors)} sectors: {sectors}\n")

# View all entries, grouped by sector
print("All entries (ticker, sector):")
for sector in sectors:
    cursor.execute("SELECT ticker FROM stocks WHERE sector = ?", (sector,))
    tickers = [row[0] for row in cursor.fetchall()]
    print(f"Sector: {sector} ({len(tickers)} tickers)")
    for ticker in tickers:
        print(f"  {ticker} - {sector}")
    print()  # Blank line between sectors

# Close the connection
conn.close()