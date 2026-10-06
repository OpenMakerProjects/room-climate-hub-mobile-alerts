#include <Arduino.h>
#include <Wire.h>
#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <Adafruit_BME280.h>
#include <Adafruit_SSD1306.h>
#include "config.h"
#include "alert_policy.h"
Adafruit_BME280 bme;
Adafruit_SSD1306 oled(128,64,&Wire,-1);
WiFiClient network; PubSubClient mqtt(network); AlertPolicy policy;
bool sensorReady=false, displayReady=false;
unsigned long sampled=0,retryAt=0; uint32_t sequence=0;
void color(bool r,bool g,bool b){digitalWrite(LED_R,r);digitalWrite(LED_G,g);digitalWrite(LED_B,b);}
void setup(){
  Serial.begin(115200); pinMode(LED_R,OUTPUT);pinMode(LED_G,OUTPUT);pinMode(LED_B,OUTPUT);color(0,0,1);
  Wire.begin();sensorReady=bme.begin(BME_ADDRESS);displayReady=oled.begin(SSD1306_SWITCHCAPVCC,OLED_ADDRESS);
  mqtt.setServer(MQTT_HOST,MQTT_PORT);mqtt.setBufferSize(512);mqtt.setSocketTimeout(2);
}
void loop(){
  unsigned long now=millis();
  if (now-retryAt>=RETRY_MS) {
    retryAt=now;
    if(!sensorReady)sensorReady=bme.begin(BME_ADDRESS);
    if(WIFI_SSID[0]&&MQTT_HOST[0]){
      if(WiFi.status()!=WL_CONNECTED)WiFi.begin(WIFI_SSID,WIFI_PASSWORD);
      else if(!mqtt.connected())mqtt.connect("omp-climate-002","openmaker/2/availability",0,true,"offline");
      if(mqtt.connected())mqtt.publish("openmaker/2/availability","online",true);
    }
  }
  mqtt.loop(); if(now-sampled<SAMPLE_MS)return;sampled=now;
  float t=NAN,h=NAN,p=NAN;
  if(sensorReady){t=bme.readTemperature();h=bme.readHumidity();p=bme.readPressure()/100.0f;}
  bool valid=policy.update(t,h,p); if(!valid)sensorReady=false;
  color(!valid||policy.active,valid&&!policy.active,!valid);
  char payload[256];++sequence;
  if(valid)snprintf(payload,sizeof payload,"{\"project_id\":2,\"seq\":%lu,\"uptime_ms\":%lu,\"valid\":true,\"temperature_c\":%.2f,\"humidity_pct\":%.2f,\"pressure_hpa\":%.2f,\"alert\":%s}",(unsigned long)sequence,now,t,h,p,policy.active?"true":"false");
  else snprintf(payload,sizeof payload,"{\"project_id\":2,\"seq\":%lu,\"uptime_ms\":%lu,\"valid\":false,\"temperature_c\":null,\"humidity_pct\":null,\"pressure_hpa\":null,\"alert\":false}",(unsigned long)sequence,now);
  Serial.println(payload);if(mqtt.connected())mqtt.publish("openmaker/2/telemetry",payload,false);
  if(displayReady){oled.clearDisplay();oled.setTextSize(1);oled.setTextColor(SSD1306_WHITE);oled.setCursor(0,0);oled.println("Room Climate / ID 2");if(valid){oled.print(t);oled.println(" C");oled.print(h);oled.println(" % RH");oled.print(p);oled.println(" hPa");oled.println(policy.active?"HIGH TEMP ALERT":"Normal");}else oled.println("Sensor fault");oled.println(mqtt.connected()?"MQTT online":"MQTT offline");oled.display();}
}
