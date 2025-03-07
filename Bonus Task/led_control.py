import network
import BlynkLib #saved in esp32
from machine import Pin
import time
from neopixel import NeoPixel

#station mode

wifi=network.WLAN(network.STA_IF)

# my password and id
ssid='Sbain'
password='cant7301'

wifi.active(True)
wifi.connect(ssid,password)

#checking connection

while not wifi.isconnected():
    print("Connecting to Wi-Fi...")
    time.sleep(1)

print("Connected to Wi-Fi:", wifi.ifconfig())

# blynk authentication token added

blynk=BlynkLib.Blynk('0ZnSnhUpX5eRqfCcY4MTHgM3uq2N0zHZ')

pin = Pin(48, Pin.OUT)   
led = NeoPixel(pin, 1)

# conditions for switching on or off (colors) using blynk

@blynk.on('V1') #green
def green_led(value):
    if int(value[0]) == 1:
        led[0] = (0, 255, 0)  # Green
    else:
        led[0] = (0, 0, 0)  # Turn off LED
    led.write()
        
  
@blynk.on('V2') #red
def red_led(value):
    if int(value[0]) == 1:
        led[0] = (255, 0, 0)  # Red
    else:
        led[0] = (0, 0, 0)  # Turn off LED
    led.write()
    
@blynk.on('V3') #blue
def blue_led(value):
    if int(value[0]) == 1:
        led[0] = (0, 0, 255)  # Blue
    else:
        led[0] = (0, 0, 0)  # Turn off LED
    led.write()
        

# running blynk        
while True:
    blynk.run()
    time.sleep(0.1)
        