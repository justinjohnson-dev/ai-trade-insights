"""File for testing and playing around with code - polygon.io API"""

# polygon_functions.py
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from polygon import RESTClient

from app.utils.app_logger import app_logger

load_dotenv()

# Replace 'YOUR_API_KEY' with your Polygon.io API key
API_KEY = os.getenv("POLYGON_API_KEY")  # type: ignore


def fetch_all_us_stock_tickers(client):
    """Fetches all US stock tickers."""
    app_logger.info("Fetching all US stock tickers...")
    tickers = client.list_tickers(market="stocks", active=True, limit=1000)
    app_logger.info("First 10 US stock tickers:")
    for i, ticker in enumerate(tickers):
        if i >= 10:
            break
        app_logger.info("%s: %s", ticker.ticker, ticker.name)


def fetch_two_years_historical_data(client, ticker):
    """Fetches 2 years of historical data for the given ticker."""
    app_logger.info("Fetching 2 years of historical data for %s...", ticker)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=2 * 365)
    aggs = client.get_aggs(
        ticker=ticker,
        multiplier=1,
        timespan="day",
        from_=start_date.strftime("%Y-%m-%d"),
        to=end_date.strftime("%Y-%m-%d"),
        adjusted=True,
        sort="asc",
        limit=5000,
    )

    # Check if the fetched data is empty
    if not aggs:
        app_logger.info(
            "No historical data found for ticker: %s. Please check if the ticker is valid.",
            ticker,
        )
        return []  # Return an empty list if no data is found

    app_logger.info(
        "Number of days fetched: %d", len(aggs)
    )  # Changed to lazy formatting
    app_logger.info("First 5 days of data:")
    for agg in aggs[:5]:
        date = datetime.fromtimestamp(agg.timestamp / 1000).date()
        app_logger.info("Date: %s, Close: %s", date, agg.close)  # Use lazy formatting
    return aggs  # Return data for use in other functions


def fetch_end_of_day_data(client, ticker="SPY"):
    """Fetches end-of-day data for the given ticker."""
    app_logger.info("\nFetching end-of-day data for %s...", ticker)
    previous_close = client.get_previous_close(ticker, adjusted=True)
    for pc in previous_close.results:
        date = datetime.fromtimestamp(pc["t"] / 1000).date()
        app_logger.info("Date: %s, Close: %s", date, pc["c"])


def fetch_reference_data(client, ticker="SPY"):
    """Fetches reference data for the given ticker."""
    app_logger.info("\nFetching reference data for %s...", ticker)
    ticker_details = client.get_ticker_details(ticker)
    app_logger.info("Name: %s", ticker_details.name)
    app_logger.info("Market: %s", ticker_details.market)
    app_logger.info("Locale: %s", ticker_details.locale)
    app_logger.info("Primary Exchange: %s", ticker_details.primary_exchange)
    app_logger.info("Type: %s", ticker_details.type)
    app_logger.info("Active: %s", ticker_details.active)


# def fetch_fundamentals_data(client, ticker="SPY"):
#     """Fetches fundamental data for the given ticker."""
#     app_logger.info(f"\nFetching fundamental data for {ticker}...")

#     try:
#         # Correct method to fetch financials
#         financials = client.reference_stock_financials(symbol=ticker, limit=1, type="Q")

#         if financials and financials.results:
#             fin = financials.results[0]
#             app_logger.info(f"Ticker: {fin['ticker']}")
#             app_logger.info(f"Period: {fin['period']}")
#             app_logger.info(f"Calendar Date: {fin['calendar_date']}")
#             income_statement = fin["financials"]["income_statement"]
#             app_logger.info(f"Total Revenue: {income_statement.get('total_revenue')}")
#             app_logger.info(f"Net Income: {income_statement.get('net_income')}")
#         else:
#             app_logger.info("No fundamental data available for this ticker.")
#     except Exception as e:
#         app_logger.info(f"An error occurred: {e}")


def fetch_corporate_actions(client, ticker="SPY"):
    """Fetches corporate actions for the given ticker."""
    app_logger.info("\nFetching corporate actions for %s...", ticker)
    corporate_actions = client.get_corporate_actions(
        ticker=ticker, ca_types=["Dividend", "Split"], limit=10
    )
    if corporate_actions.results:
        for ca in corporate_actions.results:
            app_logger.info(
                "Type: %s, Effective Date: %s, Details: %s",
                ca.ca_type,
                ca.effective_date,
                ca.details,
            )
    else:
        app_logger.info("No corporate actions found for this ticker.")


def calculate_technical_indicators(aggs, period=45):
    """Calculates technical indicators such as Simple Moving Average."""
    app_logger.info("\nCalculating technical indicators...")
    closes = [agg.close for agg in aggs]
    if len(closes) >= period:
        sma = sum(closes[-period:]) / period
        app_logger.info("%d-day SMA for SPY: %f", period, sma)
        return sma
    else:
        app_logger.info("Not enough data to calculate SMA.")


def fetch_minute_aggregates(client, ticker="SPY"):
    """Fetches minute-level aggregates for the given ticker."""
    app_logger.info("\nFetching minute aggregates for %s...", ticker)
    end_date = datetime.now()
    start_date = (end_date - timedelta(days=1)).strftime("%Y-%m-%d")
    minute_aggs = client.get_aggs(
        ticker=ticker,
        multiplier=1,
        timespan="minute",
        from_=start_date,
        to=end_date.strftime("%Y-%m-%d"),
        adjusted=True,
        sort="asc",
        limit=5000,
    )
    app_logger.info("Number of minute aggregates fetched: %d", len(minute_aggs))
    app_logger.info("First 5 minute aggregates: %s", minute_aggs[:5])


def main():
    # Initialize the REST client
    client = RESTClient(API_KEY)

    # 1. Fetch all US stock tickers
    # fetch_all_us_stock_tickers(client)

    # 2. Fetch 2 years of historical data for SPY
    aggs = fetch_two_years_historical_data(client, ticker="SPY")

    # 3. Fetch end-of-day data for SPY
    # fetch_end_of_day_data(client, ticker="SPY")

    # 4. Fetch reference data for SPY
    # fetch_reference_data(client, ticker="SPY")

    # 5. Fetch fundamentals data for SPY
    # fetch_fundamentals_data(client, ticker="SPY")

    # # 6. Fetch corporate actions for SPY
    # fetch_corporate_actions(client, ticker="SPY")

    # 7. Calculate technical indicators for SPY
    calculate_technical_indicators(aggs)

    # 8. Fetch minute aggregates for SPY
    # fetch_minute_aggregates(client, ticker="SPY")


if __name__ == "__main__":
    main()
