import os
import requests
from typing import TypeAlias
from datetime import datetime
from ...models import CompanyProfile, IncomeStatement, BalanceSheet, CashflowStatement
from django.core.management.base import BaseCommand, CommandError


TICKERS = ['LMT', 'RTX', 'NOC', 'GD', 'BA', 'PLTR']
FMP_BASE_URL = 'https://financialmodelingprep.com/api/v3'
FMP_API_KEY = os.environ['FMP_API_KEY']
FMP_BASE_PARAMS = {'apikey': FMP_API_KEY}

CPJson: TypeAlias = dict[str, str | float | int | bool]
ISJson: TypeAlias = dict[str, str | float | int]
BSJson: TypeAlias = dict[str, str | int]

class Command(BaseCommand):
    help = 'Saves/updates a list of company profiles to the database.'

    def handle(self, *args, **options) -> None:
        for ticker in TICKERS:
            # cp_data = self._fetch_company_profile(ticker)
            # self._insert_company_profile_db(ticker, cp_data)
            # is_data = self._fetch_income_statements(ticker)
            # for i_statement in is_data:
            #     self._insert_income_statement_db(ticker, i_statement)
            # bs_data = self._fetch_balance_sheets(ticker)
            # for bs in bs_data:
            #     self._insert_balance_sheet_db(ticker, bs)
            cf_data = self._fetch_cashflow_statements(ticker)
            for cf_statement in cf_data:
                self._insert_cashflow_statement_db(ticker, cf_statement)

    def _fetch_company_profile(self, ticker: str) -> CPJson:
        url = FMP_BASE_URL + '/profile' + '/' + ticker
        self.stdout.write(f'fetching from {url}')
        r = requests.get(url, params=FMP_BASE_PARAMS)
        if r.status_code != 200:
            raise CommandError(f'Failed to fetch company profile for {ticker}: {r.status_code}')
        data = r.json()[0]
        return data
    
    def _fetch_income_statements(self, ticker: str, period: str='annual') -> list[ISJson]:
        url = FMP_BASE_URL + '/income-statement' + '/' + ticker
        self.stdout.write(f'fetching from {url}')
        params = FMP_BASE_PARAMS.copy()
        params.update({'period': period})
        r = requests.get(url, params=params)
        if r.status_code != 200:
            raise CommandError(f'Failed to fetch income statement(s) for {ticker}: {r.status_code}')
        data = r.json()
        return data
    
    def _fetch_balance_sheets(self, ticker: str, period: str='annual') -> list[BSJson]:
        url = FMP_BASE_URL + '/balance-sheet-statement' + '/' + ticker
        self.stdout.write(f'fetching from {url}')
        params = FMP_BASE_PARAMS.copy()
        params.update({'period': period})
        r = requests.get(url, params=params)
        if r.status_code != 200:
            raise CommandError(f'Failed to fetch balance sheet(s) for {ticker}: {r.status_code}')
        data = r.json()
        return data

    def _fetch_cashflow_statements(self, ticker: str, period: str='annual') -> list[dict]:
        url = FMP_BASE_URL + '/cash-flow-statement' + '/' + ticker
        self.stdout.write(f'fetching from {url}')
        params = FMP_BASE_PARAMS.copy()
        params.update({'period': period})
        r = requests.get(url, params=params)
        if r.status_code != 200:
            raise CommandError(f'Failed to fetch cashflow statement(s) for {ticker}: {r.status_code}')
        data = r.json()
        return data

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

    def _insert_balance_sheet_db(self, ticker: str, data: BSJson) -> None:
        self.stdout.write(f'saving balance sheet for {ticker}')
        b_sheet = BalanceSheet(
            date=datetime.strptime(data['date'], '%Y-%m-%d'), # type: ignore
            symbol=data['symbol'],
            reported_currency=data['reportedCurrency'],
            cik=data['cik'],
            filling_date=datetime.strptime(data['fillingDate'], '%Y-%m-%d'), # type: ignore
            accepted_date=datetime.strptime(data['acceptedDate'], '%Y-%m-%d %H:%M:%S'), # type: ignore
            calendar_year=data['calendarYear'],
            period=data['period'],
            cash_and_cash_equivalents=data['cashAndCashEquivalents'],
            short_term_investments=data['shortTermInvestments'],
            cash_and_short_term_investments=data['cashAndShortTermInvestments'],
            net_receivables=data['netReceivables'],
            inventory=data['inventory'],
            other_current_assets=data['otherCurrentAssets'],
            total_current_assets=data['totalCurrentAssets'],
            property_plant_equipment_net=data['propertyPlantEquipmentNet'],
            goodwill=data['goodwill'],
            intangible_assets=data['intangibleAssets'],
            goodwill_and_intangible_assets=data['goodwillAndIntangibleAssets'],
            long_term_investments=data['longTermInvestments'],
            tax_assets=data['taxAssets'],
            other_non_current_assets=data['otherNonCurrentAssets'],
            total_non_current_assets=data['totalNonCurrentAssets'],
            other_assets=data['otherAssets'],
            total_assets=data['totalAssets'],
            account_payables=data['accountPayables'],
            short_term_debt=data['shortTermDebt'],
            tax_payables=data['taxPayables'],
            deferred_revenue=data['deferredRevenue'],
            other_current_liabilities=data['otherCurrentLiabilities'],
            total_current_liabilities=data['totalCurrentLiabilities'],
            long_term_debt=data['longTermDebt'],
            deferred_revenue_non_current=data['deferredRevenueNonCurrent'],
            deferred_tax_liabilities_non_current=data['deferredTaxLiabilitiesNonCurrent'],
            other_non_current_liabilities=data['otherNonCurrentLiabilities'],
            total_non_current_liabilities=data['totalNonCurrentLiabilities'],
            other_liabilities=data['otherLiabilities'],
            capital_lease_obligations=data['capitalLeaseObligations'],
            total_liabilities=data['totalLiabilities'],
            preferred_stock=data['preferredStock'],
            common_stock=data['commonStock'],
            retained_earnings=data['retainedEarnings'],
            accumulated_other_comprehensive_income_loss=data['accumulatedOtherComprehensiveIncomeLoss'],
            other_total_stockholders_equity=data['othertotalStockholdersEquity'],
            total_stockholders_equity=data['totalStockholdersEquity'],
            total_equity=data['totalEquity'],
            total_liabilities_and_stockholders_equity=data['totalLiabilitiesAndStockholdersEquity'],
            minority_interest=data['minorityInterest'],
            total_liabilities_and_total_equity=data['totalLiabilitiesAndTotalEquity'],
            total_investments=data['totalInvestments'],
            total_debt=data['totalDebt'],
            net_debt=data['netDebt'],
            link=data['link'],
            final_link=data['finalLink']
        )
        b_sheet.save()

    def _insert_cashflow_statement_db(self, ticker: str, data: dict) -> None:
        self.stdout.write(f'saving cashflow statement for {ticker}')
        cf_statement = CashflowStatement(
            date=datetime.strptime(data['date'], '%Y-%m-%d'), # type: ignore
            symbol=data['symbol'],
            reported_currency=data['reportedCurrency'],
            cik=data['cik'],
            filling_date=datetime.strptime(data['fillingDate'], '%Y-%m-%d'), # type: ignore
            accepted_date=datetime.strptime(data['acceptedDate'], '%Y-%m-%d %H:%M:%S'), # type: ignore
            calendar_year=data['calendarYear'],
            period=data['period'],
            net_income=data['netIncome'],
            depreciation_and_amortization=data['depreciationAndAmortization'],
            deferred_income_tax=data['deferredIncomeTax'],
            stock_based_compensation=data['stockBasedCompensation'],
            change_in_working_capital=data['changeInWorkingCapital'],
            accounts_receivables=data['accountsReceivables'],
            inventory=data['inventory'],
            accounts_payables=data['accountsPayables'],
            other_working_capital=data['otherWorkingCapital'],
            other_non_cash_items=data['otherNonCashItems'],
            net_cash_provided_by_operating_activities=data['netCashProvidedByOperatingActivities'],
            investments_in_property_plant_and_equipment=data['investmentsInPropertyPlantAndEquipment'],
            acquisitions_net=data['acquisitionsNet'],
            purchases_of_investments=data['purchasesOfInvestments'],
            sales_maturities_of_investments=data['salesMaturitiesOfInvestments'],
            other_investing_activities=data['otherInvestingActivites'],
            net_cash_used_for_investing_activities=data['netCashUsedForInvestingActivites'],
            debt_repayment=data['debtRepayment'],
            common_stock_issued=data['commonStockIssued'],
            common_stock_repurchased=data['commonStockRepurchased'],
            dividends_paid=data['dividendsPaid'],
            other_financing_activities=data['otherFinancingActivites'],
            net_cash_used_provided_by_financing_activities=data['netCashUsedProvidedByFinancingActivities'],
            effect_of_forex_changes_on_cash=data['effectOfForexChangesOnCash'],
            net_change_in_cash=data['netChangeInCash'],
            cash_at_end_of_period=data['cashAtEndOfPeriod'],
            cash_at_beginning_of_period=data['cashAtBeginningOfPeriod'],
            operating_cash_flow=data['operatingCashFlow'],
            capital_expenditure=data['capitalExpenditure'],
            free_cash_flow=data['freeCashFlow'],
            link=data['link'],
            final_link=data['finalLink']
        )
        cf_statement.save()
