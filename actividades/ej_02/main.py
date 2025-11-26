import network
from time import sleep
import machine
import ssd1306
from app import app   # importa el Microdot creado en app.py

i2c = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def connect_to(ssid: str, passwd: str) -> str:
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to network...")
        sta_if.active(True)
        sta_if.connect(ssid, passwd)
        while not sta_if.isconnected():
            print(".", end="")
            sleep(.05)

    print()
    print("Network config:", sta_if.ifconfig())
    print()
    return sta_if.ifconfig()[0]

# Conectar WiFi
ip = connect_to("Cooperadora Alumnos", "")

# Mostrar en OLED
oled.fill(0)
oled.text("Lin-Bianco!", 1, 1)
oled.text("ej2_IP:", 1, 20)
oled.text(ip, 1, 35)
oled.show()

# Levantar servidor
app.run(port=80)