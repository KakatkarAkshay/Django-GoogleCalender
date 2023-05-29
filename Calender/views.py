import os
import json

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2 import credentials

from .utils import get_redirect_uri


class GoogleCalendarInitView(View):
    def get(self, request):
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
        client_secret_json = json.loads(client_secret)

        redirect_uri = get_redirect_uri(request)

        flow = Flow.from_client_config(
            client_secret_json,
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=redirect_uri
        )
        authorization_url, _ = flow.authorization_url(prompt='consent')

        return redirect(authorization_url)


class GoogleCalendarRedirectView(View):
    def get(self, request):
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
        client_secret_json = json.loads(client_secret)

        code = request.GET.get('code')

        redirect_uri = get_redirect_uri(request)

        flow = Flow.from_client_config(
            client_secret_json,
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=redirect_uri
        )
        flow.fetch_token(code=code)

        creds = flow.credentials
        request.session['access_token'] = creds.token
        request.session['refresh_token'] = creds.refresh_token
        request.session['client_id'] = creds.client_id
        request.session['client_secret'] = creds.client_secret

        return redirect('/rest/v1/calendar/events/')


class GoogleCalendarEventsView(View):
    def get(self, request):
        access_token = request.session.get('access_token')
        refresh_token = request.session.get('refresh_token')
        client_id = request.session.get('client_id')
        client_secret = request.session.get('client_secret')

        if not access_token or not refresh_token or not client_id or not client_secret:
            return JsonResponse({'error': 'User access token not found.'}, status=401)

        creds = credentials.Credentials.from_authorized_user_info({
            'token': access_token,
            'refresh_token': refresh_token,
            'client_id': client_id,
            'client_secret': client_secret,
            'token_uri': 'https://oauth2.googleapis.com/token',
            'scopes': ['https://www.googleapis.com/auth/calendar.readonly']
        })

        service = build('calendar', 'v3', credentials=creds, static_discovery=False)

        events = service.events().list(calendarId='primary').execute()

        formatted_events = []
        for event in events['items']:
            formatted_event = {
                'summary': event.get('summary', ''),
                'start': event['start'].get('dateTime', event['start'].get('date')),
                'end': event['end'].get('dateTime', event['end'].get('date'))
            }
            formatted_events.append(formatted_event)

        return JsonResponse(formatted_events, safe=False)
