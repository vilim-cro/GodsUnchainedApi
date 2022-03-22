from lib2to3.pytree import convert
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def get_price(symbol):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'convert': 'USD',
        'symbol': symbol
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '0c262c00-610c-4aa7-a4c4-c3c6517eabac',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        price = data["data"][symbol]["quote"]["USD"]["price"]
        return price
        
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e