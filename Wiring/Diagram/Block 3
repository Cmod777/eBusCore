## Block 3 – Relay Wiring (Finder 40.52 – DPDT 12V DC)

This block manages the physical disconnection and reconnection of the OT (OpenTherm) communication lines (BUS+ and BUS−) between the Tado unit and the boiler.  
The relay is activated by Shelly "AF" via 12V DC, switching both lines simultaneously (double-pole, double-throw).

---

### Relay Overview

**Model:** Finder 40.52  
**Type:** DPDT (Double Pole, Double Throw)  
**Coil Voltage:** 12V DC  
**Mounting:** PCB or DIN rail socket (e.g. 95.05 base)

---

### Relay Pinout (Top View)

```
  +----+----+----+----+----+----+
  | 11 | 12 | 14 |    | 21 | 22 | 24 |
  +----+----+----+----+----+----+----+

    COIL:
    - A1: 12V+ (from WAGO #1)
    - A2: GND (from WAGO #2)

    SWITCHING CONTACTS:
    - 11 → COM1 (BUS+ input from Tado)
    - 14 → NO1  (BUS+ output to Boiler)
    - 12 → NC1  (not used)

    - 21 → COM2 (BUS− input from Tado)
    - 24 → NO2  (BUS− output to Boiler)
    - 22 → NC2  (not used)
```

---

### Wiring Diagram (OT Line Switching)

```
                    [BUS+ from Tado]
                            |
                            v
                          [11] ← COM1
                          [14] → NO1 → [BUS+ to Boiler]

                    [BUS− from Tado]
                            |
                            v
                          [21] ← COM2
                          [24] → NO2 → [BUS− to Boiler]

                  [COIL TERMINALS]
                          A1 ← 12V+ (WAGO #1)
                          A2 ← GND  (WAGO #2)
```

---

### WAGO Assignments

| WAGO ID | Function                      | Description                         |
|---------|-------------------------------|-------------------------------------|
| WAGO #3 | OT BUS+ Line (split)          | Feeds COM1 from Tado, outputs to Boiler |
| WAGO #4 | OT BUS− Line (split)          | Feeds COM2 from Tado, outputs to Boiler |

---

### Wire Specifications

| Line        | Color     | Section     | From → To                       |
|-------------|-----------|-------------|---------------------------------|
| BUS+ in     | Yellow    | 0.5–0.75 mm²| Tado → WAGO #3 → COM1 (Pin 11)  |
| BUS+ out    | Yellow    | 0.5–0.75 mm²| NO1 (Pin 14) → Boiler           |
| BUS− in     | Blue      | 0.5–0.75 mm²| Tado → WAGO #4 → COM2 (Pin 21)  |
| BUS− out    | Blue      | 0.5–0.75 mm²| NO2 (Pin 24) → Boiler           |
| Coil A1     | Red       | 0.5 mm²     | WAGO #1 → A1                    |
| Coil A2     | Black     | 0.5 mm²     | WAGO #2 → A2                    |

---

### Behavior

- **Relay inactive (Shelly OFF):**
  - No connection between Tado and boiler (BUS lines open)
- **Relay active (Shelly ON):**
  - COM1–NO1 and COM2–NO2 closed → OT line passes through
  - Communication between Tado and boiler is established
- Switching both poles avoids floating voltage or interference

---

### Best Practices

- Always switch both BUS+ and BUS− to ensure signal integrity
- Keep OT lines twisted together for noise immunity
- Relay should click cleanly when triggered by Shelly (audible)
- Mount relay base securely if using DIN socket (Finder 95.05)
