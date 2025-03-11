from django.utils import timezone
import pytz

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_tz = getattr(request.user, 'timezone', 'UTC')
            try:
                timezone.activate(pytz.timezone(user_tz))
            except Exception:
                timezone.activate(pytz.timezone('UTC'))
        else:
            timezone.deactivate()
        
        response = self.get_response(request)
        return response
