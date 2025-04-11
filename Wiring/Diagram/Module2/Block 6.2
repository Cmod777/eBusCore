## Block 6 – LED Indicators (Power, Charging, Battery Active, Full)

This block provides visual status feedback using 4 colored LEDs mounted on the panel or DIN-clip base.  
Each LED is powered from a different source or condition depending on the system state.

---

### LED Summary Table

| LED Color | Function             | Powered By                | Behavior                           |
|-----------|----------------------|---------------------------|------------------------------------|
| Blue      | Power ON (12V OK)    | 12V from Meanwell         | ON when grid is active             |
| Green     | Battery Charging     | From external charger     | ON while charging (optional)       |
| Red       | Battery in Use       | From battery via relay    | ON when system is in UPS mode      |
| White     | Battery Full         | From charger or monitor   | ON when battery fully charged      |

---

### Wiring Diagram Example (for Blue and Red LEDs)

```
[WAGO #1 – 12V V+] ────[330Ω]───> [LED Blue Anode]
                                 [LED Cathode] ───→ [WAGO #2 – GND]

[Battery V+] ──────[Relay NO]───────[330Ω]───> [LED Red Anode]
                                           [LED Cathode] ──→ [WAGO #4 – GND]
```

> Each LED uses a resistor (330–470Ω, ¼ W) in series with the **anode (+)**.  
> Cathode (−) goes to GND via shared WAGO.

---

### WAGO Assignments

| WAGO ID | Voltage         | Usage                          |
|---------|------------------|-------------------------------|
| WAGO #1 | 12V V+ from Meanwell | Power LED (Blue)           |
| WAGO #2 | GND (from Meanwell)  | Common GND for logic       |
| WAGO #3 | Battery V+           | Red LED (Battery Active)   |
| WAGO #4 | Battery GND          | Cathode for Red LED        |

---

### Wire Specifications

| Line         | Color     | Section     | From → To                       |
|--------------|-----------|-------------|----------------------------------|
| LED V+       | Match LED | 0.25–0.5 mm²| WAGO → Resistor → LED Anode     |
| LED GND      | Black     | 0.25–0.5 mm²| LED Cathode → WAGO GND          |

---

### Behavior Summary

| Grid | Battery | Charging | LEDs Active               |
|------|---------|----------|---------------------------|
| ON   | Float   | Optional | Blue                      |
| OFF  | Active  | No       | Red                       |
| ON   | Full    | No       | Blue + White              |
| ON   | Charging| Yes      | Blue + Green              |

---

### Best Practices

- Use panel-mount LEDs with built-in resistors where possible
- Label each LED clearly on the panel (or silkscreen if custom PCB)
- Secure wires to avoid disconnections due to vibration
- Optionally add a test jumper or switch to simulate blackout state

---

### Optional Logic (Future)

- Connect LED status lines to an ADC or GPIO input on a microcontroller
- Publish LED states to Home Assistant via ESP32 or ESP8266
