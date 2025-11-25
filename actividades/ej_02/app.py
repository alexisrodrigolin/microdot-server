from microdot import Microdot, Response, send_file

app = Microdot()
Response.default_content_type = 'text/html'

@app.route('/')
def index(request):
    with open('index.html') as f:
        return f.read()

@app.route('/styles/<path:path>')
def styles(request, path):
    return send_file('styles/' + path)

@app.route('/scripts/<path:path>')
def scripts(request, path):
    return send_file('scripts/' + path)

@app.route('/img/<path:path>')
def images(request, path):
    return send_file('img/' + path)