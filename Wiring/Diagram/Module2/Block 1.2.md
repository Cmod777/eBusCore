# Module 2 – UPS Backup Unit

## Block 1 – 230V AC Power Input to Meanwell HDR-15-12

This block provides the main AC power to the UPS control unit.  
The 230V AC input powers the Meanwell HDR-15-12, which generates a 12V DC line used to trigger the UPS relay and monitor presence of the grid.

---

### Wiring Diagram

```
[AC MAIN SUPPLY]
     |
     |----[ L ] (Live - Brown) -----------+
     |                                     |
     |----[ N ] (Neutral - Blue) --------+ |
     |                                  | |
     |                                  v v
                           +------------------------+
                           | Meanwell HDR-15-12     |
                           |                        |
                           |   [ L ] ← AC Live      |
                           |   [ N ] ← AC Neutral   |
                           |   [ ⏚ ] ← PE Ground    |
                           +------------------------+
```

---

### Terminal Connections

| Terminal | Source        | Wire Color | Section    | Notes                           |
|----------|---------------|------------|------------|---------------------------------|
| L        | 230V Live     | Brown      | 1.0–1.5 mm²| Fused input                     |
| N        | 230V Neutral  | Blue       | 1.0–1.5 mm²| Standard neutral line           |
| ⏚ (PE)   | Earth/Ground  | Green/Yellow | 1.0–2.5 mm²| To DIN rail or grounding bar    |

---

### Output

The Meanwell converts the AC input to a stable 12V DC used for:
- Powering the **normally open relay coil**
- Activating **status LEDs**
- Optionally triggering **UPS logic or battery indicators**

---

### Behavior

| AC Input Present | 12V DC Available | Relay State | Notes                       |
|------------------|------------------|-------------|-----------------------------|
| Yes              | Yes              | Open        | Normal operation (no UPS)   |
| No               | No               | Closed*     | Battery takes over          |

> *Relay closes via fail-safe battery circuit (next block)

---

### Best Practices

- Use DIN rail fuse before Meanwell input
- Secure the Meanwell firmly to DIN rail
- Test 12V output with multimeter before connecting loads
- Label wires clearly for AC and DC lines
