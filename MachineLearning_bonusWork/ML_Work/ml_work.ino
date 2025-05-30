#include <Arduino.h>
#include <DHT.h>
#include <esp_heap_caps.h>

#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/version.h"

#include "model_data.h"  // your C array model

#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
// memory
constexpr int kTensorArenaSize = 40 * 1024;
uint8_t* tensor_arena;
const unsigned char* model_data_ptr = nullptr;

const tflite::Model* model = nullptr;
// for inference
tflite::MicroInterpreter* interpreter = nullptr;

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Allocate PSRAM for model
  model_data_ptr = (const unsigned char*)heap_caps_malloc(model_tflite_len, MALLOC_CAP_SPIRAM);
  if (!model_data_ptr) {
    Serial.println("Failed to allocate PSRAM for model!");
    while (1);
  }
  memcpy((void*)model_data_ptr, model_tflite, model_tflite_len);

  // Load model
  model = tflite::GetModel(model_data_ptr);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    Serial.println("Model version mismatch!");
    while (1);
  }

  // Allocate PSRAM for tensor arena
  tensor_arena = (uint8_t*)heap_caps_malloc(kTensorArenaSize, MALLOC_CAP_SPIRAM);
  if (!tensor_arena) {
    Serial.println("Failed to allocate tensor arena!");
    while (1);
  }

  static tflite::MicroMutableOpResolver<4> resolver;
  resolver.AddFullyConnected();
  resolver.AddRelu();
  resolver.AddSoftmax();
  resolver.AddReshape();
  static tflite::MicroInterpreter static_interpreter(model, resolver, tensor_arena, kTensorArenaSize);
  interpreter = &static_interpreter;

  if (interpreter->AllocateTensors() != kTfLiteOk) {
    Serial.println("Tensor allocation failed");
    while (1);
  }

  Serial.println("Setup complete. Starting inference...");
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    delay(2000);
    return;
  }

  TfLiteTensor* input = interpreter->input(0);
  input->data.f[0] = temperature;
  input->data.f[1] = humidity;

  if (interpreter->Invoke() != kTfLiteOk) {
    Serial.println("Inference failed");
    return;
  }

  TfLiteTensor* output = interpreter->output(0);
  int predicted_class = std::distance(output->data.f, std::max_element(output->data.f, output->data.f + 3));

  if (predicted_class == 0) Serial.println("Predicted: Cold");
  else if (predicted_class == 1) Serial.println("Predicted: Comfort");
  else Serial.println("Predicted: Hot");

  delay(5000);
}
