#include <ArduinoJson.h>

#define BAUD_RATE 115200

void setup() {
  Serial.begin(115200);  // Debugging
  Serial.println("ESP32 JSON UART Receiver Started");
}

void loop() {
    static String jsonBuffer = "";  // Buffer to hold incoming data

    // Read data from Serial2 if available
    while (Serial.available()) {
        char incomingChar = Serial.read();
        
        // End of JSON object detected
        if (incomingChar == '\n') {
            processJson(jsonBuffer);
            jsonBuffer = "";  // Clear buffer for the next message
        } else {
            jsonBuffer += incomingChar;
        }
    }
}

// Function to process received JSON data
void processJson(String jsonString) {
    Serial.println("Received JSON: " + jsonString);
    
    // Create a JSON document
    StaticJsonDocument<256> doc;

    // Parse JSON data
    DeserializationError error = deserializeJson(doc, jsonString);
    if (error) {
        Serial.print("JSON Parsing Failed: ");
        Serial.println(error.f_str());
        return;
    }

    // Extract values (modify according to your JSON structure)
    const char* device = doc["device"];
    int value = doc["value"];
    
    Serial.print("Device: ");
    Serial.println(device);
    Serial.print("Value: ");
    Serial.println(value);
}

