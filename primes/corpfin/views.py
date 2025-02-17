from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404

from .models import CompanyProfile


def index(request):
    return HttpResponse("Hello, world. You're at the corpfin index.")


def company_profile(request, ticker):
    company_profile = CompanyProfile.objects.filter(
        symbol=ticker).latest('created')
    return render(
        request,
        "corpfin/company_profile.html",
        {'company_profile': company_profile})
