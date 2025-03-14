# 2-rgb on off  using microdot without html code
from microdot import Microdot, Response
from machine import Pin
from neopixel import NeoPixel
import network
import time

WIFI_SSID = 'Sbain'
WIFI_PASS = 'cant7301'

print(f"Connecting to WiFi network '{WIFI_SSID}'")
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

#configuring

wifi.ifconfig(('192.168.247.100', '255.255.255.0', '192.168.247.141', '8.8.8.8'))
wifi.connect(WIFI_SSID, WIFI_PASS)

# Timeout logic to prevent infinite waiting
timeout = 10  # 10 seconds max wait 
while not wifi.isconnected() and timeout > 0:
    time.sleep(1)
    print('WiFi connect retry ...')
    timeout -= 1

if wifi.isconnected():
    print('WiFi Connected! IP:', wifi.ifconfig()[0])
else:
    print('Failed to connect to WiFi. Check credentials or network.')




# Define the pin connected to the NeoPixel
pin = Pin(48, Pin.OUT)
np = NeoPixel(pin, 1)  # 1 NeoPixel

# Function to set RGB color
def set_rgb(r, g, b):
    np[0] = (r, g, b)  # Set the color for the first NeoPixel
    np.write()  # Write the color to the NeoPixel

app = Microdot()
# Initialize the Microdot web server
@app.route('/')
def index(request):
    return 'Hello, World!'

@app.route('/rgb/<state>')
def led_control(request, state):
    if state == 'on':
        # Turn on LED (assuming it's connected to GPIO 2)
        set_rgb(255,0,0)
        return 'RGB LED turned ON'
    elif state == 'off':
        # Turn off LED
        set_rgb(0,0,0)
        return 'RGB LED turned OFF'
    else:
        return 'Invalid state'


# Start the Microdot Web Server
print("Starting server...")
#app.run(host="0.0.0.0", port=80)
app.run(port=80)
