# 4-rgb on off only using microdot and script

from microdot import Microdot, Response
from machine import Pin
from neopixel import NeoPixel
import network
import time
# my id and netword
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

# checking wifi onnected or not
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

# Initialize the Microdot web server
app = Microdot()
Response.default_content_type = "application/json"

# HTML Web Page with Buttons and RGB Input
HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32-S3 RGB Control</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        .button { padding: 15px 30px; font-size: 20px; cursor: pointer; margin: 10px; }
        input { width: 50px; text-align: center; font-size: 16px; }
    </style>
    <script>
        function sendCommand(action) {
            fetch('/' + action, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('status').innerText = "RGB LED is " + data.status;
                });
        }

        
    </script>
</head>
<body>
    <h1>ESP32-S3 RGB LED Control</h1>
    <p id="status">RGB LED is OFF</p>
    <button class="button" onclick="sendCommand('on')">Turn ON</button>
    <button class="button" onclick="sendCommand('off')">Turn OFF</button>

    </body>
</html>
"""

# Serve the Web Page
@app.route("/")
def index(request):
    response = Response(body=HTML_PAGE)
    response.headers["Content-Type"] = "text/html"
    return response

# API to Turn ON RGB LED (Set to White)
@app.route("/on", methods=["POST"])
def turn_on(request):
    print("Turning ON RGB LED")
    set_rgb(150, 50, 55)  # White color
    return {"status": "ON"}

# API to Turn OFF RGB LED (Set to Black)
@app.route("/off", methods=["POST"])
def turn_off(request):
    print("Turning OFF RGB LED")
    set_rgb(0, 0, 0)  # Turn off
    return {"status": "OFF"}

# API to Set Custom RGB Color

# Start the Microdot Web Server
print("Starting server...")
app.run(host="0.0.0.0", port=80)