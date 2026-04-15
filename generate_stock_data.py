import os
import random
import pandas as pd

# =========================
# Config
# =========================
OUTPUT_DIR = "data"

TICKER_BASE_PRICE = {
    "AAPL": 180,
    "MSFT": 370,
    "NVDA": 500,
    "GOOGL": 140,
    "META": 350,
    "DIS": 90,
    "NFLX": 490,
    "VZ": 37,
    "AMZN": 150,
    "TSLA": 240,
    "MCD": 297,
    "KO": 59,
    "PEP": 169,
    "JPM": 170,
    "BAC": 34,
    "GS": 385,
    "C": 51,
    "WFC": 50,
    "JNJ": 158,
    "PFE": 29,
    "MRK": 110,
    "ABBV": 155,
    "UNH": 525,
    "XOM": 101,
    "CVX": 150,
    "COP": 118,
    "CAT": 295,
    "BA": 260,
    "GE": 128,
    "HON": 210
}

START_DATE = "2014-01-02"
END_DATE = "2024-12-31"

# business days only
DATES = pd.date_range(start=START_DATE, end=END_DATE, freq="B")

COLUMNS = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]


# =========================
# Generate one ticker
# =========================
def generate_stock_data(ticker, base_price):
    rows = []
    price = float(base_price)

    for d in DATES:
        # daily drift and volatility
        drift = random.uniform(-0.015, 0.015)   # -1.5% to +1.5%
        gap = random.uniform(-0.008, 0.008)

        open_price = round(max(1, price * (1 + gap)), 2)
        close_price = round(max(1, open_price * (1 + drift)), 2)

        intraday_up = random.uniform(0.001, 0.02)
        intraday_down = random.uniform(0.001, 0.02)

        high_price = round(max(open_price, close_price) * (1 + intraday_up), 2)
        low_price = round(min(open_price, close_price) * (1 - intraday_down), 2)

        # keep low price positive
        low_price = max(0.01, low_price)

        adj_close = close_price

        # ticker-based volume ranges
        if ticker in ["AAPL", "TSLA", "AMZN", "NVDA"]:
            volume = random.randint(30000000, 120000000)
        elif ticker in ["MSFT", "GOOGL", "META", "BAC", "PFE", "VZ"]:
            volume = random.randint(10000000, 50000000)
        else:
            volume = random.randint(2000000, 20000000)

        rows.append([
            d.strftime("%Y-%m-%d"),
            open_price,
            high_price,
            low_price,
            close_price,
            adj_close,
            volume
        ])

        price = close_price

    return pd.DataFrame(rows, columns=COLUMNS)


# =========================
# Main
# =========================
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_files = 0
    total_rows = 0

    for ticker, base_price in TICKER_BASE_PRICE.items():
        df = generate_stock_data(ticker, base_price)
        file_path = os.path.join(OUTPUT_DIR, f"{ticker}.csv")
        df.to_csv(file_path, index=False)

        total_files += 1
        total_rows += len(df)

        print(f"[CREATED] {file_path} -> {len(df)} rows")

    print("\n==============================")
    print(f"Done. Generated {total_files} CSV files.")
    print(f"Total rows: {total_rows}")
    print(f"Date range: {START_DATE} to {END_DATE}")
    print("==============================")


if __name__ == "__main__":
    main()
