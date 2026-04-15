import os
import time
import random
import pandas as pd
import yfinance as yf

company_data = {
    "Technology": {
        "Apple Inc. (AAPL)": "AAPL",
        "Microsoft Corporation (MSFT)": "MSFT",
        "NVIDIA Corporation (NVDA)": "NVDA"
    },
    "Communication Services": {
        "Alphabet Inc. (GOOGL)": "GOOGL",
        "Meta Platforms Inc. (META)": "META",
        "Walt Disney Company (DIS)": "DIS",
        "Netflix Inc. (NFLX)": "NFLX",
        "Verizon Communications Inc. (VZ)": "VZ"
    },
    "Consumer": {
        "Amazon.com Inc. (AMZN)": "AMZN",
        "Tesla Inc. (TSLA)": "TSLA",
        "McDonald's Corporation (MCD)": "MCD",
        "Coca-Cola Company (KO)": "KO",
        "PepsiCo Inc. (PEP)": "PEP"
    },
    "Financial Services": {
        "JPMorgan Chase & Co. (JPM)": "JPM",
        "Bank of America Corporation (BAC)": "BAC",
        "Goldman Sachs Group Inc. (GS)": "GS",
        "Citigroup Inc. (C)": "C",
        "Wells Fargo & Company (WFC)": "WFC"
    },
    "Healthcare": {
        "Johnson & Johnson (JNJ)": "JNJ",
        "Pfizer Inc. (PFE)": "PFE",
        "Merck & Co. Inc. (MRK)": "MRK",
        "AbbVie Inc. (ABBV)": "ABBV",
        "UnitedHealth Group Incorporated (UNH)": "UNH"
    },
    "Energy": {
        "Exxon Mobil Corporation (XOM)": "XOM",
        "Chevron Corporation (CVX)": "CVX",
        "ConocoPhillips (COP)": "COP"
    },
    "Industrials": {
        "Caterpillar Inc. (CAT)": "CAT",
        "Boeing Company (BA)": "BA",
        "GE Aerospace (GE)": "GE",
        "Honeywell International Inc. (HON)": "HON"
    }
}

def clean_value(value):
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        if value.lower() in ["", "n/a", "nan", "none"]:
            return None
        return value
    try:
        if pd.isna(value):
            return None
    except Exception:
        pass
    return value

def build_ticker_list(company_data):
    rows = []
    for sector, companies in company_data.items():
        for company_name, ticker in companies.items():
            rows.append({
                "ticker": ticker,
                "fallback_name": company_name.split(" (")[0],
                "fallback_sector": sector
            })
    return rows

def fetch_info_with_retry(ticker, fallback_name, fallback_sector, max_retries=3):
    record = {
        "ticker": ticker,
        "longName": fallback_name,
        "sector": fallback_sector,
        "industry": None,
        "marketCap": None,
        "trailingPE": None,
        "revenueGrowth": None,
        "profitMargins": None,
        "currentRatio": None,
        "debtToEquity": None
    }

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Fetching {ticker} ... attempt {attempt}/{max_retries}")

            stock = yf.Ticker(ticker)
            info = stock.info

            record["longName"] = clean_value(info.get("longName", fallback_name)) or fallback_name
            record["sector"] = clean_value(info.get("sector", fallback_sector)) or fallback_sector
            record["industry"] = clean_value(info.get("industry"))
            record["marketCap"] = clean_value(info.get("marketCap"))
            record["trailingPE"] = clean_value(info.get("trailingPE"))
            record["revenueGrowth"] = clean_value(info.get("revenueGrowth"))
            record["profitMargins"] = clean_value(info.get("profitMargins"))
            record["currentRatio"] = clean_value(info.get("currentRatio"))
            record["debtToEquity"] = clean_value(info.get("debtToEquity"))

            print(f"  Success: {ticker}")
            return record

        except Exception as e:
            print(f"  Failed: {ticker} -> {e}")

            if attempt < max_retries:
                sleep_time = random.randint(10, 25)
                print(f"  Waiting {sleep_time} seconds before retry...")
                time.sleep(sleep_time)
            else:
                print(f"  Giving up on {ticker}, keeping fallback values.")

    return record

def main():
    os.makedirs("data", exist_ok=True)

    ticker_rows = build_ticker_list(company_data)
    records = []

    print("Starting financial info collection...")
    print(f"Total tickers: {len(ticker_rows)}")

    for i, item in enumerate(ticker_rows, start=1):
        ticker = item["ticker"]
        fallback_name = item["fallback_name"]
        fallback_sector = item["fallback_sector"]

        print(f"\n[{i}/{len(ticker_rows)}]")
        record = fetch_info_with_retry(
            ticker=ticker,
            fallback_name=fallback_name,
            fallback_sector=fallback_sector,
            max_retries=3
        )
        records.append(record)

        # Slow down between tickers to reduce rate limit risk
        sleep_time = random.randint(8, 18)
        print(f"Sleeping {sleep_time} seconds before next ticker...")
        time.sleep(sleep_time)

    df = pd.DataFrame(records)

    columns = [
        "ticker",
        "longName",
        "sector",
        "industry",
        "marketCap",
        "trailingPE",
        "revenueGrowth",
        "profitMargins",
        "currentRatio",
        "debtToEquity"
    ]
    df = df[columns]

    output_path = os.path.join("data", "financial_info.csv")
    df.to_csv(output_path, index=False, encoding="utf-8")

    print("\nDone.")
    print(f"Saved to: {output_path}")

    print("\nMissing value summary:")
    print(df.isna().sum())

    print("\nPreview:")
    print(df.head(10))

if __name__ == "__main__":
    main()
