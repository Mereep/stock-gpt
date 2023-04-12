from datatypes.stock_info import StockInfo
import yfinance as yf


def fetch_basic_stock_info(symbol: str) -> StockInfo:
    ticker = yf.Ticker(symbol)
    info = ticker.info

    return StockInfo(
        name=info.get("longName"),
        sectors=info.get("sector") if isinstance(info.get("sector"), list) else [info.get("sector")],
        market_cap=info.get("marketCap"),
        pe_ratio=info.get("trailingPE"),
        dividend_yield=info.get("dividendYield"),
        beta=info.get("beta"),
        high_52_week=info.get("fiftyTwoWeekHigh"),
        low_52_week=info.get("fiftyTwoWeekLow"),
        eps=info.get("trailingEps")
    )