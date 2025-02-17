import requests
from typing import TypeAlias
from ._constants import TICKERS, FMP_BASE_URL, FMP_API_KEY
from ...models import CompanyProfile
from django.core.management.base import BaseCommand


CPJson: TypeAlias = dict[str, str | float | int | bool]

class Command(BaseCommand):
    help = 'Saves/updates a list of company profiles to the database.'

    def handle(self, *args, **options) -> None:
        for ticker in TICKERS:
            data = self._fetch_company_profile(ticker)
            self.save_company_profile_db(ticker, data)

    def _fetch_company_profile(self, ticker: str) -> CPJson:
        url = FMP_BASE_URL + '/profile' + '/' + ticker
        print(f'fetching from {url}')
        r = requests.get(url, params={'apikey': FMP_API_KEY})
        data = r.json()[0]
        return data

    def save_company_profile_db(self, ticker: str, data: CPJson) -> None:
        self.stdout.write(f'saving/updating {ticker}')
        cp = CompanyProfile(
            symbol=data['symbol'],
            price=data['price'],
            beta=data['beta'],
            vol_avg=data['volAvg'],
            mkt_cap=data['mktCap'],
            last_div=data['lastDiv'],
            range=data['range'],
            changes=data['changes'],
            company_name=data['companyName'],
            currency=data['currency'],
            cik=data['cik'],
            isin=data['isin'],
            cusip=data['cusip'],
            exchange=data['exchange'],
            exchange_short_name=data['exchangeShortName'],
            industry=data['industry'],
            website=data['website'],
            description=data['description'],
            ceo=data['ceo'],
            sector=data['sector'],
            country=data['country'],
            full_time_employees=data['fullTimeEmployees'],
            phone=data['phone'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            zip=data['zip'],
            dcf_diff=data['dcfDiff'],
            dcf=data['dcf'],
            image=data['image'],
            ipo_date=data['ipoDate'],
            default_image=data['defaultImage'],
            is_etf=data['isEtf'],
            is_actively_trading=data['isActivelyTrading'],
            is_adr=data['isAdr'],
            is_fund=data['isFund']
        )
        cp.save()
