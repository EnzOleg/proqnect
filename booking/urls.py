from django.urls import path
from .views import request_booking, handle_booking, confirm_booking, my_bookings

app_name = 'booking'

urlpatterns = [
    path('request/<int:expert_id>/', request_booking, name='request_booking'),
    path("<int:booking_id>/confirm/", confirm_booking, name="confirm_booking"),
    path('<int:booking_id>/<str:action>/', handle_booking, name='handle_booking'),
    path("my_bookings/", my_bookings, name="my_bookings"),
]
