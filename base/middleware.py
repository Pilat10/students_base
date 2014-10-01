from django.db import connection
from django.template import Template, Context


class MyMiddleware:

    def process_response(self, request, response):
        if 'text/html' in response['Content-Type']:
            time = 0.0
            for i in connection.queries:
                time += float(i['time'])
            t = Template(u'''<div id=middleware>
            <p>Total query: {{ count }}</p>
            <p>Total time: {{ time }}</p>
            </div>''')
            response.content = response.content.replace(
                '</body>', '{} </body>'.format(t.render(Context(
                {'count': len(connection.queries), 'time': time}))))

        return response