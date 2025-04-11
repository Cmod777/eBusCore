## Block 5 – Shelly "TADO" (Power Control for Tado Unit)

This Shelly module controls the 230V AC power line that supplies the Tado controller.  
It acts as a smart switch, allowing automation or remote reset of the thermostat.  
It is powered by 12V DC and controls a separate 230V AC output via its internal relay.

---

### Power Wiring (DC Supply to Shelly)

```
[WAGO #1 (V+)] ──→ Shelly "TADO" 12V IN (+)
[WAGO #2 (GND)] ──→ Shelly "TADO" GND (−)
```

Same supply system as Shelly "AF".

---

### Relay Output Wiring (230V AC Switching)

```
[230V AC Live IN] ──→ Shelly "TADO" Relay COM
Shelly Relay NO ──→ [EXIT 1 - Tado Power Line]

[230V AC Neutral] ──→ [EXIT 1 - Tado Neutral Line] (direct)
```

### Diagram (Relay Control + Output)

```
+---------------------+
|     Shelly TADO     |
|  +12V DC   ─────┐    |
|  GND      ──────┘    |
|                     |
|  RELAY COM ──── L (Live 230V IN)      [From fuse or terminal block]
|  RELAY NO  ──── L (To Tado unit)      [EXIT 1 - Live]
|                     |
|          N (Neutral) ───────────────→ [EXIT 1 - Neutral] (direct)
+---------------------+
```

---

### WAGO Assignments

- **WAGO #5 (230V AC Live)**: split from main AC line to Shelly COM
- **WAGO #6 (230V Neutral)**: shared neutral line (goes directly to Tado)

---

### Wire Specifications

| Line               | Color   | Section     | From → To                       |
|--------------------|---------|-------------|---------------------------------|
| 12V IN (+)         | Red     | 0.5 mm²     | WAGO #1 → Shelly TADO           |
| 12V IN (GND)       | Black   | 0.5 mm²     | WAGO #2 → Shelly TADO           |
| 230V Live IN       | Brown   | 1.0–1.5 mm² | WAGO #5 → Shelly Relay COM      |
| 230V Live OUT      | Brown   | 1.0–1.5 mm² | Shelly Relay NO → EXIT 1        |
| 230V Neutral       | Blue    | 1.0–1.5 mm² | WAGO #6 → EXIT 1 Neutral        |

---

### Behavior

| Shelly Relay State | Tado Power | Result                           |
|--------------------|------------|----------------------------------|
| OFF (Open)         | Disabled   | Tado is powered off              |
| ON  (Closed)       | Enabled    | Tado receives 230V AC            |

---

### Configuration Tip (Shelly Web UI)

- Set default state to **ON** (or as needed for boot behavior)
- Optionally use this Shelly for:
  - Scheduled reboots of Tado
  - Power saving when away
  - Manual cut-off during tests

---

### Safety Notes

- All 230V lines must be properly fused.
- Use double-pole disconnection if local code requires.
- Keep low-voltage and 230V sections physically separated.
