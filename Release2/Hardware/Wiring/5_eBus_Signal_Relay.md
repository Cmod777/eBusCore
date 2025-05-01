# eBus Signal Relay – Assembly and Test Report

## Module Description
This module integrates the **physical disconnection** of the **eBus+** and **eBus−** signal lines from the WiFi eBus module using the **Finder Relay**.  
It ensures **complete bus isolation** during system shutdowns or resets, preventing any unwanted back-powering through the communication bus.

---

## Logical Circuit Name
`eBusSignalRelay v1.0`

---

## Materials Used
| Component | Description |
|:----------|:------------|
| Finder Relay 12V DC | Relay handling full disconnection of eBus+ and eBus− lines |
| Shelly Plus 1 | Automation control for relay activation |
| WAGO 1:1 Connectors | Quick connection points for maintenance |
| 4-pin Nylon Aviation Connector | Interface for external eBus+ and eBus− wiring |
| Red/Black cables 0.8mm² | Signal cabling from eBus WiFi module |
| Cable clamps | Mechanical cable fixation inside enclosure |
| Heat-shrink tubing | Optional for extra mechanical protection on signal paths |

---

## Functional Overview

- **Signal Flow**:
  - **eBus+ (red cable)**:
    - eBus WiFi output → COM3 (Relay) → NO3 → WAGO 1:1 → Pin 4 of Aviation Connector.
  - **eBus− (black cable)**:
    - eBus WiFi output → COM4 (Relay) → NO4 → WAGO 1:1 → Pin 3 of Aviation Connector.

- **Relay Behavior**:
  - When Shelly Plus 1 activates the relay:
    - eBus+ and eBus− are connected to the external system.
  - When the relay is deactivated:
    - Full disconnection of both eBus signals.
    - Prevents undesired back-powering through the bus lines.

- **Maintenance Segmentation**:
  - Modular disconnection is possible at three levels:
    1. Quick-release connector (aviation connector).
    2. WAGO 1:1 link after quick-release.
    3. Internal wiring from eBus WiFi to the relay contacts.

- **Protection Policy**:
  - **No fuses or protective devices** on signal lines.
  - Avoids risks of line interference or signal degradation.

---

## Assembly Procedure

### 1. Cable Preparation
- Use **0.8mm²** cables (or minimum **0.5mm²** if necessary).
- Crimp terminals or tin solder the ends if required.

### 2. Mechanical Anchoring
- Use cable clamps to fix all signal cables inside the enclosure.
- Ensure no excessive mechanical stress is applied to relay or connectors.

### 3. Wiring
- Route eBus+ and eBus− through COM/NO relay contacts as specified.
- Install WAGO 1:1 terminals for serviceability.
- Connect final outputs to the 4-pin aviation connector (Pin 3 for eBus−, Pin 4 for eBus+).

### 4. Final Checks
- Verify correct labeling and isolation.
- Avoid any proximity or parallel routing with 230V lines.

---

## Functional Block Diagram

```plaintext
[eBus WiFi Module]
   │        │
   ▼        ▼
(COM3)    (COM4)
  │          │
(NO3)      (NO4)
  │          │
[WAGO]    [WAGO]
  │          │
Pin 4     Pin 3
(Aviation Connector)
```

---

## Best Practices and Recommendations

- Keep signal wires **separated** from 230V power lines as much as possible.
- If unavoidable, **cross cables at 90° angles** and ensure all insulation jackets are **perfectly intact**.
- Use **heat-shrink tubing** where soldered joints exist, or preferably use **WAGO** for modular maintenance points.
- Always prioritize **mechanical fixation** to avoid stress on relay or connectors over time.

---

## Safety Tests Performed

| Test | Result |
|:-----|:-------|
| Relay switching test | Proper toggling with no sticking |
| Isolation test | Full disconnection of eBus lines when relay OFF |
| Signal continuity test | Stable transmission with relay ON |
| Mechanical integrity test | No tension on terminals or relay under cable load |

---

## Final Considerations
- **System fully validated** for safe remote control of eBus communication lines.
- **Improved modularity** for service operations.
- **Essential safety feature** to guarantee true hardware shutdown of the WiFi eBus system.

---

## Licensing Notice

All original photographs, electrical schematics, and technical drawings created by the author are licensed under:

**Creative Commons Attribution - NonCommercial - NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**

Under this license:
- Copying, sharing, and redistribution of the material are allowed, provided that proper attribution is given to the original author (Cmod777).
- Commercial use is strictly prohibited.
- No modifications, transformations, or derivative works are allowed.

For full license details, refer to: [https://creativecommons.org/licenses/by-nc-nd/4.0/](https://creativecommons.org/licenses/by-nc-nd/4.0/)

---
