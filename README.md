# Stock Financial Health Analyzer

## Introduction

The **Stock Financial Health Analyzer** is a Streamlit-based web application developed for financial data exploration and basic company health assessment. The system allows users to select companies from multiple sectors, review historical stock price trends, examine key financial indicators, and obtain a simplified rule-based evaluation of financial health.

The application is designed to combine **market performance analysis** with **fundamental financial assessment** in an interactive dashboard. To improve reliability, the system first attempts to retrieve data from **Yahoo Finance** through the `yfinance` library and then automatically falls back to **local CSV files** if online data retrieval is unavailable or incomplete.

This project is intended for **educational and analytical purposes**. It provides users with a convenient way to understand selected financial indicators and their relationship to a company’s overall financial condition.

---

## Objectives

The main objectives of this project are:

- to build an interactive stock analysis dashboard using Streamlit;
- to visualize stock market trends for selected companies;
- to present important financial indicators in a clear and structured format;
- to provide a rule-based financial health evaluation framework;
- to improve robustness by using local CSV fallback data when online retrieval fails;
- to support export of analysis results for further review.

---

## Key Features

The application provides the following features:

### 1. Company Selection by Sector
Users can choose companies from several predefined sector categories, including:

- Technology
- Communication Services
- Consumer
- Financial Services
- Healthcare
- Energy
- Industrials

### 2. Historical Stock Price Analysis
The dashboard supports different time periods for analysis:

- 1 month
- 3 months
- 6 months
- 1 year
- 5 years
- 10 years

For the selected company, the system displays:

- latest closing price
- price change over the selected period
- percentage price change
- highest and lowest prices
- average trading volume

### 3. Interactive Visualizations
The application includes several visual components:

- closing price trend chart
- optional moving averages (20-day and 50-day)
- optional candlestick chart
- optional trading volume chart
- recent stock data table

### 4. Financial Indicator Analysis
The dashboard presents key financial metrics, including:

- Market Capitalization
- Trailing Price-to-Earnings Ratio (P/E)
- Revenue Growth
- Profit Margins
- Current Ratio
- Debt-to-Equity Ratio

### 5. Financial Health Evaluation
The project evaluates financial condition across four dimensions:

- **Liquidity**
- **Solvency**
- **Profitability**
- **Growth**

Each dimension is assessed using a simple rule-based approach, and the system generates an overall financial health score and rating.

### 6. Export Function
Users can download the current analysis result as a CSV file for reporting or further analysis.

### 7. Data Fallback Mechanism
A key strength of this project is its fallback strategy:

- online data is retrieved from Yahoo Finance when available;
- if online retrieval fails, the application uses local CSV files;
- this improves stability and reduces the impact of API errors or rate limiting.

---

## System Design

The system is organized around a single Streamlit application file, supported by local data files and optional helper scripts.

### Main Workflow

1. The user selects a sector and a company in the sidebar.
2. The user chooses an analysis period and optional chart settings.
3. After clicking **Run Analysis**, the application:
   - loads stock price history,
   - loads company financial information,
   - displays market overview metrics,
   - generates charts,
   - evaluates financial dimensions,
   - calculates an overall score,
   - enables CSV export.

---

## Financial Evaluation Logic

The project uses a simplified rule-based scoring framework to evaluate financial health.

### 1. Liquidity
Liquidity is assessed using the **Current Ratio**.

- A higher current ratio generally indicates stronger short-term payment ability.
- Companies with a current ratio above 1.5 are treated as having stronger liquidity.
- Companies with a current ratio below 1.0 may face short-term financial pressure.

### 2. Solvency
Solvency is assessed using the **Debt-to-Equity Ratio**.

- A lower debt-to-equity ratio suggests lower dependence on debt financing.
- A high value may indicate greater financial leverage and potential repayment risk.

### 3. Profitability
Profitability is assessed using **Profit Margins**.

- Higher profit margins suggest better cost control and stronger earnings capability.
- Low or negative margins indicate weaker profitability.

### 4. Growth
Growth is assessed using **Revenue Growth**.

- Positive revenue growth indicates business expansion.
- Negative growth may suggest declining sales performance.

### Scoring System
Each dimension contributes a score out of **25 points**.  
The total possible overall score is **100 points**.

### Rating Categories

- **85–100**: Excellent
- **70–84**: Good
- **50–69**: Moderate
- **Below 50**: Weak

If some indicators are unavailable, the application adjusts the scoring logic based on the available dimensions.

---

## Data Sources

This project uses the following data sources:

### Online Source
- **Yahoo Finance**, accessed through the `yfinance` Python package

### Local Fallback Source
- Local stock price CSV files stored in the `data/` folder
- A local `financial_info.csv` file containing company financial indicators

The fallback mechanism is especially useful when Yahoo Finance returns incomplete data or blocks requests due to rate limiting.

---

## Technologies Used

The project was implemented using the following tools and libraries:

- **Python**
- **Streamlit**
- **Pandas**
- **yfinance**
- **Plotly**
- **OS module**

---

## Project Structure


stock-financial-health-analyzer/
│
├── app.py
├── build_financial_info.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── data/
    ├── financial_info.csv
    └── optional stock CSV files (e.g. AAPL.csv, MSFT.csv)

# File Description
app.py
Main Streamlit application containing the dashboard logic, data loading process, evaluation functions, chart generation, and export functionality.

build_financial_info.py
Helper script used to generate or prepare the local financial information file.

data/financial_info.csv
Local fallback file containing financial indicators for supported companies.

data/{ticker}.csv
Optional fallback files containing local historical stock price data.

requirements.txt
List of required Python packages.

README.md
Project documentation.  

# Installation
Step 1: Clone the Repository

git clone https://github.com/your-username/stock-financial-health-analyzer.git
cd stock-financial-health-analyzer
Step 2: Install Dependencies

pip install -r requirements.txt

# Running the Application
To launch the Streamlit dashboard, run:


streamlit run app.py
If streamlit is not recognized in your environment, use:


python -m streamlit run app.py
After running the command, Streamlit will provide a local URL in the terminal. Open the link in a web browser to use the application.

# Example Use Case
A user may choose:

Sector: Technology
Company: Apple Inc. (AAPL)
Period: 6 months
The system will then display:

market overview statistics,
historical stock price charts,
optional candlestick and volume charts,
key financial indicators,
financial health interpretation,
overall score and rating,
downloadable CSV result.

# Reliability and Error Handling
To improve usability and reliability, the system includes the following mechanisms:

caching of loaded data to reduce repeated API requests;
fallback from Yahoo Finance to local CSV files;
explicit error messages when both online and local data are unavailable;
handling of missing values in financial indicators;
display of data source status to inform the user whether the data came from Yahoo Finance or local files.
These design choices help maintain application stability and transparency.

# Limitations
Although the dashboard is functional and informative, several limitations should be noted:

some financial indicators may be unavailable for certain companies;
Yahoo Finance data retrieval may be restricted by rate limits or temporary access issues;
the scoring method is simplified and rule-based rather than statistically or academically validated;
the application focuses on a limited set of companies and sectors;
the project is intended for educational use and should not be interpreted as professional investment advice.
Future Improvements
Potential future improvements for this project include:

expanding the number of supported companies;
adding more financial ratios and valuation metrics;
introducing technical indicators such as RSI or MACD;
enabling company-to-company comparison;
improving the scoring model with more advanced financial methodology;
integrating database storage instead of only CSV files;
deploying the project online for public access.
# Conclusion
The Stock Financial Health Analyzer demonstrates how financial market data and company fundamentals can be integrated into an interactive analytical dashboard. The project combines stock trend visualization, financial indicator reporting, rule-based assessment, and CSV export within a user-friendly interface.

By incorporating both online retrieval and local fallback data, the application also addresses a practical issue in financial application development: maintaining system reliability when third-party data services are unstable.

Overall, this project provides a useful educational example of how Python and Streamlit can be used to build an accessible and interpretable financial analysis tool.

# Author
Developed as an academic project for educational purposes.

# License
This project is intended for academic and non-commercial educational use only.
