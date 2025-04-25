## Block 7 – Power ON LED (12V DC Visual Indicator)

This block adds a visual indicator that confirms the Meanwell HDR-15-12 is supplying 12V DC.  
A simple blue LED, wired with a resistor, shows that the low-voltage system is active.

---

### Functional Role

- LED turns ON as soon as 12V DC is present
- LED turns OFF if 230V AC is lost or the Meanwell fails
- Useful for diagnostics and live status checks

---

### Wiring Diagram

```
[WAGO #1 (12V+)] ───┬─────────────┐
                   |             |
              [Resistor]       [Anode] ← LED (Blue)
                   |             |
                   +────────────→ [Cathode] ←─┐
                                             |
                                 [WAGO #2 (GND)]
```

---

### Component Details

| Component     | Value / Type         | Notes                                  |
|---------------|----------------------|----------------------------------------|
| LED           | 3mm or 5mm Blue      | Any low-power (typ. 20mA) indicator    |
| Resistor      | 330Ω – 470Ω, ¼ Watt  | In series with anode                   |
| Mounting      | Panel, snap-in, or DIN clip | Should be visible on front panel |

---

### Wire Specifications

| Line        | Color | Section     | From → To            |
|-------------|-------|-------------|----------------------|
| 12V+        | Red   | 0.25–0.5 mm²| WAGO #1 → Resistor   |
| GND         | Black | 0.25–0.5 mm²| LED Cathode → WAGO #2 |

---

### Behavior

| System Power | LED State | Meaning                         |
|--------------|-----------|---------------------------------|
| 12V DC OK    | ON        | Meanwell active – system live   |
| 12V DC Lost  | OFF       | System unpowered or fault       |

---

### Best Practices

- Mount LED in visible location on the IP65 front panel
- Use heatshrink over resistor/LED legs if not enclosed
- Optionally use a plug-in indicator module for DIN rail (if available)
- Use prewired LED holders to simplify maintenance
