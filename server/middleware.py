from django.http import HttpResponseForbidden
from django.conf import settings

class IPRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        if ip not in settings.ALLOWED_IPS:
            return HttpResponseForbidden('Access denied. Your IP address is not authorized to access this service.')

        return self.get_response(request) 