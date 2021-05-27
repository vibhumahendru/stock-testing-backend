import requests
import json
from django.conf import settings

exchanges = [
{
            "name": "NASDAQ Stock Exchange",
            "acronym": "NASDAQ",
            "mic": "XNAS",
            "country": "USA",
            "country_code": "US",
            "city": "New York",
            "website": "www.nasdaq.com",
            "timezone": {
                "timezone": "America/New_York",
                "abbr": "EST",
                "abbr_dst": "EDT"
            },
            "currency": {
                "code": "USD",
                "symbol": "$",
                "name": "US Dollar"
            }
        },
        {
            "name": "Bombay Stock Exchange",
            "acronym": "MSE",
            "mic": "XBOM",
            "country": "India",
            "country_code": "IN",
            "city": "Mumbai",
            "website": "www.bseindia.com",
            "timezone": {
                "timezone": "Asia/Kolkata",
                "abbr": "IST",
                "abbr_dst": "IST"
            },
            "currency": {
                "code": "INR",
                "symbol": "Rs",
                "name": "Indian Rupee"
            }
        },
        {
            "name": "National Stock Exchange India",
            "acronym": "NSE",
            "mic": "XNSE",
            "country": "India",
            "country_code": "IN",
            "city": "Mumbai",
            "website": "www.nseindia.com",
            "timezone": {
                "timezone": "Asia/Kolkata",
                "abbr": "IST",
                "abbr_dst": "IST"
            },
            "currency": {
                "code": "INR",
                "symbol": "Rs",
                "name": "Indian Rupee"
            }
        },
]

from .models import *


def mti():
    for e in exchanges:

        currency_code = e['currency']['code']
        currency_symbol =e['currency']['symbol']
        exchange = e['acronym']
        mic = e['mic']
        print(mic, "MIIC")
        r = requests.get(f'http://api.marketstack.com/v1/exchanges/{mic}/tickers?access_key={settings.MARKETSTACK_API_KEY}')
        data = json.loads(r.content)
        print(data, "DATA")
        for t in data['data']['tickers']:
            Ticker.objects.create(name=t['name'], symbol=t['symbol'], currency_code=currency_code, currency_symbol=currency_symbol, exchange=exchange)




def make_tickers(data):
    for d in data['data']:
        Ticker.objects.create(name=d['name'], symbol=d['symbol'])

def remove_mse():
    Ticker.objects.filter(exchange="MSE").delete()
