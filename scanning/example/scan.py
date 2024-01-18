import configparser
from pytz import timezone
import time
from datetime import datetime
import requests
import json
import pprint


class ScanStocks():
    def __init__(self):
        # Load config
        self.config = configparser.ConfigParser()
        self.config.read(r'C:\Users\b_ban\Documents\VSCode\config\config.ini')
        self.poly_api_key = self.config["POLYGON"]["API_KEY"]
        self.snapshot_url = f'https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers?apiKey={self.poly_api_key}'

        self.eastern_tz = timezone('US/Eastern')
        self.min_price = .15
        self.min_gain_pct = 20


    def gainer_scan(self):
        '''
        Scan for gainers.
        '''
        gainers = []

        resp = requests.get(self.snapshot_url)
        if resp.status_code == 200:
            resp_json = json.loads(resp.text)
            today = datetime.now().date()
            for ticker in resp_json['tickers']:
                # Volume shows after 9:30
                if (ticker['todaysChangePerc'] > self.min_gain_pct and ticker['day']['v'] > 3 * 1000000):
                    gainers.append([today, 
                                    ticker['ticker'], 
                                    ticker['min']['c'], 
                                    ticker['todaysChangePerc'], 
                                    self.min_gain_pct and ticker['day']['v']])
            pprint.pprint(gainers)
    

    def run_scans(self):
        '''
        Loop scan all day.
        '''
        print('running scans')
        while True:
            self.gainer_scan()
            time.sleep(5 * 60)

def main():
    scan = ScanStocks()
    #scan.gainer_scan()
    scan.run_scans()

if __name__ == '__main__':
    main()
    