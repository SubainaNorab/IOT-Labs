# without interrupt

from machine import Pin, I2C, Timer
import machine
import ssd1306 
import dht
import time
print("Started")

DHT_PIN = 4  # DHT22 data pin
button = Pin(0, Pin.IN, Pin.PULL_UP)
# Initialize DHT22 sensor
dht_sensor = dht.DHT11(machine.Pin(DHT_PIN)) # change DHT11 fr physical device

# Initialize OLED display
i2c = machine.I2C(scl=machine.Pin(9), sda=machine.Pin(8))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

pressed= False




# Main loop
while True:
    try:
        if button.value()==0: #checking button press
            time.sleep(0.2)
            
            pressed= not pressed
            if pressed:
                oled.poweroff()
            else:
                oled.poweron()

      


        dht_sensor.measure()
        time.sleep(.2)
        temp = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        print(temp, humidity)
        if not pressed:
            oled.fill(0)
            oled.text("Temp: {} C".format(temp), 0, 0)
            oled.text("Humidity: {}%".format(humidity), 0, 16)
            oled.show()

    except Exception as e:
        print("Error reading DHT22 sensor:", e)

    time.sleep(1) 
    
        


























