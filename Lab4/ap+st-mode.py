# implementing acess point and station mode
import network
import time

print("Hello, ESP32-S3!")

# WiFi Station Mode 
SSID = "SBA" #router id
PASSWORD = "09345521" #router password

sta = network.WLAN(network.STA_IF)
sta.active(True)

if not sta.isconnected():
    print("Connecting to WiFi", end="")
    sta.connect(SSID, PASSWORD)
    
    for _ in range(15):  # more  attempts for better stability
        if sta.isconnected():
            break
        print(".", end="")  # Show progress
        time.sleep(1)

if sta.isconnected():
    print("\nConnected to WiFi!")
    print("IP Address as station:", sta.ifconfig()[0])
else:
    print("\nFailed to connect. Check credentials or signal strength.")

# WiFi Access Point Mode 
AP_SSID = "SSS"
AP_PASSWORD = "12345678" 
AP_AUTH_MODE = network.AUTH_WPA2_PSK  # Secure mode

ap = network.WLAN(network.AP_IF)
ap.active(True)

try:
    ap.config(essid=AP_SSID, password=AP_PASSWORD, authmode=AP_AUTH_MODE) #authentication mode determine how device connect to esp32
    print("Access Point Active")
    print("AP IP Address:", ap.ifconfig()[0])
except Exception as e:
    print("Failed to create Access Point:", str(e))
