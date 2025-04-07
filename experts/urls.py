from django.urls import path
from .views import *

app_name = 'experts'

urlpatterns = [
    path('', experts_search, name="search_experts"),
    path('become/', become_expert, name="become_expert"),
    path('<int:pk>/', expert_detail, name="detail"),
    path("my_bookings/", expert_bookings, name="expert_bookings"),
    path('<int:expert_id>/review/', add_review, name="add_review"),
]
