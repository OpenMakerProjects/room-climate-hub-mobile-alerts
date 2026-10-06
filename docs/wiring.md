# Wiring

The authoritative editable diagram is circuit-diagram.svg and the README pin table. Nano 3V3 powers BME280/OLED; GND shared with common-cathode RGB. A4 SDA and A5 SCL connect both I²C modules. BME CS high/SDO low selects 0x76; OLED 0x3C. D3/D5/D6 each through 1kΩ to red/green/blue anode. USB power only. No 5V sensor rail or mains wiring.
