import network
from time import sleep
import machine
import ssd1306

i2c = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def connect_to(ssid : str, passwd : str) -> None:
    """Conecta el microcontrolador a la red indicada.

    Parameters
    ----------
    ssid : str
        Nombre de la red a conectarse
    passwd : str
        Contraseña de la red
    """
    
    import network
    from time import sleep
    
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
oled.text("IP:", 1, 20)
oled.text(ip, 1, 35)
oled.show()