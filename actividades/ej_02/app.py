from microdot import Microdot, Response, send_file
from machine import Pin
from neopixel import NeoPixel

app = Microdot()
Response.default_content_type = 'text/html'

# ---------- Hardware ----------
led1 = Pin(32, Pin.OUT)
led2 = Pin(33, Pin.OUT)
led3 = Pin(25, Pin.OUT)

# Ajustá el pin y la cantidad de LEDs según tu placa
np_pin = Pin(27, Pin.OUT)
np = NeoPixel(np_pin, 4)   # si tenés 1 solo, poné 1

# ---------- Rutas estáticas ----------
@app.route('/')
def index(request):
    return send_file('index.html')

@app.route('/styles/<path:path>')
def styles(request, path):
    return send_file('styles/' + path)

@app.route('/scripts/<path:path>')
def scripts(request, path):
    return send_file('scripts/' + path)

@app.route('/img/<path:path>')
def images(request, path):
    return send_file('img/' + path)

# ---------- Rutas de control de LEDs ----------
@app.route('/led/<int:n>/<state>')
def led_route(request, n, state):
    led_map = {1: led1, 2: led2, 3: led3}
    led = led_map.get(n)
    if not led:
        return 'LED inválido', 400

    if state == 'on':
        led.value(1)
    else:
        led.value(0)

    return 'OK'

# ---------- Ruta para el NeoPixel / tira WS281x ----------
@app.route('/ws2818b/color')
def ws_color(request):
    try:
        r = int(request.args.get('r', 0))
        g = int(request.args.get('g', 0))
        b = int(request.args.get('b', 0))
    except (TypeError, ValueError):
        return 'Parámetros inválidos', 400

    # Setear todos los LEDs del NeoPixel al mismo color
    for i in range(len(np)):
        np[i] = (r, g, b)
    np.write()

    return 'OK'