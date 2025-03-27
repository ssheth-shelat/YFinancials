import yfinance as yf
import sqlite3
import json
import time
from concurrent.futures import ThreadPoolExecutor

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
    

def fetch_stock_data(ticker):
    """Fetch stock data for a single ticker."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "ticker": ticker,
            "beta": info.get("beta", 1.0),
            "price": info.get("currentPrice", 0.0),
            "div_yield": info.get("dividendYield", 0.0) * 100,
            "market_cap": info.get("marketCap", 0),
            "peg": info.get("pegRatio", float("inf")),
            "ev_rev": info.get("enterpriseToRevenue", float("inf")),
            "ev_ebitda": info.get("enterpriseToEbitda", float("inf")),
            "debt_equity": info.get("debtToEquity", 0.0),
            "roe": info.get("returnOnEquity", 0.0) * 100,
            "sector": info.get("sector", "")
        }
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None

def run_stock_screener(json_file_path, db_file="stock_sectors.db"):
    """
    Run the stock screener using the provided SQLite database, avoiding rate limits.

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

    # Fetch data in batches to avoid rate limits
    stock_data = []
    batch_size = 5  # Process 20 tickers at a time
    for i in range(0, len(tickers), batch_size):
        batch = tickers[i:i + batch_size]
        with ThreadPoolExecutor(max_workers=5) as executor:
            batch_data = list(filter(None, executor.map(fetch_stock_data, batch)))
        stock_data.extend(batch_data)
        if i + batch_size < len(tickers):  # Delay between batches
            time.sleep(2)  # 1-second delay between batches

    if not stock_data:
        print("No valid stock data retrieved.")
        return None

    # Score stocks
    selected_stock = None
    best_score = -1

    for data in stock_data:
        score = 0

        # Point in Career
        if user_prefs.get("career") == "Beginning":
            if data["beta"] > 1.2: score += 2
            if data["peg"] < 1.5: score += 2
            if data["roe"] > 15: score += 2
        elif user_prefs.get("career") == "Middle":
            if 0.8 < data["beta"] < 1.5: score += 1
            if data ["peg"] < 2: score += 1
            if data["roe"] > 10: score += 1
            if data["debt_equity"] < 1: score += 1
        elif user_prefs.get("career") == "Nearing Retirement":
            if data["beta"] < 1: score += 2
            if data["div_yield"] > 2: score += 2
            if data["debt_equity"] < 0.5: score += 2
        elif user_prefs.get("career") == "Retired":
            if data["beta"] < 0.8: score += 3
            if data["div_yield"] > 3: score += 3
            if data["debt_equity"] < 0.3: score += 3

        # Risk Tolerance
        if user_prefs["risk_tolerance"] == "Aggressive":
            if data["beta"] > 1.2: score += 2
            if data["peg"] < 1.5: score += 1
            if data["roe"] > 15: score += 1
            if data["debt_equity"] < 2: score += 1
        elif user_prefs["risk_tolerance"] == "Moderate":
            if 0.8 <= data["beta"] <= 1.2: score += 2
            if 1 <= data["peg"] <= 2: score += 1
            if 10 <= data["roe"] <= 15: score += 1
            if data["debt_equity"] < 1: score += 1
        elif user_prefs["risk_tolerance"] == "Conservative":
            if data["beta"] < 0.8: score += 2
            if data["div_yield"] > 2: score += 2
            if data["debt_equity"] < 0.5: score += 2

        # Goal
        if user_prefs["goal"] == "Exponential Growth":
            if data["peg"] < 1.5: score += 2
            if data["roe"] > 15: score += 2
            if data["beta"] > 1: score += 1
            if data["ev_rev"] < 3: score += 1
        elif user_prefs["goal"] == "Beat Inflation":
            if data["div_yield"] > 2: score += 1
            if data["roe"] > 10: score += 1
            if data["peg"] < 2: score += 1
            if data["market_cap"] > 10e9: score += 1
        elif user_prefs["goal"] == "Diversification of Income":
            if data["div_yield"] > 3: score += 3
            if data["debt_equity"] < 1: score += 1
            if data["ev_ebitda"] < 10: score += 1

        # Time to Keep Stock
        if user_prefs.get("time") == "Less than 1 year":
            if data["beta"] > 1: score += 1
            if data["peg"] < 1: score += 1
            if data["market_cap"] < 10e9: score += 1
        elif user_prefs.get("time") == "1 Year":
            if 0.8 <= data["beta"] <= 1.2: score += 1
            if data["peg"] < 1.5: score += 1
            if data["roe"] > 10: score += 1
        elif user_prefs.get("time") == "2 Years":
            if data["beta"] < 1.2: score += 1
            if data["peg"] < 2: score += 1
            if data["market_cap"] > 5e9: score += 1
        elif user_prefs.get("time") == "3+ Years":
            if data["div_yield"] > 2: score += 1
            if data["debt_equity"] < 1: score += 1
            if data["roe"] > 10: score += 1
            if data["market_cap"] > 10e9: score += 1
        elif user_prefs.get("time") == "Until % Growth Achieved":
            if data["peg"] < 1.5: score += 2
            if data["roe"] > 15: score += 2
            if data["ev_rev"] < 3: score += 1

        # Budget Check
        total_invest = user_prefs.get("total_invest", 0)
        multiple_shares = user_prefs.get("multiple_shares", 0)
        if data["price"] <= total_invest: score += 2
        shares = multiple_shares // data["price"] if data["price"] > 0 else 0
        if shares * data["price"] <= total_invest: score += 2

        # Sector Match
        if data["sector"] == user_prefs["sector"]: score += 5

        if score > best_score:
            best_score = score
            selected_stock = data["ticker"]

    return selected_stock

# For standalone testing
if __name__ == "__main__":
    result = run_stock_screener("user_preferences.json", "stock_sectors.db")
    if result:
        start_time = time.time()
        print(f"Best stock recommendation: {result}")
        print(f"Execution time: {time.time() - start_time:.2f} seconds")
    else:
        print("No suitable stock found.")