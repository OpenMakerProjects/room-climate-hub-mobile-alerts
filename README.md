# Room Climate Hub Mobile Alerts

Build a smart home prototype that uses BME280, OLED display, RGB LED to send timely mobile notifications. Include setup instructions, a circuit diagram, tested firmware, and sample output.

## Project details

| Field | Value |
| --- | --- |
| Roadmap ID | 2 |
| Category | Smart Home |
| Platform | Arduino Nano 33 IoT |
| Difficulty | Intermediate |
| Estimated build time | 24 hours |
| Connectivity | MQTT |
| Core components | BME280, OLED display, RGB LED |
| Control mode | threshold alert |

## Repository layout

- `firmware/room-climate-hub-mobile-alerts/room-climate-hub-mobile-alerts.ino`: runnable firmware or application
- `docs/wiring.md`: suggested low-voltage wiring plan
- `docs/architecture.md`: system data flow
- `docs/test-plan.md`: repeatable verification steps
- `sample-data/example.json`: example telemetry record
- `tools/validate.py`: dependency-free repository validation

## Quick start

1. Open `firmware/room-climate-hub-mobile-alerts/room-climate-hub-mobile-alerts.ino` in Arduino IDE or Arduino CLI.
2. Select the board matching **Arduino Nano 33 IoT**.
3. Compile and upload, then open the serial monitor at 115200 baud.

## Expected behavior

Mobile Alerts demonstration with repeatable test steps. The default implementation supports simulated or generic analog inputs so the control path can be exercised before hardware-specific drivers are added.

## Hardware adaptation

The included code is a safe reference implementation. Update pin assignments and sensor conversions from the exact component datasheets, then repeat the test plan before connecting actuators.

## License

MIT
