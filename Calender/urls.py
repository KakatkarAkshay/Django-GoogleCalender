from django.urls import path
from django.views.generic import RedirectView
from .views import GoogleCalendarInitView, GoogleCalendarRedirectView, GoogleCalendarEventsView

urlpatterns = [
    path('rest/v1/calendar/init/',
         GoogleCalendarInitView.as_view(), name='calendar_init'),
    path('rest/v1/calendar/redirect/',
         GoogleCalendarRedirectView.as_view(), name='calendar_redirect'),
    path('rest/v1/calendar/events/',
         GoogleCalendarEventsView.as_view(), name='calendar-events'),
    path('',
         RedirectView.as_view(url='rest/v1/calendar/init/'), name='root-redirect'),
]