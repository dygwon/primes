import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()


TICKERS = ['LMT', 'RTX', 'NOC', 'GD', 'BA', 'PLTR']
FMP_BASE_URL = 'https://financialmodelingprep.com/api/v3'
FMP_API_KEY = os.environ['FMP_API_KEY']

WORK_DIR = os.environ['WORK_DIR']
DATA_DIR = os.path.join(WORK_DIR, 'fetched_data')


def fetch_company_profile(ticker: str) -> dict:
    url = FMP_BASE_URL + '/profile' + '/' + ticker
    print(f'fetching from {url}')
    r = requests.get(url, params={'apikey': FMP_API_KEY})
    data = r.json()[0]
    return data


def save_company_profile_json(ticker: str, data: dict) -> None:
    save_file_name = f'{ticker}.json'
    save_file_path = os.path.join(DATA_DIR, save_file_name)
    print(f'saving to {save_file_path}')
    with open(save_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def main():
    for ticker in TICKERS:
        data = fetch_company_profile(ticker)
        save_company_profile_json(ticker, data)


if __name__ == '__main__':
    main()
