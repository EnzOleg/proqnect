from django.urls import path
from .views import *

app_name = 'payments'

urlpatterns = [
    path('add/', add_balance, name='add_balance'),
    path('withdraw/', withdraw_balance, name='withdraw_balance'),
    path('make_payment/', make_payment, name='make_payment'),
    path('payment_history/', payment_history, name='payment_history'),
]
