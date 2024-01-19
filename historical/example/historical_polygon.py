import requests
import pandas as pd
import configparser


def get_1min(symbol, start_date, end_date, save=True):
    config = configparser.ConfigParser()
    config.read(r'C:\Users\b_ban\Documents\VSCode\config\config.ini')
    api_key = config["POLYGON"]["API_KEY"]
    
    # Define the API endpoint and parameters
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/minute/{start_date}/{end_date}?adjusted=false&sort=asc&limit=50000&apiKey={api_key}"

    response = requests.get(url)
    df = pd.DataFrame(response.json()["results"])
    
    new_col_names = {
        'v': 'volume',
        'c': 'close',
        'h': 'high',
        'l': 'low',
        'o': 'open',
        't': 'datetime',
        'vw': 'vwap',
        'n': 'trades'
    }
    df = df.rename(columns=new_col_names)
    return df

   
if __name__ == '__main__':
    
    print(get_1min('BGLC', '2023-11-24', '2023-11-24'))