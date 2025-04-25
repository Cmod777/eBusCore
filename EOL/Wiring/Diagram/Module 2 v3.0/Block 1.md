# Module 2 – UPS Backup Unit (v3.0)

## Block 1 – 230V AC Input to Meanwell HDR-15-12

This block handles the input of 230V AC from Module 1 (Main Control Unit) and converts it to 12V DC using the Meanwell HDR-15-12 power supply.  
The 12V line becomes the stabilized power rail for the entire UPS logic and battery charge control.

### Wiring Diagram

```
[AC MAIN SUPPLY (from Module 1)]
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
                                     |
                                     |
                                  [DC OUTPUT]
                                     |
                          +----------+-----------+
                          |                      |
                          v                      v
                 [ V+ ] Stabilized 12V     [ V− ] GND
```

### Terminal Connections

| Terminal | Source        | Wire Color     | Section      | Notes                              |
|----------|---------------|----------------|--------------|------------------------------------|
| L        | 230V Live     | Brown          | 1.0–1.5 mm²  | Fused input from Module 1          |
| N        | 230V Neutral  | Blue           | 1.0–1.5 mm²  | Neutral line from Module 1         |
| ⏚ (PE)   | Earth/Ground  | Green/Yellow   | 1.0–2.5 mm²  | To DIN rail or grounding bar       |
| V+       | DC Output     | Red            | 1.0 mm²      | Feeds stabilized 12V to all logic  |
| V−       | DC Ground     | Black          | 1.0 mm²      | Common ground for UPS system       |

### DC Output Usage

The 12V DC output (V+ / V−) from the Meanwell powers:
- All 12V logic and control devices (e.g., W1209, Shelly Uni)
- Battery charge path (via PTC and diode)
- Status LEDs (Power, Charging, etc.)
- Relay input (when powered from grid)

### Behavior Matrix

| Grid Power | Meanwell 12V | Relay State | Notes                                  |
|------------|---------------|-------------|----------------------------------------|
| ON         | Present       | Open        | Grid powers all logic, battery charges |
| OFF        | Absent        | Closed      | Battery takes over via UPS failover    |

> The relay is powered via **battery-only**, so it activates only during power failure.

### Best Practices

- Install a DIN rail **AC fuse** upstream of the Meanwell input  
- Use clear color-coded wires (brown, blue, green/yellow, red, black)  
- Mount Meanwell horizontally with adequate spacing  
- Label **V+** and **V−** rails as "12V Stabilized"  
- Test output with a multimeter before connecting sensitive loads
