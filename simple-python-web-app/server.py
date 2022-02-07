urls = {}


def render_template(template_name, context=None):
    with open(f'templates/{template_name}') as f:
        html = f.read()

    if context:
        html = html.format(**context)
    return html


def home():
    return render_template('index.html')


def example():
    context = {'message': 'Hello, World!'}
    return render_template('example.html', context=context)


def not_found():
    return render_template('404.html')


def app(environ, start_response):
    """Simple web app."""
    data = ''
    path = environ.get('PATH_INFO')
    status = '200 OK'

    if path.endswith('/'):
        path = path[:-1]

    if path == '':
        data = home()
    elif path == '/example':
        data = example()
    else:
        data = not_found()
        status = '404 Not Found'

    response_headers = [
        ('Content-type', 'text/html'),
        ('Content-Length', str(len(data))),
    ]
    start_response(status, response_headers)
    data = data.encode('utf-8')
    return iter([data])
