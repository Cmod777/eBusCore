## Block 6 – OpenTherm BUS Wiring (Tado ↔ Relay ↔ Boiler)

This block handles the communication bus between the Tado controller and the boiler using the OpenTherm protocol (2-wire, polarity-free).  
The relay (Finder 40.52 DPDT) is used to physically connect or disconnect the BUS+ and BUS− lines, providing full control over the communication path.

---

### Physical Path Overview

```
[TADO OT BUS+] ──┐
                 ├─→ [WAGO #3] ──→ [Relay COM1 - Pin 11]
                                └─→ [Relay NO1 - Pin 14] ──→ [EXIT 2 - OT BUS+ to Boiler]

[TADO OT BUS−] ──┐
                 ├─→ [WAGO #4] ──→ [Relay COM2 - Pin 21]
                                └─→ [Relay NO2 - Pin 24] ──→ [EXIT 2 - OT BUS− to Boiler]
```

---

### Relay Role Recap

- **COM1 / COM2** → connected to Tado
- **NO1 / NO2** → connected to Boiler
- **Relay active** → COM and NO closed → OT communication active
- **Relay inactive** → COM and NO open → OT communication broken

---

### WAGO Assignments

| WAGO ID | Function            | Connected Lines                     |
|---------|---------------------|-------------------------------------|
| WAGO #3 | OT BUS+ distribution | Tado → Relay COM1 → Relay NO1 → Boiler |
| WAGO #4 | OT BUS− distribution | Tado → Relay COM2 → Relay NO2 → Boiler |

---

### Wire Specifications

| Line               | Color  | Section     | From → To                       |
|--------------------|--------|-------------|---------------------------------|
| OT BUS+ from Tado  | Yellow | 0.5 mm²     | EXIT 1 → WAGO #3 → COM1 (11)    |
| OT BUS− from Tado  | Blue   | 0.5 mm²     | EXIT 1 → WAGO #4 → COM2 (21)    |
| OT BUS+ to Boiler  | Yellow | 0.5 mm²     | NO1 (14) → EXIT 2               |
| OT BUS− to Boiler  | Blue   | 0.5 mm²     | NO2 (24) → EXIT 2               |

---

### Connectors (EXITs)

- **EXIT 1 → Tado**
  - 230V AC (from Shelly "TADO")
  - OT BUS+ and BUS− lines (go to COM1/COM2)

- **EXIT 2 → Boiler**
  - OT BUS+ and BUS− (from NO1/NO2, only connected when relay is active)

---

### Behavior Summary

| Relay State  | OT BUS+ / BUS− Path   | Communication Status       |
|--------------|------------------------|----------------------------|
| OFF (Open)   | No connection          | Tado cannot talk to boiler |
| ON  (Closed) | Full pass-through      | OT communication enabled   |

---

### Best Practices

- Use twisted-pair for OT BUS+ and BUS− to reduce interference
- Ensure WAGO terminals are labeled clearly
- Never let BUS+ / BUS− float — either fully connected or fully open via relay
- Avoid running BUS lines near high-voltage AC to prevent signal degradation
