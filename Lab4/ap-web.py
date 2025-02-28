import network
import socket
import time  # Added for delay

# Setup Access Point
ssid = "SBA"  # SSID
password = "y38992hf"  # Password
ap = network.WLAN(network.AP_IF)
ap.active(True)
time.sleep(2)  # Delay to ensure AP is fully initialized
ap.config(essid=ssid, password=password)

print("Access Point Active, IP:", ap.ifconfig()[0])

# Start Web Server
def web_page():
    html = """<!DOCTYPE html>
    <html>
    <head>
        <title>ESP32 Web Server</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin: 20px; }
            h1 { color: #333; }
            p { font-size: 18px; }
        </style>
    </head>
    <body>
        <h1>ESP32 Web Server</h1>
        <p>Welcome to ESP32 Web Server in AP Mode!</p>
        <p><strong>IoT Class - AI 6th SP25</strong></p>
    </body>
    </html>"""
    return html

# Setup Socket Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print("Connection from:", addr)
    
    request = conn.recv(1024).decode()  # Decode request for better readability
    print("Request:", request)
    
    response = web_page()
    conn.sendall("HTTP/1.1 200 OK\nContent-Type: text/html\n\n".encode())  # Use sendall to ensure full response is sent
    conn.sendall(response.encode())

    conn.close()
