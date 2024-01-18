from alpaca.data.historical import stock
from alpaca.common.enums import Sort
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, date, timedelta
import pandas as pd
import configparser


def get_daily(symbol):
    config = configparser.ConfigParser()
    config.read(r'C:\Users\b_ban\Documents\VSCode\config\config.ini')
    api_key = config["ALPACA"]["API_KEY"]
    api_secret = config["ALPACA"]["API_SECRET"]

    # Get daily data for the specified stock and date range
    start_date = date.today() - timedelta(days=30)
    api = stock.StockHistoricalDataClient(api_key=api_key, secret_key=api_secret)

    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=start_date,
        #end=end,
        limit=None,
        sort=Sort.DESC,
    )

    chart_resp = api.get_stock_bars(request)

    # Initialize empty lists to store data
    datetimes = []
    opens = []
    highs = []
    lows = []
    closes = []
    volumes = []

    #print(chart_resp)
    #print(chart_resp[symbol])

    # Extract data from bars and append to lists
    for bar in chart_resp[symbol]:
        print(bar)
        dt = pd.to_datetime(bar.timestamp, utc=True).tz_convert('US/Eastern')
        datetimes.append(dt)
        opens.append(bar.open)
        highs.append(bar.high)
        lows.append(bar.low)
        closes.append(bar.close)
        volumes.append(bar.volume)

    # Create a Pandas DataFrame
    data = {
        'datetime': datetimes,
        'open': opens,
        'high': highs,
        'low': lows,
        'close': closes,
        'volume': volumes
    }

    chart_df = pd.DataFrame(data)
    return chart_df

if __name__ == "__main__":
    print(get_daily('TSLA'))