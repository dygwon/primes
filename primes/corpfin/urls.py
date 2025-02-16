from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<ticker>/', views.company_profile, name='company_profile')
]
