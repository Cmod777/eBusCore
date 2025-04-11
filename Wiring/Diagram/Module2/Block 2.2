## Block 2 – 12V DC Distribution (From Meanwell HDR-15-12)

This block handles the distribution of the 12V DC output from the Meanwell power supply to:

- The **relay coil** that switches to battery mode during blackout
- Optional **LED indicators** (e.g., power ON)
- Future monitoring or control logic (optional)

---

### Wiring Diagram

```
[Meanwell HDR-15-12]
       |
       +-- [ V+ ] ────┬───────────────────────+
                      |                       |
                      |                       v
                      |                [WAGO #1 – V+ 12V]
                      |
                      +──────────────→ [Relay Coil A1]
                      |
                      +──────────────→ [LED Power ON Anode]

[ V− ] ───────────────→ [WAGO #2 – GND 12V]
                               |              |
                               |              +→ [Relay Coil A2]
                               +→ [LED Cathode]
```

---

### WAGO Assignments

| WAGO ID | Voltage | Connected Devices                     |
|---------|---------|----------------------------------------|
| #1      | V+ 12V  | Relay A1, LED Anode, future logic IN   |
| #2      | GND     | Relay A2, LED Cathode, shared ground   |

---

### Components Powered

- **Relay coil (Normally Open)**
  - A1 → WAGO #1
  - A2 → WAGO #2

- **Optional LED Power ON**
  - Anode → WAGO #1
  - Cathode → WAGO #2
  - Series resistor: 330–470Ω, ¼ W

---

### Wire Specifications

| Line        | Color   | Section     | From → To              |
|-------------|---------|-------------|-------------------------|
| V+ 12V DC   | Red     | 0.5–1.0 mm² | Meanwell → WAGO #1      |
| GND         | Black   | 0.5–1.0 mm² | Meanwell → WAGO #2      |
| Coil wires  | White   | 0.5 mm²     | WAGOs → Relay A1/A2     |
| LED wires   | Blue/Red| 0.25–0.5 mm²| WAGOs → LED             |

---

### Behavior

| Grid Power | Meanwell Output | Relay Coil | LED Status     | System Mode   |
|------------|------------------|------------|----------------|---------------|
| Present    | 12V active       | Energized  | ON (if present)| Grid mode     |
| Lost       | 12V off          | Off        | OFF            | Battery mode  |

---

### Safety Notes

- Use ferrules on all WAGO entries
- Use strain relief for LED/relay wires near the enclosure
- Keep 12V and battery systems isolated where needed

---

### Optional Expansion

- You may add additional WAGOs for logic signal feeds
- A monitoring module (e.g., ESP32) can be powered from WAGO #1 / #2 if required
