## Block 4 – Shelly "AF" (Relay Trigger for OT Bus Control)

The Shelly "AF" is responsible for enabling or disabling the OpenTherm (OT) communication by controlling the Finder relay coil.  
It receives 12V power from the Meanwell, and its internal relay output is connected directly to the relay coil (A1/A2).  
This module allows remote or automated control of the OT bus line.

---

### Power Wiring (DC Supply)

```
[WAGO #1 (V+)] ──→ Shelly "AF" 12V IN (+)
[WAGO #2 (GND)] ──→ Shelly "AF" GND (−)
```

Shelly boots and connects to Wi-Fi upon receiving 12V DC.

---

### Relay Output Wiring (Dry Contact)

```
Shelly Relay OUT:
    - COM   → Finder A1
    - NO    → Finder A2

NOTE: 
- The Shelly relay acts as a dry contact (no voltage output)
- It simply closes the circuit between A1 and A2 when ON
- A1 and A2 are already wired to 12V+ and GND respectively
```

### Full Diagram

```
+---------------------+
|     Shelly AF       |
|  +12V DC   ─────┐    |
|  GND      ──────┘    |
|                     |
|  RELAY COM ──┐       |
|  RELAY NO  ──┴───→ [Relay A1]
|                     |
|                [Relay A2] ←── GND (WAGO #2)
+---------------------+
```

---

### Behavior

| Shelly Relay State | OT Bus Relay (Finder) | Result                          |
|--------------------|------------------------|----------------------------------|
| OFF (Open)         | A1 and A2 open         | Relay inactive → OT disconnected |
| ON  (Closed)       | A1–A2 connected        | Relay active  → OT connected     |

---

### Wire Specifications

| Line          | Color  | Section     | From → To              |
|---------------|--------|-------------|-------------------------|
| DC IN (+12V)  | Red    | 0.5 mm²     | WAGO #1 → Shelly AF     |
| DC IN (GND)   | Black  | 0.5 mm²     | WAGO #2 → Shelly AF     |
| Relay COM     | White  | 0.5 mm²     | Shelly AF → Relay A1    |
| Relay NO      | Grey   | 0.5 mm²     | Shelly AF → Relay A2    |

---

### Configuration Tip (Shelly Web UI)

- Set relay type to **Toggle** or **Edge mode** depending on automation logic
- Optionally connect to **Home Assistant** via MQTT or Shelly integration
- Default state: **OFF**, to keep OT bus disconnected by default if needed

---

### Safety Note

- The Shelly relay output must **not** inject external voltage; it must remain a pure contact.
- Never connect A1/A2 to both Shelly and Meanwell V+/GND in parallel — they must pass through Shelly only.
