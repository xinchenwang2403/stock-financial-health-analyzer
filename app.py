import os
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Stock Financial Health Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Financial Health Analyzer")
st.write(
    "This dashboard reviews stock price trends and basic financial health indicators. "
    "It first tries Yahoo Finance. If online retrieval fails, it automatically falls back "
    "to local CSV files where applicable."
)

# -----------------------------
# Company/sector mapping
# -----------------------------
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

# -----------------------------
# Sidebar
# -----------------------------
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
analyze_button = st.sidebar.button("Run Analysis")

st.sidebar.markdown("---")
st.sidebar.write(f"**Selected Ticker:** {ticker}")
st.sidebar.write(f"**Sector Group:** {selected_sector}")

# -----------------------------
# Helper functions
# -----------------------------
def format_value(value, percentage=False):
    if value is None or value == "N/A":
        return "N/A"
    try:
        if isinstance(value, str):
            if value.strip().upper() == "N/A":
                return "N/A"
            value = float(value)

        if percentage:
            return f"{value * 100:.2f}%"

        if value >= 1e12:
            return f"{value / 1e12:.2f}T"
        elif value >= 1e9:
            return f"{value / 1e9:.2f}B"
        elif value >= 1e6:
            return f"{value / 1e6:.2f}M"
        return f"{value:,.2f}"
    except Exception:
        return str(value)


def evaluate_liquidity(current_ratio):
    if not isinstance(current_ratio, (int, float)):
        return "Liquidity data is unavailable."
    if current_ratio >= 1.5:
        return "Good liquidity position."
    elif current_ratio >= 1.0:
        return "Acceptable liquidity position."
    else:
        return "Weak liquidity position."


def evaluate_solvency(debt_to_equity):
    if not isinstance(debt_to_equity, (int, float)):
        return "Solvency data is unavailable."
    if debt_to_equity < 50:
        return "Low leverage and strong solvency."
    elif debt_to_equity < 100:
        return "Moderate leverage and manageable solvency risk."
    else:
        return "High leverage may indicate solvency risk."


def evaluate_profitability(profit_margins):
    if not isinstance(profit_margins, (int, float)):
        return "Profitability data is unavailable."
    if profit_margins > 0.20:
        return "Company shows strong profitability."
    elif profit_margins > 0.10:
        return "Company shows decent profitability."
    else:
        return "Profitability may be weak."


def evaluate_growth(revenue_growth):
    if not isinstance(revenue_growth, (int, float)):
        return "Growth data is unavailable."
    if revenue_growth > 0.10:
        return "Revenue is growing strongly."
    elif revenue_growth > 0:
        return "Revenue is growing."
    else:
        return "Revenue growth is weak or negative."


def score_liquidity(current_ratio):
    if not isinstance(current_ratio, (int, float)):
        return None
    if current_ratio >= 1.5:
        return 25
    elif current_ratio >= 1.0:
        return 18
    else:
        return 10


def score_solvency(debt_to_equity):
    if not isinstance(debt_to_equity, (int, float)):
        return None
    if debt_to_equity < 50:
        return 25
    elif debt_to_equity < 100:
        return 18
    else:
        return 10


def score_profitability(profit_margins):
    if not isinstance(profit_margins, (int, float)):
        return None
    if profit_margins > 0.20:
        return 25
    elif profit_margins > 0.10:
        return 18
    else:
        return 10


def score_growth(revenue_growth):
    if not isinstance(revenue_growth, (int, float)):
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

    overall_score = sum(available_scores)
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

    for msg in [liquidity_msg, solvency_msg, profitability_msg, growth_msg]:
        if "unavailable" not in msg.lower():
            summary_parts.append(msg)

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


# -----------------------------
# Data loading functions
# -----------------------------
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
    file_path = os.path.join("data", f"{ticker}.csv")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Local CSV file not found: {file_path}")

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

    return filtered_df


@st.cache_data(ttl=1800)
def load_local_financial_info(ticker):
    file_path = os.path.join("data", "financial_info.csv")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Local financial info file not found: {file_path}")

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
            try:
                if str(record[field]).strip().upper() == "N/A":
                    record[field] = "N/A"
                else:
                    record[field] = float(record[field])
            except Exception:
                record[field] = "N/A"

    return record


# -----------------------------
# Main analysis
# -----------------------------
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

        # -----------------------------
        # Price data: Yahoo Finance first, then local CSV
        # -----------------------------
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

        # -----------------------------
        # Financial info: Yahoo Finance -> Local CSV
        # -----------------------------
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
                    "sector": "N/A",
                    "industry": "N/A",
                    "marketCap": "N/A",
                    "trailingPE": "N/A",
                    "revenueGrowth": "N/A",
                    "profitMargins": "N/A",
                    "currentRatio": "N/A",
                    "debtToEquity": "N/A",
                }
                info_source = "Unavailable"

        # -----------------------------
        # Source status display
        # -----------------------------
        st.success(f"Stock price data source: **{price_source}**")
        st.success(f"Financial info source: **{info_source}**")

        if price_source == "Local CSV":
            st.info("Live stock price data was unavailable, so the app used local CSV price data.")

        if info_source == "Local financial_info.csv":
            st.info("Live company financial indicators were unavailable, so the app used local financial_info.csv data.")

        if info_source == "Unavailable":
            st.warning("Company financial indicators are unavailable from Yahoo Finance and local sources.")

        with st.expander("View data retrieval details"):
            if online_price_error:
                st.write(f"**Yahoo Finance price error:** {online_price_error}")
            if local_price_error:
                st.write(f"**Local CSV price error:** {local_price_error}")
            if online_info_error:
                st.write(f"**Yahoo Finance financial info error:** {online_info_error}")
            if local_info_error:
                st.write(f"**Local financial info error:** {local_info_error}")

        company_name = info.get("longName", ticker)
        sector = info.get("sector", "N/A")
        industry = info.get("industry", "N/A")

        if sector == "N/A":
            sector = selected_sector

        st.subheader(f"{company_name} ({ticker})")
        st.write(f"**Sector:** {sector} | **Industry:** {industry}")

        # -----------------------------
        # Market Overview
        # -----------------------------
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

        # -----------------------------
        # Enhanced chart: Candlestick
        # -----------------------------
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

        # -----------------------------
        # Enhanced chart: Volume
        # -----------------------------
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

        # -----------------------------
        # Key Financial Indicators
        # -----------------------------
        st.header("2. Key Financial Indicators")

        market_cap = info.get("marketCap", "N/A")
        trailing_pe = info.get("trailingPE", "N/A")
        revenue_growth = info.get("revenueGrowth", "N/A")
        profit_margins = info.get("profitMargins", "N/A")
        current_ratio = info.get("currentRatio", "N/A")
        debt_to_equity = info.get("debtToEquity", "N/A")

        col6, col7, col8 = st.columns(3)
        col6.metric("Market Cap", format_value(market_cap))
        col7.metric("Trailing P/E", format_value(trailing_pe))
        col8.metric("Current Ratio", format_value(current_ratio))

        col9, col10, col11 = st.columns(3)
        col9.metric("Debt to Equity", format_value(debt_to_equity))
        col10.metric("Revenue Growth", format_value(revenue_growth, percentage=True))
        col11.metric("Profit Margins", format_value(profit_margins, percentage=True))

        # -----------------------------
        # Financial Dimension Evaluation
        # -----------------------------
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

        # -----------------------------
        # Overall Financial Health Score
        # -----------------------------
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
            f"{overall_score}/100" if overall_score is not None else "N/A"
        )
        score_col2.metric(
            "Rating",
            score_label(overall_score)
        )

        st.subheader("Dimension Scores")
        st.write(f"- Liquidity: {dimension_scores['Liquidity'] if dimension_scores['Liquidity'] is not None else 'N/A'} / 25")
        st.write(f"- Solvency: {dimension_scores['Solvency'] if dimension_scores['Solvency'] is not None else 'N/A'} / 25")
        st.write(f"- Profitability: {dimension_scores['Profitability'] if dimension_scores['Profitability'] is not None else 'N/A'} / 25")
        st.write(f"- Growth: {dimension_scores['Growth'] if dimension_scores['Growth'] is not None else 'N/A'} / 25")

        # -----------------------------
        # Summary Insight
        # -----------------------------
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
                "using selected financial indicators. It integrates public market data and local CSV fallback. "
                "The tool is intended for educational and exploratory use rather than as professional investment advice."
            )

        # -----------------------------
        # Export
        # -----------------------------
        st.header("6. Export Analysis Result")

        export_df = build_export_dataframe(
            ticker=ticker,
            company_name=company_name,
            sector=sector,
            industry=industry,
            latest_close=latest_close,
            price_change=price_change,
            price_change_pct=price_change_pct,
            avg_volume=avg_volume,
            market_cap=market_cap,
            trailing_pe=trailing_pe,
            revenue_growth=revenue_growth,
            profit_margins=profit_margins,
            current_ratio=current_ratio,
            debt_to_equity=debt_to_equity,
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
