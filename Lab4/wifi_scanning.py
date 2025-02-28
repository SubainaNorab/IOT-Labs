
print("Hello, ESP32-S3!")

# Doing scanning in this code

import network
from machine import Pin

# Wifi as station mode 
wifi = network.WLAN(network.STA_IF)
#activated
wifi.active(True)

# Wifi scanning ..........
print("Scanning Wi-Fi... ", end="")
nets = wifi.scan()
print(f"{len(nets)} network(s)")

print(nets[0])
#checking if network exist
if nets:
   for net in nets:
    ssid = net[0].decode("utf-8")
    print(f" \t{ssid}")
else:
    print("No networks found.")

