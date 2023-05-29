import os

def get_redirect_uri(request):
    if os.getenv('REPLIT_DB_URL'):
        repl_url = os.getenv('REPL_SLUG') + '.' + os.getenv('REPL_OWNER') + '.repl.co'
        return f'https://{repl_url.lower()}/rest/v1/calendar/redirect/'
    else:
        server_port = request.META.get('SERVER_PORT')
        return f'http://localhost:{server_port}/rest/v1/calendar/redirect/'
