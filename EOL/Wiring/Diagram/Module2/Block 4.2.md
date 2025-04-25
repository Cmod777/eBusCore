## Block 4 – Battery Block (12V SLA Backup)

This block supplies backup power when 230V AC is not available.  
A 12V Sealed Lead-Acid (SLA) battery is connected via WAGO terminals and feeds the relay switch for UPS activation.

---

### Battery Type

| Parameter        | Value                           |
|------------------|----------------------------------|
| Voltage          | 12V DC                           |
| Capacity         | 1.2Ah – 7Ah (depending on size)  |
| Type             | Sealed Lead-Acid (VRLA / AGM)    |
| Output           | 2 wires (V+ / V−)                |

---

### Wiring Diagram

```
+-----------------------+
| 12V SLA Battery       |
|                       |
|   [+] ───────────────→ WAGO #3 (Battery V+)
|   [−] ───────────────→ WAGO #4 (Battery GND)
+-----------------------+
```

These WAGO terminals are used as distribution points:
- **WAGO #3**: Battery V+ → to Relay COM
- **WAGO #4**: Battery GND → to Step-Down input GND

---

### Wire Specifications

| Line      | Color  | Section     | From → To                  |
|-----------|--------|-------------|----------------------------|
| V+        | Red    | 1.0–1.5 mm² | Battery + → WAGO #3        |
| GND       | Black  | 1.0–1.5 mm² | Battery − → WAGO #4        |

---

### Fuse

- Use a **1A–2A fuse** between battery positive and WAGO #3  
- Fuse must be:
  - Inline (blade or barrel)
  - Close to battery terminal

---

### Behavior Summary

| Grid Power | Battery Output | Connected Load | Relay State     |
|------------|----------------|----------------|-----------------|
| Present    | Idle/float     | None           | Coil ON (open)  |
| Absent     | Active         | Step-down 5V   | Coil OFF (closed) |

---

### Mounting Tips

- Use **battery clips** or foam pads to secure battery inside DIN case
- Ensure air circulation or use thermal cut-off fuse in case of heat buildup
- Position battery so terminals are easily accessible but not exposed

---

### Optional Expansion

- Add a **charging module** to keep SLA topped up when grid is present (not shown here)
- Add **voltage sensor** (ADC) to monitor battery status via Home Assistant

---

### Safety Notes

- Never short battery terminals
- Replace battery every 3–5 years depending on usage
- Mark battery polarity clearly near WAGO terminals
