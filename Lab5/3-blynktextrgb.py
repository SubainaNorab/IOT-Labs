#changing led color from blynk text
#rgb text device
import BlynkLib as blynklib
import network
import uos
import utime as time
from machine import Pin, I2C, Timer
from neopixel import NeoPixel
#from machine import Pin, I2C, Timer
import ssd1306

ssid = 'Hadia'
password = '8777hadia'
BLYNK_AUTH = "22a9HJ2KXG3VbPCZUZWzVvnlWudkbjI9"

print("Connecting to WiFi network '{}'".format(ssid))
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

#checking connectioon
while not wifi.isconnected():
    time.sleep(1)
    print('WiFi connect retry ...')
print('WiFi IP:', wifi.ifconfig()[0])

print("Connecting to Blynk server...")
blynk = blynklib.Blynk(BLYNK_AUTH)

# Define the pin connected to the NeoPixel
pin = Pin(48, Pin.OUT)
np = NeoPixel(pin, 1)

i2c = I2C(1, scl=Pin(9), sda=Pin(8), freq= 200000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def set_color(r, g, b):
    np[0] = (r, g, b)
    np.write()

# RGB Values
r = 0
g = 0
b = 0

# Blynk Handlers for Virtual Pins
@blynk.on("V0")  # check input and change led color
def v0_handler(value):
    try:
        # Parse the input text (expected format: "R,G,B")
        r, g, b = map(int, value[0].split(','))
        set_color(r, g, b)
        oled.fill(0)
        oled.text("RGB Value", 18, 16)
        oled.text(value[0], 23, 32)
        oled.show()
    except Exception as e:
        print("Invalid input:", e)
    
@blynk.on("connected")
def blynk_connected():
    print("Blynk Connected!")
    blynk.sync_virtual(0, 1, 2)  # Sync data from blynk cloud to esp32

@blynk.on("disconnected")
def blynk_disconnected():
    print("Blynk Disconnected!")

# Main Loop
while True:
    blynk.run()
    

