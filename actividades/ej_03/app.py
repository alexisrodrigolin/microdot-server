from microdot import Microdot, Response, send_file
from machine import Pin
from neopixel import NeoPixel
import ds18x20
import onewire
from time import sleep_ms

app = Microdot()
Response.default_content_type = 'text/html'

# ---------- Hardware ----------
led1 = Pin(32, Pin.OUT)
led2 = Pin(33, Pin.OUT)
led3 = Pin(25, Pin.OUT)

np_pin = Pin(27, Pin.OUT)
np = NeoPixel(np_pin, 4)

buzzer_pin = Pin(14, Pin.OUT)
buzzer_pin.value(0)  # apagado al inicio

# Sensor de temperatura DS18B20 en pin 19
ow = onewire.OneWire(Pin(19))
sensor = ds18x20.DS18X20(ow)
roms = sensor.scan()
if not roms:
    print("⚠ No se encontró ningún sensor DS18B20")
rom = roms[0] if roms else None

# Setpoint global (entre 0 y 30)
temp_setpoint = 15


def leer_temperatura():
    """Lee la temperatura actual del DS18B20 (en °C)."""
    if rom is None:
        return None
    sensor.convert_temp()
    sleep_ms(750)  # tiempo de conversión del DS18B20
    t = sensor.read_temp(rom)
    return t


def actualizar_buzzer(temp_actual):
    """Enciende el buzzer si temp_actual > temp_setpoint."""
    global temp_setpoint
    if temp_actual is None:
        buzzer_pin.value(0)
        return
    if temp_actual > temp_setpoint:
        buzzer_pin.value(1)
    else:
        buzzer_pin.value(0)


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


# ---------- Ruta para el NeoPixel / tira WS2812B ----------
@app.route('/ws2818b/color')
def ws_color(request):
    try:
        r = int(request.args.get('r', 0))
        g = int(request.args.get('g', 0))
        b = int(request.args.get('b', 0))
    except (TypeError, ValueError):
        return 'Parámetros inválidos', 400

    for i in range(len(np)):
        np[i] = (r, g, b)
    np.write()

    return 'OK'


# ---------- RUTA: actualizar setpoint desde el slider ----------
@app.route('/setpoint')
def setpoint_route(request):
    """
    GET /setpoint?value=NN   -> actualiza setpoint (0–30)
    Si no se pasa value, devuelve el setpoint actual.
    """
    global temp_setpoint

    value_str = request.args.get('value')
    if value_str is not None:
        try:
            value = int(value_str)
        except ValueError:
            return 'Valor inválido', 400

        if value < 0 or value > 30:
            return 'Fuera de rango (0-30)', 400

        temp_setpoint = value

    # devolvemos el setpoint actual como texto plano
    return str(temp_setpoint)


# ---------- RUTA: estado de temperatura y buzzer ----------
@app.route('/status')
def status_route(request):
    """
    Devuelve JSON con la temperatura actual y estado del buzzer:
    {
        "temp": 23.5,
        "buzzer": 0 o 1
    }
    """
    temp_actual = leer_temperatura()
    actualizar_buzzer(temp_actual)

    buzzer_status = buzzer_pin.value()

    # armamos JSON "a mano" para evitar depender de json.dumps
    if temp_actual is None:
        temp_str = 'null'
    else:
        temp_str = '%.2f' % temp_actual

    body = '{"temp": %s, "buzzer": %d}' % (temp_str, buzzer_status)
    return Response(body, headers={'Content-Type': 'application/json'})