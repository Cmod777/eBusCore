## Block 6 – Logical Overview / Behavior Summary

This block summarizes the global logic of the UPS system.  
It defines how the system reacts to power availability, manages battery charging, and ensures safe switching to backup power when needed.

### State Diagram Summary

```
[GRID ON] ───────────────┐
                        │
                        ▼
          +-----------------------------+
          | Meanwell ON (12V Stabilized)|
          +-----------------------------+
                        │
        +---------------+------------------------------+
        |                                              |
        ▼                                              ▼
[Battery Charges]                             [Relay NOT Powered]
        |                                              |
        ▼                                              ▼
[UPS Path Isolated]                             [StepDown OFF]
                                                      |
                                                      ▼
                                            [WiFi Module OFF]

[GRID OFF] ───────────────┐
                         ▼
                [Meanwell OFF]
                         |
                         ▼
          [Battery Powers Relay + StepDown]
                         |
                         ▼
                 [Relay Activated]
                         |
                         ▼
           [5V Power Routed to WiFi Module]
                         |
                         ▼
                [WiFi Module ON (via Battery)]

[Manual Switch OFF] → [Battery Fully Disconnected (Maintenance Mode)]
```

### Operational Scenarios

| Condition                     | Battery Charging | UPS Active | WiFi Active | Notes                               |
|------------------------------|------------------|------------|-------------|-------------------------------------|
| Grid Present, Battery OK     | Yes              | No         | No          | Normal charging only                |
| Grid Present, Switch OFF     | No               | No         | No          | Maintenance mode                    |
| Grid Absent, Switch ON       | No               | Yes        | Yes         | UPS fully operating                 |
| Grid Absent, Switch OFF      | No               | No         | No          | Battery disconnected                |
| Grid Present, Battery Full   | No               | No         | No          | Idle mode                           |

### Reliability Notes

- Relay is powered only by battery to guarantee UPS activation during blackout  
- No backfeed between battery and Meanwell thanks to diodes  
- Manual switch ensures safe disconnection for service or replacement  
- Filtering stage improves voltage stability and protects WiFi module  
- Status LEDs offer real-time feedback on each phase of the system
