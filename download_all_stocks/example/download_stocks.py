import sys
sys.path.append('../../')  # Add the parent directory to the sys.path
from pyodbc_.example.save_daily import save_daily
from historical.example.alpaca import get_daily
import configparser
import requests
import json


config = configparser.ConfigParser()
config.read(r'C:\Users\b_ban\Documents\VSCode\config\config.ini')

api_key = config['ALPACA']['API_KEY']
api_secret = config['ALPACA']['API_SECRET']
base_url = 'https://api.alpaca.markets'  

def get_listed_stocks():
    '''
    Get alpaca supported stock symbols.
    Remove symbols with ".", ex: FUSE.U
    '''
    url = "https://paper-api.alpaca.markets/v2/assets?asset_class=us_equity&exchange=AMEX%2C%20NYSE%2C%20NASDAQ&attributes="

    headers = {
        "accept": "application/json",
        "APCA-API-KEY-ID": api_key,
        "APCA-API-SECRET-KEY": api_secret
    }

    response = requests.get(url, headers=headers)
    resp_json = json.loads(response.text) 

    symbols = []
    for row in resp_json:
        symbol = row['symbol']
        if ('.' not in symbol
            and (not any(x in row['name'] for x in ['ETN', 'ETF']))
            and not any(char.isdigit() for char in symbol)
            ):
            if '_DELISTED' in symbol:
                symbol = symbol.replace('_DELISTED', '')
            symbols.append(symbol)
    symbols.sort()
    return(symbols)

def save_all_daily():
    symbols = get_listed_stocks()
    symbols_len = len(symbols)

    count = 0
    for symbol in symbols:
        count+=1
        try:
            print(symbols_len, str(count)+': ', symbol)
            daily_df = get_daily(symbol)
            save_daily(symbol, daily_df)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    #symbols = get_listed_stocks()
    #print(symbols)
    save_all_daily()

