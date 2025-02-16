import os
import json
from ...models import CompanyProfile
from ._data import DATA_DIR, TICKERS
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Saves/updates a list of company profiles to the database.'

    def handle(self, *args, **options) -> None:
        for ticker in TICKERS:
            self.save_company_profile_db(ticker)

    def save_company_profile_db(self, ticker: str) -> None:
        file_name = f'{ticker}.json'
        file_path = os.path.join(DATA_DIR, file_name)
        self.stdout.write(f'saving/updating {file_path}')
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
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
