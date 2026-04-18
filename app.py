import os
import datetime
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="Stock Financial Health Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Financial Health Analyzer")
st.write(
    "This dashboard reviews stock price trends, basic financial health indicators, "
    "and the latest investment news. It first tries Yahoo Finance. If online retrieval fails, "
    "it automatically falls back to local CSV files where applicable."
)

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

st.sidebar.header("Input Settings")

selected_sector = st.sidebar.selectbox(
    "Select sector:",
    options=list(company_data.keys())
)

selected_company = st.sidebar.selectbox(
    "Select a company:",
    options=list(company_data[selected_sector].keys())
)

ticker = company_data[selected_sector][selected_company]

period = st.sidebar.selectbox(
    "Select analysis period:",
    options=["1mo", "3mo", "6mo", "1y", "5y", "10y"],
    index=2
)

show_raw_data = st.sidebar.checkbox("Show recent stock data table", value=True)
show_candlestick = st.sidebar.checkbox("Show candlestick chart", value=True)
show_volume_chart = st.sidebar.checkbox("Show volume chart", value=True)
show_moving_averages = st.sidebar.checkbox("Show moving averages", value=True)
show_company_news = st.sidebar.checkbox("Show company news", value=True)
show_market_news = st.sidebar.checkbox("Show market news", value=True)
analyze_button = st.sidebar.button("Run Analysis")

st.sidebar.markdown("---")
st.sidebar.write(f"**Selected Ticker:** {ticker}")
st.sidebar.write(f"**Sector Group:** {selected_sector}")


def clean_numeric(value):
    if value is None:
        return None
    if isinstance(value, str):
        if value.strip().upper() in ["N/A", "NONE", "", "NAN"]:
            return None
        try:
            return float(value)
        except Exception:
            return None
    if pd.isna(value):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def display_text(value, fallback="Data not available"):
    if value is None:
        return fallback
    if isinstance(value, str) and value.strip().upper() == "N/A":
        return fallback
    if isinstance(value, str) and value.strip() == "":
        return fallback
    return value


def format_value(value, percentage=False):
    value = clean_numeric(value)
    if value is None:
        return "Data not available"

    try:
        if percentage:
            return f"{value * 100:.2f}%"

        if abs(value) >= 1e12:
            return f"{value / 1e12:.2f}T"
        elif abs(value) >= 1e9:
            return f"{value / 1e9:.2f}B"
        elif abs(value) >= 1e6:
            return f"{value / 1e6:.2f}M"
        return f"{value:,.2f}"
    except Exception:
        return "Data not available"


def evaluate_liquidity(current_ratio):
    current_ratio = clean_numeric(current_ratio)
    if current_ratio is None:
        return "Liquidity could not be assessed because the current ratio is not available."
    if current_ratio >= 1.5:
        return "The company shows a good liquidity position."
    elif current_ratio >= 1.0:
        return "The company has an acceptable liquidity position."
    else:
        return "The company may have a relatively weak liquidity position."


def evaluate_solvency(debt_to_equity):
    debt_to_equity = clean_numeric(debt_to_equity)
    if debt_to_equity is None:
        return "Solvency could not be assessed because debt-to-equity data is not available."
    if debt_to_equity < 50:
        return "The company appears to have a relatively low debt burden."
    elif debt_to_equity < 100:
        return "The company has a moderate debt level."
    else:
        return "The company may have relatively high leverage."


def evaluate_profitability(profit_margins):
    profit_margins = clean_numeric(profit_margins)
    if profit_margins is None:
        return "Profitability could not be assessed because profit margin data is not available."
    if profit_margins > 0.20:
        return "The company shows strong profitability."
    elif profit_margins > 0.10:
        return "The company shows decent profitability."
    else:
        return "The company’s profitability appears relatively weak."


def evaluate_growth(revenue_growth):
    revenue_growth = clean_numeric(revenue_growth)
    if revenue_growth is None:
        return "Growth could not be assessed because revenue growth data is not available."
    if revenue_growth > 0.10:
        return "Revenue is growing strongly."
    elif revenue_growth > 0:
        return "Revenue is growing."
    else:
        return "Revenue growth is weak or negative."


def score_liquidity(current_ratio):
    current_ratio = clean_numeric(current_ratio)
    if current_ratio is None:
        return None
    if current_ratio >= 1.5:
        return 25
    elif current_ratio >= 1.0:
        return 18
    else:
        return 10


def score_solvency(debt_to_equity):
    debt_to_equity = clean_numeric(debt_to_equity)
    if debt_to_equity is None:
        return None
    if debt_to_equity < 50:
        return 25
    elif debt_to_equity < 100:
        return 18
    else:
        return 10


def score_profitability(profit_margins):
    profit_margins = clean_numeric(profit_margins)
    if profit_margins is None:
        return None
    if profit_margins > 0.20:
        return 25
    elif profit_margins > 0.10:
        return 18
    else:
        return 10


def score_growth(revenue_growth):
    revenue_growth = clean_numeric(revenue_growth)
    if revenue_growth is None:
        return None
    if revenue_growth > 0.15:
        return 25
    elif revenue_growth > 0:
        return 18
    else:
        return 10


def calculate_overall_score(current_ratio, debt_to_equity, profit_margins, revenue_growth):
    scores = {
        "Liquidity": score_liquidity(current_ratio),
        "Solvency": score_solvency(debt_to_equity),
        "Profitability": score_profitability(profit_margins),
        "Growth": score_growth(revenue_growth)
    }

    available_scores = [v for v in scores.values() if v is not None]

    if not available_scores:
        return None, scores

    if len(available_scores) == 4:
        overall_score = sum(available_scores)
    else:
        overall_score = round(sum(available_scores) / len(available_scores) * 4)

    return overall_score, scores


def score_label(score):
    if score is None:
        return "Unavailable"
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Moderate"
    else:
        return "Weak"


def build_overall_summary(liquidity_msg, solvency_msg, profitability_msg, growth_msg, score):
    summary_parts = []

    if score is not None:
        summary_parts.append(
            f"The company receives an overall financial health score of {score}/100, "
            f"which is classified as {score_label(score).lower()}."
        )

    useful_messages = []
    for msg in [liquidity_msg, solvency_msg, profitability_msg, growth_msg]:
        if msg and "could not be assessed" not in msg.lower():
            useful_messages.append(msg)

    summary_parts.extend(useful_messages)

    if not summary_parts:
        return "Overall summary: insufficient financial data is available to generate a meaningful assessment."

    return "Overall summary: " + " ".join(summary_parts)


def period_to_days(period):
    mapping = {
        "1mo": 30,
        "3mo": 90,
        "6mo": 180,
        "1y": 365,
        "5y": 365 * 5,
        "10y": 365 * 10
    }
    return mapping.get(period, 180)


def build_export_dataframe(
    ticker, company_name, sector, industry,
    latest_close, price_change, price_change_pct, avg_volume,
    market_cap, trailing_pe, revenue_growth, profit_margins,
    current_ratio, debt_to_equity,
    overall_score, overall_rating, price_source, info_source
):
    data = {
        "Ticker": [ticker],
        "Company Name": [company_name],
        "Sector": [sector],
        "Industry": [industry],
        "Latest Close Price": [latest_close],
        "Price Change": [price_change],
        "Price Change %": [price_change_pct],
        "Average Volume": [avg_volume],
        "Market Cap": [market_cap],
        "Trailing PE": [trailing_pe],
        "Revenue Growth": [revenue_growth],
        "Profit Margins": [profit_margins],
        "Current Ratio": [current_ratio],
        "Debt to Equity": [debt_to_equity],
        "Overall Score": [overall_score],
        "Overall Rating": [overall_rating],
        "Price Data Source": [price_source],
        "Financial Info Source": [info_source]
    }
    return pd.DataFrame(data)


def find_file(filename):
    candidate_paths = [
        os.path.join(BASE_DIR, "data", filename),
        os.path.join(BASE_DIR, filename)
    ]
    for path in candidate_paths:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(
        f"File not found in either location: {candidate_paths[0]} or {candidate_paths[1]}"
    )


def format_news_time(raw_time):
    if raw_time is None:
        return "Unknown time"

    if isinstance(raw_time, (int, float)):
        try:
            dt = datetime.datetime.fromtimestamp(raw_time)
            return dt.strftime("%Y-%m-%d %H:%M")
        except Exception:
            return "Unknown time"

    if isinstance(raw_time, str):
        try:
            dt = datetime.datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d %H:%M")
        except Exception:
            return raw_time

    return "Unknown time"


def parse_news_item(item):
    if not isinstance(item, dict):
        return {
            "title": "No title available",
            "publisher": "Unknown source",
            "link": None,
            "published": "Unknown time",
            "summary": "No summary available.",
            "related": []
        }

    content = item.get("content", {}) if isinstance(item.get("content", {}), dict) else {}

    title = (
        item.get("title")
        or content.get("title")
        or "No title available"
    )

    publisher = (
        item.get("publisher")
        or content.get("publisher")
        or content.get("provider", {}).get("displayName")
        or "Unknown source"
    )

    link = (
        item.get("link")
        or content.get("canonicalUrl", {}).get("url")
        or content.get("clickThroughUrl", {}).get("url")
        or None
    )

    raw_time = (
        item.get("providerPublishTime")
        or content.get("pubDate")
        or item.get("pubDate")
        or None
    )
    published = format_news_time(raw_time)

    summary = (
        item.get("summary")
        or content.get("summary")
        or content.get("description")
        or "No summary available."
    )

    related = (
        item.get("relatedTickers")
        or content.get("relatedTickers")
        or []
    )

    return {
        "title": title,
        "publisher": publisher,
        "link": link,
        "published": published,
        "summary": summary,
        "related": related
    }


def deduplicate_news(news_items):
    seen = set()
    clean_list = []

    for item in news_items:
        parsed = parse_news_item(item)
        key = (parsed["title"], parsed["link"])

        if key not in seen:
            seen.add(key)
            clean_list.append(parsed)

    return clean_list


@st.cache_data(ttl=1800)
def load_stock_history_online(ticker, period):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    return hist


@st.cache_data(ttl=1800)
def load_stock_info_online(ticker):
    stock = yf.Ticker(ticker)
    return stock.info


@st.cache_data(ttl=1800)
def load_local_csv_data(ticker, period):
    file_path = find_file(f"{ticker}.csv")
    df = pd.read_csv(file_path)

    if "Date" not in df.columns:
        raise ValueError("Local CSV must contain a 'Date' column.")

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    df = df.set_index("Date")

    if "Close" not in df.columns:
        raise ValueError("Local CSV must contain a 'Close' column.")

    days = period_to_days(period)
    latest_date = df.index.max()
    cutoff_date = latest_date - pd.Timedelta(days=days)
    filtered_df = df[df.index >= cutoff_date]

    if filtered_df.empty:
        raise ValueError(f"No local stock data available for ticker {ticker} within period {period}.")

    return filtered_df


@st.cache_data(ttl=1800)
def load_local_financial_info(ticker):
    file_path = find_file("financial_info.csv")
    df = pd.read_csv(file_path)

    if "ticker" not in df.columns:
        raise ValueError("financial_info.csv must contain a 'ticker' column.")

    row = df[df["ticker"].astype(str).str.upper() == ticker.upper()]

    if row.empty:
        raise ValueError(f"No local financial info found for ticker: {ticker}")

    record = row.iloc[0].to_dict()

    numeric_fields = [
        "marketCap",
        "trailingPE",
        "revenueGrowth",
        "profitMargins",
        "currentRatio",
        "debtToEquity"
    ]

    for field in numeric_fields:
        if field in record:
            record[field] = clean_numeric(record[field])

    return record


@st.cache_data(ttl=1800)
def load_company_news(ticker):
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        if not news:
            return []
        parsed_news = deduplicate_news(news)
        return parsed_news
    except Exception:
        return []


@st.cache_data(ttl=1800)
def load_market_news():
    market_tickers = ["^GSPC", "^IXIC", "^DJI"]
    all_news = []

    for mt in market_tickers:
        try:
            index_obj = yf.Ticker(mt)
            items = index_obj.news
            if items:
                all_news.extend(items)
        except Exception:
            continue

    parsed_news = deduplicate_news(all_news)
    return parsed_news[:8]


if analyze_button:
    if not ticker:
        st.warning("Please select a valid stock ticker symbol.")
    else:
        hist = None
        info = {}
        price_source = None
        info_source = None

        online_price_error = None
        local_price_error = None
        online_info_error = None
        local_info_error = None

        try:
            with st.spinner("Trying to retrieve stock price data from Yahoo Finance..."):
                hist = load_stock_history_online(ticker, period)
            if hist is not None and not hist.empty:
                price_source = "Yahoo Finance"
        except Exception as e:
            online_price_error = str(e)

        if hist is None or hist.empty:
            try:
                with st.spinner("Online stock price retrieval failed. Loading local CSV data..."):
                    hist = load_local_csv_data(ticker, period)
                if hist is not None and not hist.empty:
                    price_source = "Local CSV"
            except Exception as e:
                local_price_error = str(e)

        if hist is None or hist.empty:
            st.error("Unable to retrieve stock price data from both Yahoo Finance and local CSV.")
            if online_price_error:
                st.write(f"**Yahoo Finance price error:** {online_price_error}")
            if local_price_error:
                st.write(f"**Local CSV price error:** {local_price_error}")
            st.stop()

        try:
            with st.spinner("Trying to retrieve company financial indicators from Yahoo Finance..."):
                info = load_stock_info_online(ticker)
            if isinstance(info, dict) and len(info) > 0:
                info_source = "Yahoo Finance"
        except Exception as e:
            online_info_error = str(e)

        if not info or not isinstance(info, dict):
            try:
                with st.spinner("Yahoo Finance financial retrieval failed. Loading local financial info..."):
                    info = load_local_financial_info(ticker)
                info_source = "Local financial_info.csv"
            except Exception as e:
                local_info_error = str(e)
                info = {
                    "longName": ticker,
                    "sector": selected_sector,
                    "industry": None,
                    "marketCap": None,
                    "trailingPE": None,
                    "revenueGrowth": None,
                    "profitMargins": None,
                    "currentRatio": None,
                    "debtToEquity": None,
                }
                info_source = "Unavailable"

        st.success(f"Stock price data source: **{price_source}**")
        st.success(f"Financial info source: **{info_source}**")

        if price_source == "Local CSV":
            st.info("Live stock price data was unavailable, so the app used local CSV price data.")

        if info_source == "Local financial_info.csv":
            st.info("Live company financial indicators were unavailable, so the app used local financial_info.csv data.")

        if info_source == "Unavailable":
            st.warning("Company financial indicators are currently unavailable from both Yahoo Finance and local sources.")

        with st.expander("View data retrieval details"):
            if online_price_error:
                st.write(f"**Yahoo Finance price error:** {online_price_error}")
            if local_price_error:
                st.write(f"**Local CSV price error:** {local_price_error}")
            if online_info_error:
                st.write(f"**Yahoo Finance financial info error:** {online_info_error}")
            if local_info_error:
                st.write(f"**Local financial info error:** {local_info_error}")

        company_name = display_text(info.get("longName", ticker), ticker)
        sector = display_text(info.get("sector", selected_sector), selected_sector)
        industry = display_text(info.get("industry", None), "Not provided")

        st.subheader(f"{company_name} ({ticker})")
        st.write(f"**Sector:** {sector} | **Industry:** {industry}")

        st.header("1. Market Overview")

        latest_close = float(hist["Close"].iloc[-1])
        first_close = float(hist["Close"].iloc[0])
        high_price = float(hist["High"].max()) if "High" in hist.columns else None
        low_price = float(hist["Low"].min()) if "Low" in hist.columns else None
        price_change = latest_close - first_close
        price_change_pct = (price_change / first_close) * 100 if first_close != 0 else 0
        avg_volume = float(hist["Volume"].mean()) if "Volume" in hist.columns else None

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Latest Close Price", f"{latest_close:,.2f} USD")
        col2.metric("Price Change", f"{price_change:,.2f} USD", f"{price_change_pct:.2f}%")
        col3.metric("Average Volume", format_value(avg_volume))
        col4.metric("Highest Price", format_value(high_price))
        col5.metric("Lowest Price", format_value(low_price))

        if show_raw_data:
            st.subheader("Recent Stock Data")
            display_hist = hist.copy().tail(20)
            st.dataframe(display_hist, use_container_width=True)

        hist = hist.copy()
        hist["MA20"] = hist["Close"].rolling(window=20).mean()
        hist["MA50"] = hist["Close"].rolling(window=50).mean()

        st.subheader("Closing Price Trend")

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=hist.index,
            y=hist["Close"],
            mode="lines",
            name="Close Price",
            line=dict(width=2)
        ))

        if show_moving_averages:
            fig.add_trace(go.Scatter(
                x=hist.index,
                y=hist["MA20"],
                mode="lines",
                name="20-Day Moving Average",
                line=dict(dash="dash")
            ))
            fig.add_trace(go.Scatter(
                x=hist.index,
                y=hist["MA50"],
                mode="lines",
                name="50-Day Moving Average",
                line=dict(dash="dot")
            ))

        fig.update_layout(
            title=f"{ticker} Closing Price Trend ({period})",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            hovermode="x unified",
            template="plotly_white",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        if show_candlestick and all(col in hist.columns for col in ["Open", "High", "Low", "Close"]):
            st.subheader("Candlestick Chart")

            candle_fig = go.Figure(data=[
                go.Candlestick(
                    x=hist.index,
                    open=hist["Open"],
                    high=hist["High"],
                    low=hist["Low"],
                    close=hist["Close"],
                    name="Candlestick"
                )
            ])

            candle_fig.update_layout(
                title=f"{ticker} Candlestick Chart ({period})",
                xaxis_title="Date",
                yaxis_title="Price (USD)",
                template="plotly_white",
                height=600
            )

            st.plotly_chart(candle_fig, use_container_width=True)

        if show_volume_chart and "Volume" in hist.columns:
            st.subheader("Trading Volume")

            volume_fig = go.Figure()
            volume_fig.add_trace(go.Bar(
                x=hist.index,
                y=hist["Volume"],
                name="Volume"
            ))

            volume_fig.update_layout(
                title=f"{ticker} Trading Volume ({period})",
                xaxis_title="Date",
                yaxis_title="Volume",
                template="plotly_white",
                height=400
            )

            st.plotly_chart(volume_fig, use_container_width=True)

        st.header("2. Key Financial Indicators")

        market_cap = info.get("marketCap", None)
        trailing_pe = info.get("trailingPE", None)
        revenue_growth = info.get("revenueGrowth", None)
        profit_margins = info.get("profitMargins", None)
        current_ratio = info.get("currentRatio", None)
        debt_to_equity = info.get("debtToEquity", None)

        col6, col7, col8 = st.columns(3)
        col6.metric("Market Cap", format_value(market_cap))
        col7.metric("Trailing P/E", format_value(trailing_pe))
        col8.metric("Current Ratio", format_value(current_ratio))

        col9, col10, col11 = st.columns(3)
        col9.metric("Debt to Equity", format_value(debt_to_equity))
        col10.metric("Revenue Growth", format_value(revenue_growth, percentage=True))
        col11.metric("Profit Margins", format_value(profit_margins, percentage=True))

        available_financial_items = sum([
            clean_numeric(market_cap) is not None,
            clean_numeric(trailing_pe) is not None,
            clean_numeric(revenue_growth) is not None,
            clean_numeric(profit_margins) is not None,
            clean_numeric(current_ratio) is not None,
            clean_numeric(debt_to_equity) is not None
        ])

        if available_financial_items <= 2:
            st.info("Only limited financial indicator data is currently available for this company.")

        st.header("3. Financial Dimension Evaluation")

        liquidity_msg = evaluate_liquidity(current_ratio)
        solvency_msg = evaluate_solvency(debt_to_equity)
        profitability_msg = evaluate_profitability(profit_margins)
        growth_msg = evaluate_growth(revenue_growth)

        eval_col1, eval_col2 = st.columns(2)

        with eval_col1:
            st.subheader("Liquidity")
            st.write(f"- {liquidity_msg}")
            st.subheader("Solvency")
            st.write(f"- {solvency_msg}")

        with eval_col2:
            st.subheader("Profitability")
            st.write(f"- {profitability_msg}")
            st.subheader("Growth")
            st.write(f"- {growth_msg}")

        st.header("4. Overall Financial Health Score")

        overall_score, dimension_scores = calculate_overall_score(
            current_ratio,
            debt_to_equity,
            profit_margins,
            revenue_growth
        )

        score_col1, score_col2 = st.columns(2)
        score_col1.metric(
            "Overall Score",
            f"{overall_score}/100" if overall_score is not None else "Insufficient data"
        )
        score_col2.metric("Rating", score_label(overall_score))

        st.subheader("Dimension Scores")
        st.write(f"- Liquidity: {dimension_scores['Liquidity'] if dimension_scores['Liquidity'] is not None else 'Not available'} / 25")
        st.write(f"- Solvency: {dimension_scores['Solvency'] if dimension_scores['Solvency'] is not None else 'Not available'} / 25")
        st.write(f"- Profitability: {dimension_scores['Profitability'] if dimension_scores['Profitability'] is not None else 'Not available'} / 25")
        st.write(f"- Growth: {dimension_scores['Growth'] if dimension_scores['Growth'] is not None else 'Not available'} / 25")

        st.header("5. Summary Insight")

        summary_text = build_overall_summary(
            liquidity_msg,
            solvency_msg,
            profitability_msg,
            growth_msg,
            overall_score
        )
        st.success(summary_text)

        with st.expander("Interpretation Note"):
            st.write(
                "This dashboard provides a simple rule-based interpretation and scoring framework "
                "using selected financial indicators. It integrates public market data, company information, "
                "and daily news, with local CSV fallback for some datasets. The tool is intended for educational "
                "and exploratory use rather than as professional investment advice."
            )

        if show_company_news:
            st.header("6. Daily Company News")

            company_news = load_company_news(ticker)

            if company_news:
                st.write(f"Latest news related to **{company_name} ({ticker})**:")

                for i, item in enumerate(company_news[:5], start=1):
                    st.subheader(f"{i}. {item['title']}")
                    st.write(f"**Source:** {item['publisher']}")
                    st.write(f"**Published:** {item['published']}")
                    st.write(f"**Summary:** {item['summary']}")
                    if item["link"]:
                        st.markdown(f"[Read full article]({item['link']})")
                    st.markdown("---")
            else:
                st.info("No recent company news is currently available for this ticker.")

        if show_market_news:
            st.header("7. Daily Market News")

            market_news = load_market_news()

            if market_news:
                st.write("Latest market-wide news from major indices and the broader investment environment:")

                for i, item in enumerate(market_news[:6], start=1):
                    st.subheader(f"{i}. {item['title']}")
                    st.write(f"**Source:** {item['publisher']}")
                    st.write(f"**Published:** {item['published']}")
                    st.write(f"**Summary:** {item['summary']}")
                    if item["related"]:
                        st.write(f"**Related Tickers:** {', '.join(item['related'][:6])}")
                    if item["link"]:
                        st.markdown(f"[Read full article]({item['link']})")
                    st.markdown("---")
            else:
                st.info("No recent market news is currently available.")

        st.header("8. Export Analysis Result")

        export_df = build_export_dataframe(
            ticker=ticker,
            company_name=company_name,
            sector=sector,
            industry=industry,
            latest_close=latest_close,
            price_change=price_change,
            price_change_pct=price_change_pct,
            avg_volume=avg_volume,
            market_cap=market_cap if market_cap is not None else "N/A",
            trailing_pe=trailing_pe if trailing_pe is not None else "N/A",
            revenue_growth=revenue_growth if revenue_growth is not None else "N/A",
            profit_margins=profit_margins if profit_margins is not None else "N/A",
            current_ratio=current_ratio if current_ratio is not None else "N/A",
            debt_to_equity=debt_to_equity if debt_to_equity is not None else "N/A",
            overall_score=overall_score,
            overall_rating=score_label(overall_score),
            price_source=price_source,
            info_source=info_source
        )

        csv_data = export_df.to_csv(index=False).encode("utf-8")

        st.dataframe(export_df, use_container_width=True)

        st.download_button(
            label="Download Analysis Result as CSV",
            data=csv_data,
            file_name=f"{ticker}_analysis_result.csv",
            mime="text/csv"
        )

else:
    st.info("Please choose a company from the sidebar, then click **Run Analysis**.")
