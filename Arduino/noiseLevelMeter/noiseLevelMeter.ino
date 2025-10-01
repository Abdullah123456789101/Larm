/*!
 * @file readData.ino
 * @brief This retrieves microphone data and prints it out.
 * @copyright  Copyright (c) 2022 DFRobot Co.Ltd (http://www.dfrobot.com)
 * @license The MIT License (MIT)
 * @author [TangJie](jie.tang@dfrobot.com)
 * @version V1.0
 * @date 2022-02-18
 * @url https://github.com/DFRobot/DFRobot_MSM261
 */

#include "DFrobot_MSM261.h"

#define SAMPLE_RATE     (44100)
#define I2S_SCK_IO      (21)
#define I2S_WS_IO       (26)
#define I2S_DI_IO       (22)
#define DATA_BIT        (16)
#define MODE_PIN        (33)

const uint32_t record_time = 10; // 10 sec
const uint32_t bufferSamples = 250;
const uint32_t bufferSize = bufferSamples * 4;  // 1000
const uint32_t byteRate = SAMPLE_RATE * 4; // 176.400 bytes/sec
const uint32_t waveDataSize = record_time * byteRate; // 1.764.000 bytes
const uint32_t numChunks = waveDataSize / bufferSize; // 1764
const uint32_t waveSamples = record_time * SAMPLE_RATE;
const float dB_offset = 80.0 + 30.0;

DFRobot_Microphone microphone(I2S_SCK_IO, I2S_WS_IO, I2S_DI_IO);
char buffer[bufferSize];


#include <WiFi.h>
#include <HTTPClient.h>

// WiFi credentials
const char* ssid = "Lukas' iPhone";
const char* password = "blubber7";

// Your server (must support HTTPS)
const char* serverName = "https://agchr.pythonanywhere.com/add";  

void setup()
{
  Serial.begin(115200);
  pinMode(MODE_PIN,OUTPUT);
  digitalWrite(MODE_PIN,LOW); // Configure the Microphone to Receive Left Channel Data
  while(microphone.begin(SAMPLE_RATE, DATA_BIT) != 0){
      Serial.println(" I2S init failed");
  }
  Serial.println("I2S init success");

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");
}

void loop()
{
  float sum = 0.0;
  for (uint32_t cntChunks = 0; cntChunks < numChunks; cntChunks++)
  {
    microphone.read(buffer, bufferSize);

    int16_t left_Sample;
    //int16_t rightSample;
    float left;
    float leftSquared;

    for (uint32_t i = 0; i < bufferSize; i += 4)
    {
      left_Sample = buffer[i+0] | buffer[i+1]<<8;
      //rightSample = buffer[i+2] | buffer[i+3]<<8;
      left = (float)left_Sample;
      leftSquared = left * left;
      
      sum += leftSquared;
    }
  }

  // Calc RMS of raw valus
  float mean = sum / waveSamples;
  float RMS = sqrt(mean);

  // Convert RMS to dB. See stackoverflow.com: how-can-i-calculate-audio-db-level
  float amplitude = RMS / 32768.0;
  float dB = 20.0 * log10(amplitude);

  Serial.print("RMS: ");
  Serial.print(RMS);
  Serial.print(" dB: ");
  Serial.print(dB);
  Serial.print(" dB+offset: ");
  Serial.print(dB + dB_offset);
  Serial.println();

  if(WiFi.status()== WL_CONNECTED){
    HTTPClient http;

    http.begin(serverName);  // specify your server endpoint
    http.addHeader("Content-Type", "application/json");

    // Example JSON payload
    String jsonData = "{ \"db\": " + String(dB + dB_offset) + ", \"sensor_id\": 67 }";

    int httpResponseCode = http.POST(jsonData);

    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println(response);
    } else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }

  delay(8000);


}
