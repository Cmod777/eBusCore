## Block 1 – 230V AC Power Input to Meanwell HDR-15-12

This block provides primary AC power to the system. The 230V line feeds the Meanwell HDR-15-12 power supply, which then generates a regulated 12V DC output used by all low-voltage devices.

---

### Wiring Diagram

```
[AC MAIN SUPPLY]
     |
     |----[ L ] (Live - Brown) -----------+
     |                                     |
     |----[ N ] (Neutral - Blue) --------+ |  
     |                                  | |
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

### Connections

- **L (Live)**:  
  - Connect to 230V AC live wire (brown)  
  - Recommended via a DIN rail fuse (e.g. 2A slow-blow)

- **N (Neutral)**:  
  - Connect to 230V AC neutral wire (blue)

- **⏚ PE (Protective Earth)**:  
  - Connect to DIN rail grounding bar (green/yellow wire)

---

### Wire Specifications

| Connection | Color     | Section    | Notes                       |
|------------|-----------|------------|-----------------------------|
| Live (L)   | Brown     | 1.0–1.5 mm² | Fused via DIN rail fuse     |
| Neutral (N)| Blue      | 1.0–1.5 mm² | Standard neutral connection |
| PE (⏚)     | Green/Yellow | 1.0–2.5 mm² | To DIN rail grounding bus |

---

### Behavior

- When 230V AC is present, the Meanwell supplies stable 12V DC on its output terminals.
- This voltage powers **Shelly modules**, **the Finder relay**, **status LEDs**, and other low-voltage parts of the system.
- If 230V AC is lost, all 12V-powered logic in this module stops functioning.

---

### Additional Notes

- The HDR-15-12 is a DIN rail mountable power supply with a compact footprint.
- If space allows, you can add a **status LED** (230V AC indicator) in parallel with the input, using a 230V LED module.

---

```

Front view of the Meanwell HDR-15-12 terminals:

[ ⏚ ] [ L ] [ N ] || [ V+ ] [ V- ]
```

You will use the three leftmost terminals for AC input.  
Next block will describe how to distribute the 12V DC output to all devices via WAGO terminals.
