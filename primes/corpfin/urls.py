from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<ticker>/', views.company_profile, name='company_profile'),
    path('<ticker>/income-statements',
         views.income_statements,
         name='income_statements'),
    path('<ticker>/balance-sheets',
         views.balance_sheets,
         name='balance_sheets')
]
