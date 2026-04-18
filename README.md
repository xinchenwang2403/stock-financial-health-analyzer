# Stock Financial Health Analyzer

## Project Overview
The **Stock Financial Health Analyzer** is an interactive Streamlit dashboard designed to help users evaluate a company’s stock performance, financial health, and latest investment-related news in one place. The tool combines market price trends, selected accounting and financial indicators, and daily news updates to support more informed exploratory analysis.

This product is designed for **students, beginner investors, and non-specialist users** who want an accessible way to understand both market behaviour and basic company fundamentals without using complex professional financial platforms.

---

## Analytical Problem
Many users can observe stock price movements, but they often lack a simple way to connect those movements with core financial health indicators and current news context. Looking only at stock prices can be misleading, because a company’s market performance does not always reflect its liquidity, solvency, profitability, or growth position.

This project addresses the following analytical problem:

> **How can users evaluate a company more effectively by combining stock price trends, selected financial indicators, and recent investment news in one dashboard?**

This is relevant in a **financial and accounting context** because financial information becomes more useful when it is presented in a way that supports interpretation, comparison, and decision-making.

---

## Dataset Information

### 1. Yahoo Finance Data
**Source:** Yahoo Finance via the `yfinance` Python library  
**Access date:** [replace with your actual access date, e.g. 18 April 2026]  
**Type of data used:**
- Historical stock price data
- Company financial information
- Company-related news
- Market-wide news linked to major indices

**Coverage:**
- Stocks from multiple sectors, including:
  - Technology
  - Communication Services
  - Consumer
  - Financial Services
  - Healthcare
  - Energy
  - Industrials
- Historical price periods selectable by the user:
  - 1 month
  - 3 months
  - 6 months
  - 1 year
  - 5 years
  - 10 years
- Financial indicators used:
  - Market Capitalisation
  - Trailing P/E
  - Revenue Growth
  - Profit Margins
  - Current Ratio
  - Debt to Equity
- News coverage:
  - Company-specific news for the selected stock
  - Market-wide news from major indices such as S&P 500, Nasdaq, and Dow Jones

**Why this dataset was chosen:**  
Yahoo Finance is suitable for this project because it provides a practical and accessible source of public financial market data. It supports both stock-level and company-level analysis and enables the integration of price data, financial indicators, and current news into one product. This makes it well aligned with the analytical goal of combining numerical financial analysis with real-time market context.

---

### 2. Local CSV Fallback Data
**Source:** Local CSV files prepared for the project  
**Access date:** [replace with your actual preparation/use date]  

**Files used:**
- Individual stock CSV files such as `AAPL.csv`, `MSFT.csv`, etc.
- `financial_info.csv`

**Purpose:**  
The local CSV files are used as a fallback when online retrieval from Yahoo Finance is unavailable. This improves the reliability and reproducibility of the dashboard during demonstration or assessment.

**Why this dataset was chosen:**  
A fallback dataset was included to make the application more stable and user-friendly. If live retrieval fails, the dashboard can still display stock price data and selected financial indicators from local files.

---

## Python Workflow

The project follows a complete Python-based analytical workflow:

### 1. Data Retrieval
- The app first retrieves **historical stock prices** using `yfinance`.
- It then retrieves **company financial information** using `yfinance`.
- It also retrieves:
  - **company news** for the selected stock
  - **market news** from major market indices
- If online stock or financial data retrieval fails, the app uses **local CSV fallback files**.

### 2. Data Cleaning
The project includes functions to:
- handle missing values
- convert text-based numeric values into float format
- standardise invalid entries such as `N/A`, blank strings, or null values
- validate data before display and analysis

### 3. Data Transformation
The app transforms raw data into useful analytical outputs by:
- filtering historical prices according to the selected time period
- calculating price change and percentage change
- calculating average trading volume
- generating moving averages (20-day and 50-day)
- formatting large values such as millions, billions, and trillions
- parsing nested news data structures from Yahoo Finance into readable fields

### 4. Financial Analysis
The dashboard evaluates four financial dimensions:
- **Liquidity**
- **Solvency**
- **Profitability**
- **Growth**

It then applies a simple rule-based scoring framework to generate:
- dimension scores
- an **overall financial health score**
- a final rating such as:
  - Excellent
  - Good
  - Moderate
  - Weak

### 5. Visualisation
The dashboard uses interactive visualisation to improve interpretation:
- line chart for closing price trend
- optional moving average overlays
- candlestick chart
- trading volume bar chart
- dashboard metrics for key stock and financial indicators

### 6. Result Output
The app outputs:
- stock performance summary
- financial indicator summary
- overall financial health score
- company news
- market news
- downloadable CSV export of key analysis results

---

## Core Python Libraries Used

- **streamlit** – for building the interactive dashboard
- **yfinance** – for retrieving stock, company, and news data from Yahoo Finance
- **pandas** – for data loading, cleaning, filtering, transformation, and export
- **plotly.graph_objects** – for interactive charts and visualisation
- **os** – for local file path management
- **datetime** – for parsing and formatting news publication time

---

## Product Design and User Focus

This dashboard was designed with a strong user focus. The goal was not to create a professional trading terminal, but to build a clear and educational data product for non-expert users.

### User-oriented design features
- **Sector-based company selection** to make navigation easier
- **Simple sidebar controls** for selecting company and analysis period
- **Optional chart display controls** to avoid overwhelming the user
- **Automatic fallback to local data** when live data fails
- **Clear section headings** to guide users through the analysis
- **Plain-English financial evaluation messages** for each financial dimension
- **Daily company and market news modules** to add real-world context
- **Downloadable CSV result** for convenience and reproducibility

### Target users
- accounting and finance students
- beginner investors
- non-specialist users interested in stock analysis
- users who need a simple educational dashboard rather than a complex professional platform

---

## How to Run

### Environment Requirements
This project is written in **Python 3** and uses Streamlit for the dashboard interface.

### Required Libraries
Install the required packages using:


py -m pip install --upgrade streamlit yfinance pandas plotly
If needed, you can also install from a requirements.txt file:


py -m pip install -r requirements.txt
Project Files
Ensure your project folder includes:

app.py
optional local CSV files for fallback
financial_info.csv if using local financial fallback
stock CSV files such as AAPL.csv, MSFT.csv, etc. if using local price fallback
Recommended structure:

your_project/
│
├── app.py
├── README.md
├── requirements.txt
└── data/
    ├── AAPL.csv
    ├── MSFT.csv
    ├── NVDA.csv
    └── financial_info.csv
Run the App
Open the terminal in the project directory and run:


py -m streamlit run app.py
After running, Streamlit will provide a local address such as:


http://localhost:8502
Open that address in your browser.

Steps to Reproduce
Install the required Python packages.
Save the project files in the correct directory structure.
Run py -m streamlit run app.py.
Select a sector and company from the sidebar.
Select the analysis period.
Click Run Analysis.
Review:
market overview
stock charts
financial indicators
financial health evaluation
company news
market news
Export the result as CSV if needed.

##Key Insights & Results
1. Stock price movements alone do not provide a full evaluation
A company may show strong recent price performance, but this does not necessarily mean it has strong liquidity, profitability, or solvency. The dashboard highlights the importance of combining market data with financial indicators.

2. Financial health is multi-dimensional
The project shows that company evaluation should not rely on one ratio only. Liquidity, solvency, profitability, and growth each capture different aspects of financial health, so a broader view gives better insight.

3. News adds important real-world context
Daily company news and broader market news help users interpret recent market movement more meaningfully. This improves the practical value of the dashboard beyond purely numerical analysis.

4. Data reliability matters in financial analysis
The inclusion of local CSV fallback demonstrates that data availability and reliability are important issues in real-world financial data products. A robust product should continue to function even when live retrieval fails.

5. Simplicity improves accessibility
By presenting data with clear metrics, section headings, user controls, and plain-language interpretation, the dashboard makes financial analysis more accessible to non-expert users.

##Links
GitHub Repository: [replace with your GitHub repository link]
Demo Video: [replace with your demo video link]
Online Streamlit App (if available): [ Local URL: http://localhost:8502
  Network URL: http://192.168.10.3:8502]

##Author Info
Name: [Xinchen.Wang2403]
Student ID: [2470712]
Course Code: ACC102
Track: [Track 4]

##AI Disclosure
I used ChatGPT on [April/2026] to help with:

improving the structure and wording of the README
refining explanations of the project workflow
improving the clarity of the analytical problem, user focus, and key insights
supporting code explanation and documentation writing
All final coding decisions, project design decisions, file organisation, testing, and final review were completed by me.

##Notes 

This dashboard is intended for educational and exploratory purposes only. It provides a simple rule-based interpretation of selected financial indicators and public market information. It should not be treated as professional financial advice or investment advice.
