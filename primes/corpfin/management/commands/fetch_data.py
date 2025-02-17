import os
import requests
from typing import TypeAlias
from datetime import datetime
from ...models import CompanyProfile, IncomeStatement
from django.core.management.base import BaseCommand, CommandError


TICKERS = ['LMT', 'RTX', 'NOC', 'GD', 'BA', 'PLTR']
FMP_BASE_URL = 'https://financialmodelingprep.com/api/v3'
FMP_API_KEY = os.environ['FMP_API_KEY']
FMP_BASE_PARAMS = {'apikey': FMP_API_KEY}

CPJson: TypeAlias = dict[str, str | float | int | bool]
ISJson: TypeAlias = dict[str, str | float | int]

class Command(BaseCommand):
    help = 'Saves/updates a list of company profiles to the database.'

    def handle(self, *args, **options) -> None:
        for ticker in TICKERS:
            cp_data = self._fetch_company_profile(ticker)
            self._insert_company_profile_db(ticker, cp_data)
            is_data = self._fetch_income_statements_annual(ticker)
            for i_statement in is_data:
                self._insert_income_statement_db(ticker, i_statement)

    def _fetch_company_profile(self, ticker: str) -> CPJson:
        url = FMP_BASE_URL + '/profile' + '/' + ticker
        self.stdout.write(f'fetching from {url}')
        r = requests.get(url, params=FMP_BASE_PARAMS)
        if r.status_code != 200:
            raise CommandError(f'Failed to fetch data for {ticker}: {r.status_code}')
        data = r.json()[0]
        return data
    
    def _fetch_income_statements_annual(self, ticker: str) -> list[ISJson]:
        url = FMP_BASE_URL + '/income-statement' + '/' + ticker
        self.stdout.write(f'fetching from {url}')
        params = FMP_BASE_PARAMS.copy()
        params.update({'period': 'annual'})
        r = requests.get(url, params=params)
        if r.status_code != 200:
            raise CommandError(f'Failed to fetch income statement for {ticker}: {r.status_code}')
        data = r.json()
        return data

    def _insert_income_statement_db(self, ticker: str, data: ISJson) -> None:
        self.stdout.write(f'saving income statement for {ticker}')
        i_statement = IncomeStatement(
            date=datetime.strptime(data['date'], '%Y-%m-%d'), # type: ignore
            symbol=data['symbol'],
            reported_currency=data['reportedCurrency'],
            cik=data['cik'],
            filling_date=datetime.strptime(data['fillingDate'], '%Y-%m-%d'), # type: ignore 
            accepted_date=datetime.strptime(data['acceptedDate'], '%Y-%m-%d %H:%M:%S'), # type: ignore
            calendar_year=data['calendarYear'],
            period=data['period'],
            revenue=data['revenue'],
            cost_of_revenue=data['costOfRevenue'],
            gross_profit=data['grossProfit'],
            gross_profit_ratio=data['grossProfitRatio'],
            research_and_development_expenses=data['researchAndDevelopmentExpenses'],
            general_and_administrative_expenses=data['generalAndAdministrativeExpenses'],
            selling_and_marketing_expenses=data['sellingAndMarketingExpenses'],
            selling_general_and_administrative_expenses=data['sellingGeneralAndAdministrativeExpenses'],
            other_expenses=data['otherExpenses'],
            operating_expenses=data['operatingExpenses'],
            cost_and_expenses=data['costAndExpenses'],
            interest_income=data['interestIncome'],
            interest_expense=data['interestExpense'],
            depreciation_and_amortization=data['depreciationAndAmortization'],
            ebitda=data['ebitda'],
            ebitda_ratio=data['ebitdaratio'],
            operating_income=data['operatingIncome'],
            operating_income_ratio=data['operatingIncomeRatio'],
            total_other_income_expenses_net=data['totalOtherIncomeExpensesNet'],
            income_before_tax=data['incomeBeforeTax'],
            income_before_tax_ratio=data['incomeBeforeTaxRatio'],
            income_tax_expense=data['incomeTaxExpense'],
            net_income=data['netIncome'],
            net_income_ratio=data['netIncomeRatio'],
            eps=data['eps'],
            eps_diluted=data['epsdiluted'],
            weighted_average_shs_out=data['weightedAverageShsOut'],
            weighted_average_shs_out_dil=data['weightedAverageShsOutDil'],
            link=data['link'],
            final_link=data['finalLink']
        )
        i_statement.save()

    def _insert_company_profile_db(self, ticker: str, data: CPJson) -> None:
        self.stdout.write(f'saving company profile for {ticker}')
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
            ipo_date=datetime.strptime(data['ipoDate'], '%Y-%m-%d'), # type: ignore
            default_image=data['defaultImage'],
            is_etf=data['isEtf'],
            is_actively_trading=data['isActivelyTrading'],
            is_adr=data['isAdr'],
            is_fund=data['isFund']
        )
        cp.save()
