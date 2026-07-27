from django.db import connection
from django.template import Context, Template

BANNER = Template('''<div id="middleware">
<p>Total query: {{ count }}</p>
<p>Total time: {{ time }}</p>
</div>''')


class QueryCountMiddleware:
    """
    Debug instrumentation: appends a query-count/time banner before
    </body> on HTML responses. Not wired into MIDDLEWARE by default.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 'text/html' not in response.get('Content-Type', ''):
            return response
        if getattr(response, 'streaming', False):
            return response
        total_time = sum(float(q['time']) for q in connection.queries)
        banner = BANNER.render(Context(
            {'count': len(connection.queries), 'time': total_time}))
        charset = response.charset
        content = response.content.decode(charset)
        response.content = content.replace(
            '</body>', banner + '</body>').encode(charset)
        response['Content-Length'] = len(response.content)
        return response
