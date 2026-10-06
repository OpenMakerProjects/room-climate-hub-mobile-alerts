#pragma once
// Copy config.local.example.h to config.local.h; it is gitignored.
#if __has_include("config.local.h")
#include "config.local.h"
#else
#define WIFI_SSID ""
#define WIFI_PASSWORD ""
#define MQTT_HOST ""
#endif
constexpr unsigned MQTT_PORT=1883;
constexpr unsigned char BME_ADDRESS=0x76, OLED_ADDRESS=0x3c;
constexpr unsigned char LED_R=3, LED_G=5, LED_B=6;
constexpr unsigned long SAMPLE_MS=2000, RETRY_MS=15000;
