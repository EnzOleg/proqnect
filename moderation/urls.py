from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name='admin'

urlpatterns = [
    path('panel/', welcome_view, name='welcome_view')
]
