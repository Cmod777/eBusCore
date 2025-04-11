## Block 2 – 12V DC Distribution from Meanwell HDR-15-12

This block distributes the 12V DC output from the Meanwell power supply to all internal components of the control unit: Shelly modules, relay coil, and the Power ON LED.  
Distribution is managed via WAGO 3-way terminals for both V+ and GND.

---

### Wiring Diagram

```
             +-------------------------------+
             | Meanwell HDR-15-12 (12V DC)   |
             |                               |
             |   [ V+ ] →──+                 |
             |              \                |
             |               \               |
             |                \              |
             |                 +─→ [WAGO #1] →───+
             |                                | 
             |   [ V− ] →──+                 | |
             |              \                | |
             |               \               v v
             |                \        +-----------------+
             +----------------+        | Devices Powered |
                                       |                 |
                                       | - Shelly "AF"   |
                                       | - Shelly "TADO" |
                                       | - Relay A1/A2   |
                                       | - Power LED     |
                                       +-----------------+
```

---

### Terminal Distribution (WAGO)

| WAGO ID | Line | Function                         | Connected Devices                          |
|---------|------|----------------------------------|--------------------------------------------|
| WAGO #1 | V+   | Distributes +12V DC              | Shelly "AF", Shelly "TADO", Relay A1, LED+ |
| WAGO #2 | GND  | Common ground (−12V)             | Shelly "AF", Shelly "TADO", Relay A2, LED− |

---

### Pin Connections by Device

#### Relay (Finder 40.52)
- A1 → WAGO #1 (V+)
- A2 → WAGO #2 (GND)

#### Shelly “AF”
- DC IN (+)  → WAGO #1 (V+)
- DC IN (−) → WAGO #2 (GND)

#### Shelly “TADO”
- DC IN (+)  → WAGO #1 (V+)
- DC IN (−) → WAGO #2 (GND)

#### Power ON LED
- Anode (+) → WAGO #1 (V+)
- Cathode (−) → WAGO #2 (GND)
- Inline resistor (330–470 Ω) in series with anode

---

### Wire Specifications

| Destination       | Color  | Section     | Notes                        |
|-------------------|--------|-------------|------------------------------|
| V+ (12V DC)       | Red    | 0.5–1.0 mm² | From Meanwell to WAGO #1    |
| GND (12V DC)      | Black  | 0.5–1.0 mm² | From Meanwell to WAGO #2    |
| LED wiring        | Red/Black | 0.25–0.5 mm² | With inline resistor         |

---

### Behavior

- As soon as 230V AC is present, 12V DC becomes available.
- All devices powered via WAGO terminals activate:
  - The Shelly modules boot
  - The relay is ready for trigger
  - The LED lights up to indicate the system is live
- If 230V fails, the entire logic side of this control unit is shut off.

---

### Best Practices

- Keep V+ and GND pairs physically close to reduce loop area.
- Use ferrules on wires going into WAGO terminals for safety and maintenance.
- Secure WAGO terminals to DIN rail using adhesive or clip bases if needed.
