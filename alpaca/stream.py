
import configparser
import threading
import pandas as pd
from alpaca_trade_api.rest import REST
from alpaca_trade_api.stream import Stream
import time

config = configparser.ConfigParser()
config.read(r'C:\Users\b_ban\Documents\VSCode\Youtube\alpaca\config.ini')

api_key = config['ALPACA']['API_KEY']
api_secret = config['ALPACA']['API_SECRET']
base_url = 'https://api.alpaca.markets'  # Use 'https://paper-api.alpaca.markets' for paper trading

api = REST(api_key, api_secret, base_url, api_version='v2')

# Initialize a1min chart dataframe (replace this with your actual initialization logic)
min_chart = pd.DataFrame(columns=['timestamp', 'symbol', 'price', 'size', 'conditions'])

# Process data
def update_min_chart(data):
    # Extract relevant data from the message
    print(data)
    timestamp = pd.to_datetime(data.timestamp)
    symbol = data.symbol
    price = float(data.price)
    size = int(data.size)
    conditions = data.conditions

# Function to run Alpaca Time Sale stream in a separate thread
def run_time_sale_stream(symbols):
    # Function to process each message from the Time Sale stream
    async def on_time_sale_message(data):
        # Update the a1min chart dataframe
        update_min_chart(data)

    # Connect to the Alpaca Time Sale stream
    conn = Stream(api_key, api_secret, base_url, data_feed='sip')
    conn.subscribe_trades(on_time_sale_message, *symbols)
    conn.run()

# Start the Alpaca Time Sale stream in a separate thread
symbol_to_watch = ['BETS', 'VIEW', 'EYPT']  # Replace with the symbol you want to watch
time_sale_thread = threading.Thread(target=run_time_sale_stream, args=(symbol_to_watch,))
time_sale_thread.start()

# Main thread can continue to do other tasks or run indefinitely
while True:
    #with a1min_chart_lock:
        #print(a1min_chart)  # Replace this with your actual processing logic
        time.sleep(1)

