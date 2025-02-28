print("Hello, ESP32-S3!")

import network
import time

ssid = "Hadia" 
password = "8777hadia" #password

print("Connecting to WiFi", end="")
sta = network.WLAN(network.STA_IF) #initialization
sta.active(True) #activation
sta.connect(ssid , password)

# Wait for connection
for _ in range(10):
    if sta.isconnected():
        break
    print(".", end="", flush=True)
    time.sleep(1)
    
# checking connected or not
if sta.isconnected():
    print("Connected to WiFi!")
    print("IP Address:", sta.ifconfig()[0])
else:
    print("Failed to connect.Please check credentials or signals")
