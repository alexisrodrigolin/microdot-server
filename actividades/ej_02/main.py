import network
from time import sleep
import machine
import ssd1306
from app import app
from neopixel import NeoPixel
i2c = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

led1 = machine.Pin(32, machine.Pin.OUT)
led2 = machine.Pin(33, machine.Pin.OUT)
led3 = machine.Pin(25, machine.Pin.OUT)

led1.value(0)
led2.value(1)
led3.value(0)

np = NeoPixel(machine.Pin(27), 4)  
for i in range(4):
    np[i] = (0, 0, 0)  
np.write()
def connect_to(ssid : str, passwd : str) -> None:
    """Conecta el microcontrolador a la red indicada.

    Parameters
    ----------
    ssid : str
        Nombre de la red a conectarse
    passwd : str
        Contraseña de la red
    """
    
    
    
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to network...")
        sta_if.active(True)
        sta_if.connect(ssid, passwd)
        while not sta_if.isconnected():
            print(".",end="")
            sleep(.05)
    
    print()
    print("Network config:", sta_if.ifconfig())
    print()
    return sta_if.ifconfig()[0]
ip = connect_to("Cooperadora Alumnos", "")

# Muestra "Hola mundo!" en (1, 1) y la IP debajo
oled.fill(0)
oled.text("Lin-Bianco!", 1, 1)  # Posición (1,1) para mejor visualización
oled.text("ej2_IP:", 1, 20)
oled.text(ip, 1, 35)
oled.show()
app.run(port=80)
