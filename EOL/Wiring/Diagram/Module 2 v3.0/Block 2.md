## Block 2 – Battery Charging and UPS Switching Logic

This block handles the charging of the 12V battery from the stabilized line, and routes battery power to the UPS system when the grid is lost.  
It includes: charging path with protection, switchable battery cutoff, and automatic activation of the UPS relay and StepDown module.

### Wiring Diagram

```
[Meanwell V+ 12V Stabilized]
         |
         +---[ PTC Fuse ]---+---[ 1N5819 Diode ]---+
                            |                      |
                      [WAGO 3x]               [WAGO 3x]
                            |                      |
                            |                      +--> [Battery +]
                            |                            [Battery -] --> [GND Common]
                            |
                            +--> [DIODE 1N5819] --> [Switch IN+]
                                                      [Switch OUT+] --> [UPS LOAD INPUTS]

[UPS LOAD INPUTS] → [Relay V+]
                 → [StepDown IN+]

[Relay V−], [StepDown IN−] → [GND Common]
```

### Terminal Connections

| Element        | Type          | Wire Color | Notes                                              |
|----------------|---------------|------------|----------------------------------------------------|
| PTC Fuse       | 12V Line Fuse | Red        | Resettable fuse in series for charge protection    |
| 1N5819 Diode   | Schottky      | Red        | Blocks reverse current from battery                |
| Battery Switch | Manual        | Red        | Used to disconnect battery during maintenance      |
| Relay V+       | UPS Trigger   | Red        | Activated only when battery provides power         |
| StepDown IN+   | UPS Load      | Red        | Receives 12V from battery when grid fails          |
| V− (All)       | GND Common    | Black      | Shared negative rail for all logic and load        |

### Behavior Matrix

| Grid Power | Battery Charging | Battery Output Active | Notes                          |
|------------|------------------|------------------------|--------------------------------|
| ON         | Yes              | No                     | Battery charges via diode+PTC  |
| OFF        | No               | Yes                    | Relay and StepDown powered     |
| Switch OFF | No               | No                     | Battery completely isolated    |

### Best Practices

- Use low forward-drop Schottky diode (e.g. 1N5819)  
- Ensure PTC fuse is correctly dimensioned for charge current  
- Use manual battery switch for safety during installation or testing  
- Clearly label the battery cutoff switch  
- Keep battery wiring short and protected
