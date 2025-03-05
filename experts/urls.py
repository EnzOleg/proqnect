from django.urls import path
from .views import experts_search, become_expert, expert_detail, expert_bookings

app_name = 'experts'

urlpatterns = [
    path('', experts_search, name="search_experts"),
    path('become/', become_expert, name="become_expert"),
    path('<int:pk>/', expert_detail, name="detail"),
    path("my_bookings/", expert_bookings, name="expert_bookings"),
]
