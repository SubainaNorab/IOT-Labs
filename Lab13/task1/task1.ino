#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

// Configuration
#define DHTPIN 4           // GPIO pin connected to DHT11
#define DHTTYPE DHT11
#define WIFI_SSID "NTU FSD"
#define WIFI_PASSWORD ""
#define MQTT_SERVER "10.13.47.140"  // Replace with your PC IP
#define MQTT_PORT 1883

// Objects
DHT dht(DHTPIN, DHTTYPE);
WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;
const long interval = 5000;  // Send every 5 seconds

void setup_wifi() {
  Serial.println("Connecting to WiFi...");
  Serial.print("ESP32 MAC: ");
  Serial.println(WiFi.macAddress());

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  unsigned long startAttemptTime = millis();

  // Wait for connection for max 10 seconds
  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < 10000) {
    delay(500);
    Serial.print(".");
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFailed to connect to WiFi");
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP32Client-";
    clientId += String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  setup_wifi();
  client.setServer(MQTT_SERVER, MQTT_PORT);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    setup_wifi();  // Retry connection if WiFi is lost
    return;
  }

  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > interval) {
    lastMsg = now;
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    if (isnan(temperature) || isnan(humidity)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }

    String tempStr = String(temperature, 2);
    String humStr = String(humidity, 2);

    client.publish("esp32/dht/temp", tempStr.c_str());
    client.publish("esp32/dht/hum", humStr.c_str());

    Serial.print("Published Temperature: ");
    Serial.println(tempStr);
    Serial.print("Published Humidity: ");
    Serial.println(humStr);
    Serial.println("Waiting for next reading...");
  }
}
