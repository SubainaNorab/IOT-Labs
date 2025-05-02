#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

// WiFi Credentials
const char* ssid = "Sbain";
const char* password = "cant7301";

// Firebase Configuration
const String FIREBASE_HOST = "lab11-firebase-df992-default-rtdb.firebaseio.com";
const String FIREBASE_AUTH = "gAazo17Whgd55GZgQQlxqMnMPmpLVdyfeqVGjMls";
const String FIREBASE_PATH = "/temp_hum.json";

// DHT Sensor
#define DHTPIN 4       // GPIO4 (change if needed)
#define DHTTYPE DHT11  // DHT11 or DHT22

// Timing
const unsigned long SEND_INTERVAL = 10000;  // 10 seconds
const unsigned long SENSOR_DELAY = 2000;    // 2 seconds between reads

// ======= Global Objects ======= //
DHT dht(DHTPIN, DHTTYPE);
unsigned long lastSendTime = 0;
unsigned long lastReadTime = 0;

// NTP Setup
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", 0, 60000);  // GMT time offset, 60 sec update interval

// Timezone Offset (adjust based on your timezone)
const long timeOffset = 5 * 3600;  // For GMT+5, adjust as needed

// ======= Setup ======= //
void setup() {
  Serial.begin(115200);
  Serial.println("\nESP32-S3 DHT11 Firebase Monitor");

  initDHT();
  connectWiFi();
  timeClient.begin();  // Start NTP client
  timeClient.setTimeOffset(timeOffset);  // Set timezone offset
  delay(1000);  // Allow some time for the NTP client to sync with the server
}

// ======= Main Loop ======= //
void loop() {
  // Maintain WiFi connection
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  // Read sensor (with proper timing)
  if (millis() - lastReadTime >= SENSOR_DELAY) {
    float temp, hum;
    if (readDHT(&temp, &hum)) {
      // Send to Firebase (with proper timing)
      if (millis() - lastSendTime >= SEND_INTERVAL) {
        sendToFirebase(temp, hum);
        lastSendTime = millis();
      }
    }
    lastReadTime = millis();
  }
}

// ======= Sensor Functions ======= //
void initDHT() {
  dht.begin();
  Serial.println("DHT sensor initialized");
  delay(500);  // Short stabilization delay
}

bool readDHT(float* temp, float* humidity) {
  *temp = dht.readTemperature();
  *humidity = dht.readHumidity();

  if (isnan(*temp) || isnan(*humidity)) {
    Serial.println("DHT read failed! Retrying...");
    
    // Attempt sensor recovery
    digitalWrite(DHTPIN, LOW);  // Reset pin state
    pinMode(DHTPIN, INPUT);
    delay(100);
    initDHT();  // Reinitialize
    
    return false;
  }
  
  Serial.printf("DHT Read: %.1f°C, %.1f%%\n", *temp, *humidity);
  return true;
}

// ======= WiFi Functions ======= //
void connectWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.disconnect(true);  // Clear previous config
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 15) {
    delay(500);
    Serial.print("...");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi Connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nWiFi Connection Failed!");
  }
}

// ======= Firebase Functions ======= //
void sendToFirebase(float temp, float humidity) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Cannot send - WiFi disconnected");
    return;
  }

  // Update time
  timeClient.update();
  String formattedTime = formatTime(timeClient.getHours(), timeClient.getMinutes(), timeClient.getSeconds());
  Serial.println("Formatted Time: " + formattedTime);  // Debug print to check the formatted time

  HTTPClient http;
  String url = "https://" + FIREBASE_HOST + FIREBASE_PATH + "?auth=" + FIREBASE_AUTH;
  
  // Create JSON payload
  String jsonPayload = "{\"temperature\":" + String(temp) + 
                      ",\"humidity\":" + String(humidity) + 
                      ",\"timestamp\":\"" + formattedTime + "\"}";

  Serial.println("Sending to Firebase...");
  Serial.println(jsonPayload);

  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  
  int httpCode = http.POST(jsonPayload);
  
  if (httpCode == HTTP_CODE_OK) {
    Serial.println("Firebase update successful");
  } else {
    Serial.printf("Firebase error: %d\n", httpCode);
    if (httpCode == -1) {
      Serial.println("Check your Firebase URL and authentication");
    }
  }
  
  http.end();
}

// ======= Time Formatting Function ======= //
String formatTime(int hours, int minutes, int seconds) {
  String period = (hours >= 12) ? "PM" : "AM";  // Set AM/PM
  if (hours > 12) hours -= 12;  // Convert to 12-hour format
  if (hours == 0) hours = 12;  // Handle midnight as 12:00
  String formattedTime = String(hours) + ":" + (minutes < 10 ? "0" : "") + String(minutes) + " " + period;
  return formattedTime;
}
