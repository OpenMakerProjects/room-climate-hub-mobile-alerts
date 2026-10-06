# Repeatable tests

Run the README host and board commands. Policy tests cover three-sample confirmation, hysteresis, invalid readings, and reset of consecutive counts. Bridge tests mock external delivery and cover cooldown, recovery, bad telemetry, failure retries and destination validation. PNG tests prove rejection of corrupt/noncanonical transport. After assembling actual hardware, independently test addresses, 3.3V signals, displayed values, fault indication, MQTT disconnect/reconnect and phone delivery. Those physical tests have not been performed by automation.
