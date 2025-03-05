from django.urls import path
from .views import make_payment, payment_history

urlpatterns = [
    path('make_payment/', make_payment, name='make_payment'),
    path('payment_history/', payment_history, name='payment_history'),
]
