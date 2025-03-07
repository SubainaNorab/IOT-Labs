import network
import BlynkLib #saved in esp32 S3
from machine import Pin
import time
from neopixel import NeoPixel
import dht

# sensor configutations
sensor = dht.DHT11(Pin(4))

#station mode
wifi = network.WLAN(network.STA_IF)

ssid = 'Sbain'
password = 'cant7301'

wifi.active(True)
wifi.connect(ssid, password)
# checking wifi connected or not
while not wifi.isconnected():
    print("Connecting to Wi-Fi...")
    time.sleep(1)

print("Connected to Wi-Fi:", wifi.ifconfig())
# blynk object using authentication token
blynk = BlynkLib.Blynk('nh3M_8lOZN5vTBNjHqJMQgs6dDLVkWf7')

#checking that connection built with blynk or not
@blynk.on("connected")
def blynk_connected():
    print("Blynk Connected!")
    blynk.sync_virtual(0, 1) 


# reading temperature and humidity from sensor   
    
def read_dht():
    try:
        sensor.measure()
        temp = sensor.temperature()
        humidity = sensor.humidity()
        
        if temp is not None and humidity is not None:  # Ensure valid readings
            print(f"Temp: {temp}°C, Humidity: {humidity}%")
            blynk.virtual_write(0, temp)  # Send to Virtual Pin V4
            time.sleep(1)
            print('temp send')
            blynk.virtual_write(1, humidity)  # Send to Virtual Pin V5
        else:
            print("Invalid DHT11 data")
    
    except Exception as e:
        print("Failed to read from DHT11:", e)
    
        
while True:
    blynk.run()
    
    read_dht() # for temperature and humidity
    time.sleep(8)
