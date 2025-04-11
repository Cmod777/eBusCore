## Block 3 – Relay Wiring (Blackout Switch – Battery to Step-Down)

This block handles automatic failover.  
The **relay is normally open (NO)** and kept active by the 12V line from the Meanwell.  
If the grid goes down, the coil loses power → the relay **closes** and connects the 12V battery to the USB-C step-down converter.

---

### Functional Behavior

| Condition        | Coil State | Relay Contact | Battery → Step-Down | Power to eBUS |
|------------------|------------|----------------|----------------------|---------------|
| Grid Present     | Energized  | OPEN           | Disconnected         | Grid-powered  |
| Grid Absent      | Coil OFF   | CLOSED         | Connected            | Battery mode  |

---

### Relay Type

- **SPST** (Single Pole, Single Throw)
- **Normally Open** (closes on coil drop)
- Coil: 12V DC
- Contact rating: ≥2A @ 12V DC

---

### Wiring Diagram

```
               +------------------------------+
               |         12V BATTERY          |
               |         (Sealed SLA)         |
               +---------------+--------------+
                               |
                              [WAGO #3 – V+ Battery]
                               |
                               +────────────┐
                                            |
                                      [ Relay COM ]
                                      [ Relay NO  ] ────→ [ 12V IN – Step-Down 12V → 5V ]
                                                                 |
                                                                [ GND from WAGO #4 ]
```

---

### Coil Side (powered by Meanwell)

```
[WAGO #1 – 12V+] ──→ A1 (Relay Coil +)
[WAGO #2 – GND  ] ──→ A2 (Relay Coil −)
```

---

### Contact Side (Battery → USB Step-Down)

| Contact | Wire | From → To                      | Color     | Section     |
|---------|------|--------------------------------|-----------|-------------|
| COM     | V+   | Battery + (via WAGO #3)        | Red       | 1.0 mm²     |
| NO      | V+   | Step-Down IN (12V)             | Red       | 1.0 mm²     |

Battery GND goes to:
```
[Battery −] ─→ [WAGO #4 – GND] ─→ [Step-Down GND Input]
```

---

### WAGO Assignments

| WAGO ID | Function               | Connected Devices                      |
|---------|------------------------|----------------------------------------|
| #3      | Battery V+             | Battery → Relay COM → Step-Down        |
| #4      | Battery GND (shared)   | Battery − → Step-Down GND              |

---

### Behavior Summary

- **Relay coil powered → NO is open** → Battery is disconnected
- **Relay coil unpowered → NO closes** → Battery powers USB converter

---

### Safety Notes

- Insert a **fuse (1–2A)** between battery and relay COM
- Use thick cable for battery lines (1.0 mm² or more)
- Always use a sealed or enclosed relay for safety

---

### Optional Expansion

- A manual override switch can be added in parallel to relay contact for maintenance
- Battery voltage monitor (e.g., ADC on ESP32) can tap off WAGO #3
