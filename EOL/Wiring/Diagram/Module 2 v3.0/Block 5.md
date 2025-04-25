## Block 5 – Shared GND and Distribution Nodes

This block defines the shared GND and distribution system for stabilized and battery-powered 12V lines.  
All modules, relays, filters, and indicators reference a common GND point to ensure stability and isolation.

### Wiring Diagram

```
[Meanwell V−] → [GND Common WAGO Block]
[Battery − ] → [GND Common WAGO Block]
[Relay V−  ] → [GND Common WAGO Block]
[StepDown −] → [GND Common WAGO Block]
[Controller W1209 GND] → [GND Common]
[WiFi OUT− Filtered] → [GND Common]
[LEDs] → [GND Common]
[Switch −] → [GND Common]
```

### GND Mapping Table

| Component             | GND Connection          | Notes                                       |
|-----------------------|-------------------------|---------------------------------------------|
| Meanwell HDR-15-12    | Output V−               | Source of stabilized GND                    |
| Battery −             | Battery terminal −      | Connected via WAGO to shared GND            |
| StepDown IN− / OUT−   | Both tied to GND Common | For input and output regulation             |
| Relay V−              | To GND Common           | Powers relay coil                           |
| Controller W1209      | GND pin                 | Required for temperature control logic      |
| All LEDs              | Cathode side            | Common negative rail                        |
| Shelly Plus Uni       | GND input               | For reliable 12V operation                  |
| Filter COM2 Output    | For WiFi module         | Ensures safe return path                    |

### Best Practices

- Use large WAGO 5-way or 8-way terminal blocks for GND distribution  
- Keep GND wire section equal to power wires (≥1.0 mm²)  
- Avoid creating floating GNDs between battery and Meanwell  
- Check continuity of all negative rails with a multimeter  
- Keep GND lines as short and direct as possible
