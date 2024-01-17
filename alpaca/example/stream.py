import configparser
import threading
import pandas as pd
import time
from alpaca.data.live import StockDataStream
from alpaca.data.enums import DataFeed

config = configparser.ConfigParser()
config.read(r'C:\Users\b_ban\Documents\VSCode\Youtube\alpaca\config.ini')

api_key = config['ALPACA']['API_KEY']
api_secret = config['ALPACA']['API_SECRET']
base_url = 'https://api.alpaca.markets'  # Use 'https://paper-api.alpaca.markets' for paper trading

# Process data
def update_min_chart(data):
    #print(data)
    timestamp = pd.to_datetime(data['t'].seconds, unit='s', utc=True)
    timestamp = timestamp.tz_convert('US/Eastern')
    symbol = data['S']
    price = float(data['p'])
    size = int(data['s'])
    conditions = data['c']

    # Avoid list, not valid trades and will skew charts
    # U	Extended Hours Sold (Out Of Sequence)
    # H	Price Variation Trade
    # L	Sold Last (Late Reporting)
    # Z	Sold (Out Of Sequence)

    print(timestamp, symbol, price, size, conditions)

# Run Alpaca Time Sale stream in a separate thread
def run_time_sale_stream(symbols):
    # Process messages
    async def on_time_sale_message(message):
        update_min_chart(message)

    # Connect to the Alpaca Time Sale stream
    conn = StockDataStream(api_key, api_secret, base_url, feed=DataFeed.SIP)
    conn.subscribe_trades(on_time_sale_message, *symbols)
    conn.run()

# Start the Alpaca Time Sale stream in a separate thread
symbol_to_watch = ['PHUN', 'DATS', 'DWAC', 'CNEY']
time_sale_thread = threading.Thread(target=run_time_sale_stream, args=(symbol_to_watch,))
time_sale_thread.start()

# Main thread can continue to do other tasks or run indefinitely
while True:
        time.sleep(1)

