# ChatGPT Query Generator

This code provides a command-line interface for collecting and analyzing stock market data, as well as generating queries for Language Models such as ChatGPT. 

<hr>
<b>Disclaimer:</b>
This code is not meant to be used for trading or investment purposes. It is meant for educational purposes only.
No investment advice is provided or implied. The author is not responsible for any losses or gains that may occur from using this software or parts thereof. <br />
Respect the licences.
<hr>
However, if you find this code useful, please consider thinking of me :-)

## Overview
The main purpose of this code is to provide a command-line interface to collect and analyze stock market data. 
It has various commands and subcommands for collecting stock market data, market indicators, news articles, 
and stock indicators. Additionally, it has a command to generate a query meant for ChatGPT (or generally LLM) query based on the data collected.
### Information Included in the Query
- Stock Symbol Trend Information (open, closes, volume etc.) in different resolutions (fetched from `yfinance`)
- Basic Stock Info as in eps, 52 week high / low, market cap, sector etc.  (fetched from `yfinance`)
- Market Indicators (e.g. unemployment rate, inflation rate; over 20 at the time of writing) (fetched from the FRED API; see below)
- Technical Indicators (e.g. RSI, MACD, Bollinger Bands etc.) calculated using `TA-Lib` (based on the stock trend information)
- News Articles headlines (fetched from the News API; see below) 
- an example prompt for ChatGPT / LLMs for analysing the stock
### General Workflow
The workflow is generally as follows:<br /><br />
**Once per day:**
1. Collect stock market data you are interested in using the `symbols collect` command.
2. Collect market indicators data using the `market-indicators update` command .
3. Collect news articles using the `news update` command.
4. Calculate stock indicators using the `stock-indicators update` command. <br /> <br />
As often as you want:<br />
5. Generate a ChatGPT query using the `query generate` command.
#### **Shortcut / TLDR**
If you want to go the easy road, just use as follows (example for Microsoft Stock) after installing the dependencies:
```bash
STOCKGPT_NEWS_API_KEY=... STOCKGPT_FRED_API_KEY... python stock_gpt.py query generate --symbol MSFT --update-symbol
```
This will update everything related to the symbol and generate a query for it. Be aware you do not have to update
the symbol every time. You can use specific commands to update your repository as described below.
### Sharing is caring
Feel free to modify the query and feed back results that work best for you. We are all learning.
## Setup
### Clone the Repository
First, clone or download the repository, e.g.:
```bash
git clone https://github.com/Mereep/stock-gpt.git
```
### Install Dependencies
This setup assumes you have Python 3.10+ installed. Older versions of Python may work, but are not tested. You can install Python from the official website: https://www.python.org/downloads/
However, I recommend using a package manager such as `pyenv` or `conda` to install Python (see: https://realpython.com/intro-to-pyenv/ and https://docs.conda.io/en/latest/miniconda.html)
Before using this code, make sure to install the required libraries and packages for your Python versions listed in the requirements.txt file. You can do this by running:
```bash 
pip install -r requirements.txt
```
or any package manager of your choice.
When running into a problem with installing `TA-Lib`, you may need specific headers in place.
For example, on Ubuntu, you can install the headers by running:
```bash
sudo apt-get install libta-lib-dev
```
or on MacOS:
```bash
brew install ta-lib
```

### Environment Setup
The following environment variables are required for running the commands. You'll need to obtain API keys for the FRED API and the News API. See the links below for more details.
Please **do** respect their terms of use and do not abuse their services.
<table>
    <thead>
        <th>
            KEY
        </th>
        <th>
            Description
        </th>
    </thead>
    <tbody>
        <tr>
            <td>
                STOCKGPT_FRED_API_KEY
            </td>
            <td>
                API for fetching market indicators. See:
                <a href="https://research.stlouisfed.org/docs/api/api_key.html">FRED API Key</a>
            </td>
        </tr>
        <tr>
            <td>
                STOCKGPT_NEWS_API_KEY
            </td>
            <td>
                API for fetching news articles. See:
                <a href="https://newsapi.org/docs/get-started">News API</a>
            </td>
        </tr>
    </tbody>
</table>

## Commands
All commands are meant to run using `python stock_gpt.py [command]`
Make sure you add the needed API keys to the environment variables before running the commands.
(see the Setup section for more details).
Concretly, all commands are to be run in the schema:
```bash
STOCKGPT_NEWS_API_KEY=... STOCKGPT_FRED_API_KEY... python stock_gpt.py [command] [subcommand] [options]
```
### Collect Command

The symbols command collects and updates stock market data using `yfinance`.
<br />**Usage:**

```bash
symbols collect [--symbol SYMBOL [SYMBOL ...]] [--start START_DATE] [--end END_DATE]
```
    --symbol: The stock symbols to collect data for. If not provided, all symbols will be updated.
    --start: The start date for collecting data in the format YYYY-MM-DD. Defaults to 365 days before the current date.
    --end: The end date for collecting data in the format YYYY-MM-DD. Defaults to the current date.
### Market Indicators Command

The market-indicators command collects and updates market indicators data using the `fredAPI`.


```bash
market-indicators update [--indicator INDICATOR [INDICATOR ...]] [--start START_DATE] [--end END_DATE]
```
    --indicator: The list of market indicators to collect data for. Defaults to the indicators specified in the configuration file.
    --start: The start date for collecting data in the format YYYY-MM-DD. Defaults to None.
    --end: The end date for collecting data in the format YYYY-MM-DD. Defaults to None.

### News Command

The news command collects and updates news articles data using the `newsapi`.
**Usage:**:

```bash
news update [--symbol SYMBOL [SYMBOL ...]] [--page-size PAGE_SIZE]
```
    --symbol: The list of stock symbols to collect news articles for. If not provided, all symbols will be updated.
    --page-size: The number of news articles to collect per symbol. Defaults to 15.

### Stock Indicators Command

The stock-indicators command calculates and updates stock indicators for existing stock market data.
(use the collect command to collect stock market data first).

**Usage:**:
```bash
stock-indicators update
```

### Query Command

The query command generates a ChatGPT query based on the given parameters.
**Usage:**

```bash
query generate --symbol [--update_symbol UPDATE_SYMBOL] [--market_indicators_max_value_count MAX_VALUE_COUNT] [--stock_indicators_max_age MAX_AGE] [--stock_values_max_age MAX_AGE] [--max_news_age MAX_AGE] [--day DAY]
```
    --symbol: The stock symbol for the query. Required. 
    --update-symbol: Whether to update the stock symbol data before generating the query. Defaults to False.
    --market-indicators-max-value-count: The maximum number of market indicator values to consider. Defaults to 3.
    --stock-indicators-max-age: The maximum age of stock indicators in days. Defaults to 3.
    --stock-values-max-age: The maximum age of stock values in days. Defaults to 31.
    --max-news-age: The maximum age of news articles in days. Defaults to 7.
    --day: The date in the format `YYYY-MM-DD` for the query. Defaults to the current date.
    --top-clipboard: Whether to copy the generated query to the clipboard. Defaults to False. 
## Examples
- Collect / Update specific stock symbols (e.g., AAPL and MSFT) with data from the last 30 days: 
```bash
python stock_gpt.py symbols collect --symbol AAPL MSFT --start 2023-03-12 --end 2023-04-12
```
Update all stock symbols with data from the last year: 
```bash
python stock_gpt.py symbols collect`
``` 
Update all market indicators:
```bash
python stock_gpt.py market-indicators update`
```
Calculate and update stock indicators
```bash
python stock_gpt.py stock-indicators update`
```
Update news articles for specific stock symbols (e.g., AAPL and MSFT)
```bash
python stock_gpt.py news update --symbol AAPL MSFT`
```
- Generate a ChatGPT query with custom parameters
```bash
python stock_gpt.py query generate --market_indicators_max_value_count 5 --stock_indicators_max_age 7 --stock_values_max_age 60 --max_news_age 14 --day 2023-04-10`
```

## Contribute
If you'd like to contribute: You're welcome :-)<br />
Here is much to do, for example:
- Unit Tests (yay, no Tests yet)
- Prompt improvements
  - which data to include?
  - how much data?
  - how to format the data?
  - what to ask?
  - different prompt goals (expected answers)
  - potentially take different LLMs into Account
- A graphical User Interface
- Linting, Style Guides, etc.
- Different data repositories (we only have CSV atm.)
- Different data sources (how about article summaries etc?)
- New indicators (market, stock (technical), fundamental
- Other opinion sources (reddit, twitter, etc.)
- Installation / setup
- CI (bundle to executables ?)
- ...
## Appendix
### Data
The data is stored in the `data` directory. There are several subdirectories:
- `defaults`: Includes `.csv`-files:
  - `stock_indicators.csv` used for calculating. You may want to change this files to 
  include / remove indicators. However, when adding indicators you must implement the extractors (see: `src/stock_indicators/indicator_impl.py`). 
  Use ChatGPT if you need help ;). 
  - It Also includes a `market_indicators.csv` file with the market indicators used in the project. 
  Those must be fetchable using the FRED API (see: https://fred.stlouisfed.org/docs/api/fred/).
- `stock_data`: Repositories for all the stuff collected and calculated. You can delete the `.csv`-files within the subdirectories
and re-collect all the data if needed.

### Market indicators
Overview of some of the Market Indicators used in the project:
<table>
  <thead>
    <tr>
      <th>Indicator</th>
      <th>Description</th>
      <th>Best Investment Horizon</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>GDP</code></td>
      <td>Gross Domestic Product is the total value of goods and services produced in a country over a specific time period. It's a key indicator of economic activity and growth.</td>
      <td>Long-term</td>
    </tr>
    <tr>
      <td><code>UNRATE</code></td>
      <td>Unemployment Rate is the percentage of the labor force that is currently unemployed. It's used to track changes in the labor market and is considered a lagging indicator of economic growth.</td>
      <td>Long-term</td>
    </tr>
    <tr>
      <td><code>CPIAUCSL</code></td>
      <td>Consumer Price Index for All Urban Consumers is a measure of the average change in prices paid by urban consumers for a basket of goods and services. It's used to track changes in inflation and is considered a leading indicator of interest rates.</td>
      <td>Short-term</td>
    </tr>
    <tr>
      <td><code>FEDFUNDS</code></td>
      <td>Federal Funds Rate is the interest rate at which banks and other depository institutions lend money to each other overnight. It's set by the Federal Reserve and is a key tool used to influence the economy.</td>
      <td>Short-term</td>
    </tr>
    <tr>
      <td><code>ISM_MFR_PMI</code></td>
      <td>Purchasing Managers' Index for Manufacturing is a measure of the economic activity in the manufacturing sector. It's based on a survey of purchasing managers and is used to track changes in production, employment, and prices.</td>
      <td>Short-term</td>
    </tr>
    <tr>
      <td><code>UMCSENT</code></td>
      <td>University of Michigan Consumer Sentiment Index is a measure of consumer confidence based on a survey of households. It's used to track changes in consumer spending and is considered a leading indicator of economic growth.</td>
      <td>Short-term</td>
    </tr>
    <tr>
      <td><code>HMI</code></td>
      <td>National Association of Home Builders Housing Market Index is a measure of homebuilder confidence based on a survey of industry professionals. It's used to track changes in the housing market and is considered a leading indicator of economic growth.</td>
      <td>Short-term</td>
    </tr>
    <tr>
      <td><code>VIXCLS</code></td>
      <td>CBOE Volatility Index is a measure of the expected volatility of the S&P 500 Index over the next 30 days. It's often referred to as the "fear index" and is used to gauge investor sentiment and market risk.</td>
      <td>Short-term</td>
    </tr>
    <tr>
      <td><code>SP500ADL</code></td>
      <td>S&P 500 Advance-Decline Line is a measure of the number of stocks that are advancing or declining in price in the S&P 500 Index. It's used to track changes in market breadth, which can provide insights into market trends and investor sentiment.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>T10Y2Y</code></td>
<td>Treasury Yield Curve Spread is a measure of the difference between long-term and short-term interest rates. It's often used as an indicator of economic growth and recession risk, as well as a gauge of investor sentiment and market risk.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>INDPRO</code></td>
<td>Industrial Production Index is a measure of the output of the industrial sector of the economy. It's used to track changes in production and is considered a leading indicator of economic growth.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>TCU</code></td>
<td>Total Capacity Utilization is a measure of the percentage of industrial capacity that is currently in use. It's used to track changes in production and is considered a leading indicator of economic growth.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>RSAFS</code></td>
<td>Retail Sales of Goods is a measure of the total sales of goods by retailers. It's used to track changes in consumer spending and is considered a leading indicator of economic growth.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>DGORDER</code></td>
<td>Durable Goods Orders is a measure of the total orders for long-lasting goods by manufacturers. It's used to track changes in production and is considered a leading indicator of economic growth.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>HOUST</code></td>
<td>New Residential Construction is a measure of the number of new housing units that are started each month. It's used to track changes in the housing market and is considered a leading indicator of economic growth.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>HSN1F</code></td>
<td>New Home Sales is a measure of the number of new homes that are sold each month. It's used to track changes in the housing market and is considered a leading indicator of economic growth.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>MANEMP</code></td>
<td>Employment in Manufacturing is a measure of the number of people employed in the manufacturing sector. It's used to track changes in employment and is considered a leading indicator of economic growth.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>PCUAD--AD--AD</code></td>
<td>Producer Price Index for All Commodities is a measure of the average change in prices received by producers for goods and services. It's used to track changes in inflation and is considered a leading indicator of interest rates.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>NAPMNONMFG</code></td>
<td>Purchasing Managers' Index for Non-Manufacturing is a measure of the economic activity in the non-manufacturing sector. It's based on a survey of purchasing managers and is used to track changes in production, employment, , and prices in industries such as retail, construction, and services.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>SPCS20RSA</code></td>
<td>S&P Case-Shiller 20-City Composite Home Price Index is a measure of the average change in home prices in 20 major metropolitan areas. It's used to track changes in the housing market and is considered a leading indicator of economic growth.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>M2SL</code></td>
<td>M2 Money Stock is a measure of the total amount of money in circulation in the economy. It's used to track changes in the money supply and is considered a leading indicator of economic growth.</td>
<td>Long-term</td>
</tr>
<tr>
<td><code>WTISPLC</code></td>
<td>West Texas Intermediate Spot Price is a measure of the price of oil in the spot market. It's used to track changes in energy prices and is considered a leading indicator of inflation and economic growth.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>EXUSEU</code></td>
<td>U.S. / Euro Foreign Exchange Rate is a measure of the value of the U.S. dollar relative to the euro. It's used to track changes in currency exchange rates and is considered a leading indicator of international trade and economic growth.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>EXJPUS</code></td>
<td>U.S. / Japanese Yen Foreign Exchange Rate is a measure of the value of the U.S. dollar relative to the Japanese yen. It's used to track changes in currency exchange rates and is considered a leading indicator of international trade and economic growth.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>EXCAUS</code></td>
<td>Canadian Dollar / U.S. Dollar Foreign Exchange Rate is a measure of the value of the Canadian dollar relative to the U.S. dollar. It's used to track changes in currency exchange rates and is considered a leading indicator of international trade and economic growth.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>EXUSUK</code></td>
<td>U.S. / U.K. Foreign Exchange Rate is a measure of the value of the U.S. dollar relative to the British pound. It's used to track changes in currency exchange rates and is considered a leading indicator of international trade and economic growth.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>BAMLH0A0HYM2</code></td>
<td>BofA Merrill Lynch U.S. High Yield Master II Option-Adjusted Spread is a measure of the yield spread over U.S. Treasury bonds for high-yield corporate bonds. It's used to track changes in credit risk and is considered a leading indicator of economic growth.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>BAMLH0A0HYM2EY</code></td>
<td>BofA Merrill Lynch U.S. High Yield Master II Effective Yield is a measure of the average yield on U.S. high-yield corporate bonds. It's used to track changes in credit risk and is considered a leading indicator of economic growth.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>BAMLHE00EHYIOAS</code></td>
<td>BofA Merrill Lynch U.S. Corporate Master Option-Adjusted Spread is a measure of the yield spread over U.S. Treasury bonds for investment-grade corporate bonds. It's used to track changes in credit risk and is considered a leading indicator of economic growth.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>BAMLHE00EHYIOA</code></td>
<td>BofA Merrill Lynch U.S. Corporate Master Effective Yield is a measure of the average yield on U.S. investment-grade corporate bonds. It's used to track changes in credit risk and is considered a leading indicator of economic growth.</td>
<td>Short-term</td>
</tr>
<tr>
<td><code>TEDRATE</code></td>
<td>TED Spread is a measure of the difference between the interest rates on interbank loans and short-term U.S. government debt. It's used to track changes in credit risk and is considered a leading indicator of economic growth and financial stability.</td>
<td>Short-term</td>
</tr>
  </tbody>
</table>
