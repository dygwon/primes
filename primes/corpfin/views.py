from django.shortcuts import render
from django.http import HttpResponse

from .models import CompanyProfile, IncomeStatement, BalanceSheet


def index(request):
    return HttpResponse("Hello, world. You're at the corpfin index.")


def company_profile(request, ticker):
    company_profile = CompanyProfile.objects.filter(
        symbol=ticker).latest('created')
    return render(
        request,
        'corpfin/company_profile.html',
        {'company_profile': company_profile})


def income_statements(request, ticker):
    income_statements = IncomeStatement.objects.filter(symbol=ticker)
    return render(
        request,
        'corpfin/income_statements.html',
        {'income_statements': income_statements})


def balance_sheets(request, ticker):
    balance_sheets = BalanceSheet.objects.filter(symbol=ticker)
    return render(
        request,
        'corpfin/balance_sheets.html',
        {'balance_sheets': balance_sheets})
