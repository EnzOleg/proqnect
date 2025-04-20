from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', index, name='index'),
    path('accounts/', include('accounts.urls')),
    path('assistant/', include('assistant.urls')),
    path('friends/', include('friends.urls')),
    path('booking/', include('booking.urls')),
    path('chat/', include('chat.urls')),
    path('experts/', include('experts.urls')),
    path('payments/', include('payments.urls')),
    path('feed/', include('feed.urls')),
    path('notifications/', include('notifications.urls')),
    path('moderation/', include('moderation.urls')),
    path('about/', about, name='about')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)