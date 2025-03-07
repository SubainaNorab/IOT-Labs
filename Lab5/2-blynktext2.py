# handling text on new line
import BlynkLib as blynklib
import network
import uos
import utime as time
from machine import Pin, I2C, Timer
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



i2c = I2C(1, scl=Pin(9), sda=Pin(8), freq= 200000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

oled.fill(0)
oled.show()

# Function to split text into lines based on display width
def split_text(text, max_chars_per_line=16):
    lines = []
    for line in text.split('\\n'):  # First, split by explicit newlines
        while len(line) > max_chars_per_line:
            # Split long lines into chunks
            lines.append(line[:max_chars_per_line])
            line = line[max_chars_per_line:]
        lines.append(line)  # Add the remaining part of the line
    return lines



def display_text(text):
    oled.fill(0)  # Clear the display
    lines = split_text(text)  # Split text into lines
    y = 0  # Starting y-coordinate for the first line
    for line in lines:
        if y < 64:  # Ensure the text doesn't go beyond the display height
            oled.text(line, 0, y)
            y += 8  # Move to the next line (8 pixels per line)
    oled.show()

@blynk.on("V0")  #text displeyer
def v0_handler(value):
    try:
        message = value[0]
        print("Received message:", message)
        display_text(message)  # Display the message on the OLED
    except Exception as e:
        print("Invalid input:", e)
    
@blynk.on("connected")
def blynk_connected():
    print("Blynk Connected!")
    blynk.sync_virtual(0)  # Sync data from the web

@blynk.on("disconnected")
def blynk_disconnected():
    print("Blynk Disconnected!")

# Main Loop
while True:
    #running on blynk :)
    blynk.run()
    time.sleep(0.1)
    

