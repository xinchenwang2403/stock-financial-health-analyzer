# Stock Financial Health Analyzer

## Project Overview
The **Stock Financial Health Analyzer** is an interactive data product designed to help users evaluate a company's recent stock performance, financial condition, and news context in one dashboard. It is built for students, beginner investors, and business users who want a simple but structured way to explore stock-related insights.

The product creates value by combining **market trend analysis**, **financial health scoring**, and **daily news integration** into a single user-friendly interface. To improve reliability, it uses both **Yahoo Finance online data** and **local CSV fallback datasets**.

---

## Analytical Problem
The analytical problem addressed in this project is:

**How can users quickly and intuitively assess the short-term market performance and basic financial health of a listed company, while also considering recent company-specific and market-wide news that may influence investment perception?**

This problem is highly relevant in **finance**, **investment analysis**, and **business decision support**, because stock evaluation often requires users to combine:
- historical price movement,
- accounting and financial indicators,
- and current news signals.

Many beginners find it difficult to interpret these dimensions together. This project solves that problem by transforming multiple financial data sources into a clear, interactive, and explainable dashboard.

---

## Dataset Information

### 1. Online Data Source
**Yahoo Finance** via the `yfinance` Python library

### 2. Local Fallback Data Sources
The app also uses local CSV files when online data retrieval is unavailable or incomplete:
- stock price CSV files for selected tickers
- `financial_info.csv`
- `company_news.csv`
- `market_news.csv`

### Data Access / Collection Date
- Yahoo Finance data accessed dynamically during app runtime
- Local CSV fallback datasets prepared and accessed during project development and testing
- Recommended disclosure date:April/2026

### Data Scope
The project includes:
- **Historical stock prices** for selected listed companies
- **Financial indicators** such as:
  - market capitalization
  - trailing P/E ratio
  - revenue growth
  - profit margins
  - current ratio
  - debt-to-equity ratio
- **Company news** linked to the selected stock
- **Market-wide news** related to major indices such as:
  - S&P 500 (`^GSPC`)
  - Nasdaq (`^IXIC`)
  - Dow Jones (`^DJI`)

### Covered Sectors
- Technology
- Communication Services
- Consumer
- Financial Services
- Healthcare
- Energy
- Industrials

### Example Companies
- Apple (AAPL)
- Microsoft (MSFT)
- NVIDIA (NVDA)
- Alphabet (GOOGL)
- Meta (META)
- Amazon (AMZN)
- Tesla (TSLA)
- JPMorgan (JPM)
- Johnson & Johnson (JNJ)
- Exxon Mobil (XOM)

### Why These Data Are Suitable
These datasets are suitable for the analytical problem because they capture three essential dimensions of stock evaluation:

1. **Market performance** through price history and volume data  
2. **Financial condition** through core accounting and financial indicators  
3. **Current context** through company-specific and market-wide news  

Together, these sources allow users to move beyond isolated metrics and form a broader view of financial health and market sentiment.

---

## Python Workflow

The project follows a complete Python-based analytical workflow:

### 1. Data Retrieval
- Retrieve stock price history from Yahoo Finance
- Retrieve company financial information from Yahoo Finance
- Retrieve company news from Yahoo Finance
- Retrieve market news from Yahoo Finance via major indices

### 2. Fallback Loading
If Yahoo Finance retrieval fails or returns incomplete results:
- load local stock price CSV files
- load `financial_info.csv`
- load `company_news.csv`
- load `market_news.csv`

### 3. Data Cleaning
- convert date columns to datetime format
- standardise missing values such as `N/A`, blank strings, and null values
- convert selected financial fields into numeric format
- sort stock time series by date
- filter local stock data based on selected time period

### 4. Data Transformation
- calculate price change and percentage change
- calculate average trading volume
- calculate moving averages (20-day and 50-day)
- derive rule-based financial evaluation messages
- compute dimension scores and overall financial health score

### 5. Analysis
The dashboard evaluates four financial dimensions:
- Liquidity
- Solvency
- Profitability
- Growth

It then generates:
- dimension-level interpretations
- an overall score out of 100
- a qualitative rating (Excellent / Good / Moderate / Weak)

### 6. Visualisation
The product includes:
- stock closing price trend chart
- moving average overlays
- candlestick chart
- trading volume chart
- metric cards for price and financial indicators
- structured news display sections

### 7. Result Output
Users can:
- inspect key metrics directly in the dashboard
- view structured company and market news
- export the final analysis result as a CSV file

### Core Python Libraries
- `streamlit`
- `pandas`
- `yfinance`
- `plotly`
- `datetime`
- `os`

---

## Product Design and User Focus

This data product is designed with a strong user focus.

### Target Users
- students learning financial analysis
- beginner investors
- academic project evaluators
- users who need a simple overview of stock health without advanced modelling knowledge

### User-Centred Design Features
- **Sector-based company selection** for easier navigation
- **Simple sidebar controls** for period and chart options
- **Readable metric cards** for fast interpretation
- **Rule-based financial scoring** for explainability
- **News integration** to connect numbers with recent events
- **CSV fallback mechanism** for a more stable demo and user experience
- **Export function** for downstream reporting and comparison

### Why the Design Is Effective
The dashboard reduces user effort by combining multiple types of information in one place. Instead of searching separately for prices, ratios, and news, users can evaluate a company through one interactive workflow. This improves usability, interpretability, and demonstration value.

---

## Key Insights & Results

The project produces several useful analytical insights:

1. **Stock analysis becomes more meaningful when price data is combined with financial indicators.**  
   A company may show strong recent price growth while still having weaker liquidity or leverage conditions.

2. **Financial health is multi-dimensional rather than one-dimensional.**  
   Profitability, solvency, growth, and liquidity can tell different stories, so an overall score helps users balance these dimensions.

3. **News context adds important real-world interpretation.**  
   Company-specific and market-wide news help explain sudden price changes or shifts in investor attention that are not obvious from financial ratios alone.

4. **A fallback mechanism significantly improves product reliability.**  
   In testing, Yahoo Finance may occasionally return incomplete financial or news data, so local CSV support makes the dashboard more robust and presentation-ready.

5. **The dashboard is especially valuable for educational and exploratory use.**  
   It translates complex financial information into a user-friendly format without requiring users to understand advanced valuation models.

---

## How to Run

### 1. Environment Requirements
Recommended:
- Python 3.12.10

### 2. Install Dependencies
Run the following command in your terminal:
 `pip install streamlit yfinance pandas plotly`
If you use a requirements file, you may also run:
 `pip install -r requirements.txt`
### 3.Project structure

Make sure your project folder contains:

project_folder/
├── app.py
├── README.md
├── requirements.txt
├── notebook.ipynb
└── data/
    ├── AAPL.csv
    ├── MSFT.csv
    ├── NVDA.csv
    ├── financial_info.csv
    ├── company_news.csv
    └── market_news.csv
Note: Additional ticker CSV files can be included for broader fallback support.
### 4.RUN THE streamlit App

Use the following command:

`streamlit run app.py`

### 5.Reproducibility steps

To reproduce the dashboard successfully:

install all required libraries
place app.py in the project root directory
ensure the data/ folder contains the required fallback CSV files
run the Streamlit command above
open the local browser link generated by Streamlit
select a sector, company, and analysis period
click Run Analysis


### 6.Notes for Evaluators

The app first attempts live retrieval from Yahoo Finance.
If online retrieval fails, the app automatically switches to local CSV fallback sources.
This design ensures the app remains functional during marking and demonstration.

## Repository Contents
Main Files
app.py — final integrated Streamlit dashboard
notebook.ipynb — project notebook containing project explanation and supporting analysis
requirements.txt — package dependencies
README.md — project documentation
Data Folder
stock price CSV files for selected tickers
financial_info.csv
company_news.csv
market_news.csv

## Links
GitHub Repository: [https://github.com/xinchenwang2403/stock-financial-health-analyzer.git]
Demo Video: [https://video.xjtlu.edu.cn/Mediasite/Channel/556fdc2c32b340f58d12b8179e0284435f/headless/watch/658466a072194114b604ec9b3930ec2f1d]
Online App / Streamlit Link: [https://stock-financial-health-analyzer-9evatafgzn8fzejf8mexun.streamlit.app/]
If a public online app is not available, replace the third link with:
Online App / Streamlit Link: Not deployed publicly; please run locally using the instructions above.

## Limitations
This project has several limitations:

The financial health score is a rule-based simplified framework rather than a professional valuation or risk model.
Yahoo Finance data may occasionally be incomplete, delayed, or inconsistent.
Local fallback CSV files require manual maintenance and updating.
The dashboard currently covers a selected set of companies rather than the entire market.
News content is displayed descriptively, but no sentiment analysis or NLP classification is currently included.

## Future Improvements
Potential future improvements include:

adding more financial indicators such as ROE, free cash flow, and operating margin
comparing multiple companies side by side
introducing news sentiment analysis
automating fallback data updates
adding volatility and beta-based risk measures
expanding ticker coverage across more sectors and markets

## Author Information
Name:Xinchen.Wang
Student ID: 2470712
Course Code:ACC102
Track:Track 4

## AI Disclosure
This project used AI tools to support code refinement, debugging assistance, README drafting, and documentation improvement.

Tool used: OpenAI ChatGPT
Purpose of use:
improving Streamlit app integration
refining fallback logic design
drafting and polishing README/documentation
improving explanation clarity for notebook/report writing
Date(s) of use: [April 20/2026]
All final decisions, code integration, testing, and submission checking were completed by the author. AI assistance was used as a support tool and not as a substitute for the author's understanding or responsibility.

## Academic Integrity Note
All data sources used in this project are publicly accessible or locally prepared for educational use. External tools and AI support have been transparently disclosed above. This work is submitted in accordance with course academic integrity expectations.
