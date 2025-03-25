import yfinance as yf
import sqlite3
import json
import time

class StockDatabase:
    """Class to manage stock tickers organized by sector using SQLite."""
    def __init__(self, db_file="stock_sectors.db"):
        self.db_file = db_file

    def get_tickers(self, sector):
        """Return tickers for the specified sector from the SQLite database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT ticker FROM stocks WHERE sector = ?", (sector,))
        tickers = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tickers

def run_stock_screener(json_file_path, db_file="stock_sectors.db"):
    """
    Run the stock screener on stocks within the user-specified sector.

    Args:
        json_file_path (str): Path to the JSON file with user preferences.
        db_file (str): Path to the SQLite database file.

    Returns:
        str or None: Recommended stock ticker or None if no match.
    """
    # Load user preferences
    try:
        with open(json_file_path, "r") as f:
            user_prefs = json.load(f)
    except FileNotFoundError:
        print("Error: user_preferences.json not found.")
        return None

    # Initialize stock database
    db = StockDatabase(db_file)

    # Get tickers for the specified sector
    tickers = db.get_tickers(user_prefs["sector"])

    if not tickers:
        print(f"No stocks found for sector: {user_prefs['sector']}")
        return None

    # Filter and score stocks within the sector
    selected_stock = None
    best_score = -1

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Extract dynamic stock metrics
            beta = info.get("beta", 1.0)
            price = info.get("currentPrice", 0.0)
            dividend_yield = info.get("dividendYield", 0.0)

            # Scoring based on user preferences
            score = 0
            if user_prefs["risk_tolerance"] == "Aggressive" and beta > 1:
                score += 1
            elif user_prefs["risk_tolerance"] == "Conservative" and beta < 1:
                score += 1
            if user_prefs["money_total"] >= price:
                score += 2
            if user_prefs["goal"] == "Diversification of Income" and dividend_yield > 0:
                score += 2

            if score > best_score:
                best_score = score
                selected_stock = ticker

            time.sleep(0.75)  # Respect API rate limits
        except Exception as e:
            print(f"Error processing ticker {ticker}: {e}")
            continue

    return selected_stock

# For standalone testing
if __name__ == "__main__":
    result = run_stock_screener("user_preferences.json")
    if result:
        print(f"Best stock recommendation: {result}")
    else:
        print("No suitable stock found.")