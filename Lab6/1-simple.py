from microdot import Microdot
import network
import utime as time

WIFI_SSID = 'Sbain'
WIFI_PASS = 'cant7301'

# Static IP configuration
#STATIC_IP = "192.168.247.100"  # Ensure this IP is free in your network
#SUBNET_MASK = "255.255.255.0"
#GATEWAY = "192.168.247.141"  # Matches your PC's default gateway
#DNS_SERVER = "8.8.8.8"  # Google DNS


# checking connection with wifi
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



# running microdot

app = Microdot()

@app.route("/")
def index(request):
    return "Microdot is working on ESP32!"

app.run(port=80)