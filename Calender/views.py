from django.http import HttpResponse
from django.views import View


class GoogleCalendarInitView(View):
    def get(self, request):
        return HttpResponse('Google Calendar Init!')

class GoogleCalendarRedirectView(View):
    def get(self, request):
        return HttpResponse('Google Calendar Redirect!')