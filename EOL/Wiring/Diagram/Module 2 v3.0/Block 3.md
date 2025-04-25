## Block 3 – StepDown & Relay Output Filtering + WiFi Supply

This block manages the conversion of 12V battery power to 5V for the eBus WiFi module.  
It also routes the StepDown output through a relay and filtering stage before reaching the WiFi module, ensuring power is only delivered during grid failure and is clean and safe.

### Wiring Diagram

```
[BATTERY] → [Switch] → [Relay V+]
                     [Relay V−] → [GND Common]

[StepDown IN+ ] ← Connected to Relay V+
[StepDown IN− ] ← [GND Common]

[StepDown OUT+ ] → [Relay NO1]
[StepDown OUT− ] → [Relay NO2]

[Relay COM1] → [Filter: 1000µF + 220µF Caps] → [DIODE 1N5819] → [WiFi Module +5V]
[Relay COM2] → [Filter: 1000µF + 220µF Caps] → [WiFi Module GND]
```

### Terminal Connections

| Element          | Direction     | Wire Color | Notes                                                    |
|------------------|---------------|------------|----------------------------------------------------------|
| Relay NO1        | Input         | Red        | Receives +5V from StepDown output                        |
| Relay NO2        | Input         | Black      | GND from StepDown                                        |
| Relay COM1       | Output        | Red        | Filtered and routed to eBus WiFi via diode               |
| Relay COM2       | Output        | Black      | Filtered GND to eBus WiFi                                |
| Filter Caps      | Parallel      | —          | Typically 1000µF + 220µF electrolytic capacitors         |
| Filter Diode     | Series        | —          | Prevents reverse flow into StepDown                     |
| StepDown OUT+    | Output        | Red        | Routed through relay to WiFi                            |
| StepDown OUT−    | Output        | Black      | Routed through relay to WiFi                            |

### Behavior Matrix

| Grid Power | Relay State | 5V Output Active | Notes                              |
|------------|-------------|------------------|------------------------------------|
| ON         | Open        | No               | WiFi module not powered            |
| OFF        | Closed      | Yes              | Battery powers WiFi through relay  |
| Battery OFF| —           | No               | Everything isolated                |

### Best Practices

- Use electrolytic capacitors with low ESR for filtering  
- Add LED indicator after diode to verify 5V presence  
- Mount relay on DIN securely with good contact on terminals  
- Keep StepDown module accessible for replacement or adjustment  
- Ensure WiFi module wiring is short and stable
