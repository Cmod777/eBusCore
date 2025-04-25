## Block 8 – Physical Output Lines (EXIT 1, 2, 3)

This block defines the three physical exits of the control unit, each carrying different signals or power to external devices.

---

### EXIT 1 – To Tado Controller

**Purpose:**  
Delivers 230V AC and OT signal lines to the Tado thermostat.

**Contains:**
- **230V AC Live** (controlled by Shelly "TADO" relay)
- **230V AC Neutral** (direct)
- **OT BUS+** (connected to relay COM1 – Pin 11)
- **OT BUS−** (connected to relay COM2 – Pin 21)

**Wiring Diagram:**

```
230V LIVE  → Shelly "TADO" Relay NO ─→ EXIT 1 - L
230V NEUTRAL → WAGO #6              ─→ EXIT 1 - N
OT BUS+ → WAGO #3 → Relay COM1 (11) ─→ EXIT 1 - BUS+
OT BUS− → WAGO #4 → Relay COM2 (21) ─→ EXIT 1 - BUS−
```

---

### EXIT 2 – To Boiler

**Purpose:**  
Carries OT communication lines to the boiler, but **only** when the relay is active.

**Contains:**
- **OT BUS+** (from Relay NO1 – Pin 14)
- **OT BUS−** (from Relay NO2 – Pin 24)

**Wiring Diagram:**

```
Relay NO1 (14) ──→ EXIT 2 - BUS+
Relay NO2 (24) ──→ EXIT 2 - BUS−
```

---

### EXIT 3 – To Main Electrical Panel (Optional)

**Purpose:**  
Can carry a spare 230V AC line or service wire. Use as needed.

**Configuration Options:**
- Direct 230V AC passthrough (fused)
- Spare DC/GND line
- Monitoring probe or reset line

---

### Wire Specifications

| EXIT     | Line Type       | Color       | Section     | Notes                          |
|----------|------------------|-------------|-------------|--------------------------------|
| EXIT 1   | 230V Live        | Brown       | 1.0–1.5 mm² | From Shelly "TADO" NO          |
| EXIT 1   | 230V Neutral     | Blue        | 1.0–1.5 mm² | From WAGO #6                   |
| EXIT 1   | OT BUS+          | Yellow      | 0.5 mm²     | From Relay COM1 (11)           |
| EXIT 1   | OT BUS−          | Light Blue  | 0.5 mm²     | From Relay COM2 (21)           |
| EXIT 2   | OT BUS+          | Yellow      | 0.5 mm²     | From Relay NO1 (14)            |
| EXIT 2   | OT BUS−          | Light Blue  | 0.5 mm²     | From Relay NO2 (24)            |
| EXIT 3   | Optional         | Custom      | Custom      | Use as needed                  |

---

### Labels & Best Practices

- Clearly label each exit:
  - `EXIT 1 – TADO`
  - `EXIT 2 – BOILER`
  - `EXIT 3 – AUX`
- Use cable glands or DIN exit blocks to maintain IP65 rating
- Always test continuity and switching behavior after installation
- Document actual wire color codes used on final build

---

### Summary Table

| EXIT   | Purpose            | Controlled By       | Type         |
|--------|--------------------|---------------------|--------------|
| EXIT 1 | Tado unit          | Shelly "TADO" relay | 230V + OT    |
| EXIT 2 | Boiler connection  | Finder relay        | OT only      |
| EXIT 3 | Auxiliary / Spare  | Optional            | Flexible     |
