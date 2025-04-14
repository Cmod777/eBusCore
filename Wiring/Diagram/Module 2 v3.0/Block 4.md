## Block 4 – Status LEDs and Indicators

This block provides visual feedback on the status of the UPS system using 12V LEDs.  
Each LED indicates a specific condition such as power presence, battery charging, UPS active state, or standby.

### Wiring Diagram

```
[Meanwell V+ Stabilized] → [LED1: POWER ON] → [GND Common]
[Charging Path (after PTC+Diode)] → [LED2: BATTERY CHARGING] → [GND Common]
[UPS Switch OUT+] → [LED3: UPS ACTIVE] → [GND Common]
[WiFi Filter Output +5V] → [LED4: WIFI READY] → [GND Common]
[LED Logic Node (if charging OFF & UPS OFF)] → [LED5: BATTERY FULL / STANDBY] → [GND Common]
```

### LED Table

| LED # | Name              | Source Voltage                        | Trigger Condition                     | Wire Color | Notes                                           |
|-------|-------------------|----------------------------------------|----------------------------------------|------------|-------------------------------------------------|
| 1     | POWER ON          | 12V Stabilized (Meanwell V+)          | Grid power available                   | Red        | Always on when grid is active                  |
| 2     | BATTERY CHARGING  | After PTC + Diode                     | Battery is charging                    | Orange     | Shows charging in progress                     |
| 3     | UPS ACTIVE        | After UPS Switch (Battery Output)     | Battery supplying load                 | Blue       | On during blackout                             |
| 4     | WIFI READY        | After filtering and relay closure     | 5V WiFi power present                  | Green      | Indicates WiFi power line is ready             |
| 5     | FULL / STANDBY    | Logic node if UPS = OFF & CHARGE = OFF| Battery is idle, fully charged         | White      | Optional logic with transistor or comparator   |

### Best Practices

- Use 12V pre-resistored LEDs  
- Group LED grounds to a single GND Common rail  
- Optionally mount LEDs on DIN front panel for quick view  
- For LED5 (FULL/STANDBY), logic can be implemented with diode + transistor or logic relay  
- Label each LED clearly on the enclosure or case
