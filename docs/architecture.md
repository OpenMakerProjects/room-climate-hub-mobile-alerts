# Architecture

BME280 → Nano I²C → three-sample temperature policy → OLED/RGB and non-retained MQTT telemetry → Python bridge → configured ntfy HTTP API → subscribed phone. The Nano's availability last will is retained. Sensor/display remain local during network outage. Notification delivery is best-effort with in-memory five-minute cooldown, no offline queue. See README for exact pins, thresholds, security limitations and setup.
