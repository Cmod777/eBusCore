# Cooling Fan System – Assembly and Test Report

## System Overview

The active ventilation module controls the simultaneous activation of all internal cooling fans via the **W1209** temperature controller in **cooling mode**.  
Fans are powered exclusively by a **stabilized 12V system**, fully isolated from the primary 13.8V source.

---

## Logical Circuit Name
`CoolingFanRelay v1.0`

---

## Materials Used
| Component | Description |
|:----------|:------------|
| W1209 Temperature Controller | Thermostat module with NTC sensor and relay output |
| Sunon EE40101S1-0000-999 | 12V DC axial fans (7300 RPM, 5.9 CFM each) |
| MF-R050 Resettable Fuse | Line protection for fan positive supply |
| LM2596 Step-down Converter | 13.8V to 12V stabilized output |
| WAGO Terminal Blocks | Separate terminals for 12V+ and GND wiring |
| Red/Black cables 0.5–0.8mm² | Power distribution and relay control lines |
| Heat-shrink tubing or RTV silicone | Protection on critical connections |

---

## Functional Overview

1. **Power Topology**:
   - **12V+ stabilized** from the LM2596 output is routed to a WAGO block for fan supply.
   - **GND stabilized** from LM2596 output is routed to a WAGO block for all GND connections.

2. **Fan Wiring**:
   - **All fan positives** connect to **WAGO 12V+ ventole**.
   - **All fan negatives** connect to **WAGO GND ventole**.

3. **Relay Control (W1209)**:
   - WAGO 12V+ ventole is connected to the **K1–NO contact** of the W1209.
   - Before reaching K1–NO, the positive line passes through a **MF-R050 resettable fuse** for protection.
   - When the W1209 reaches the trigger temperature, K0–COM connects to K1–NO, supplying 12V to the fans.

4. **W1209 Power Supply**:
   - **K0–COM contact** is connected to a WAGO node that joins:
     - V+ power input of the W1209 itself.
     - OUT+ of the LM2596 step-down converter.
   - Ensures that the switching circuit remains at 12V stabilized.

5. **Isolation Policy**:
   - **No connections** between 13.8V circuits and the 12V stabilized circuits.
   - All 12V+ are exclusively derived from the LM2596 output.

---

## Electrical Block Diagram (ASCII)

```plaintext
[LM2596 Step-Down] 13.8V → 12V
         │
         │
    +----+----+
    │         │
[WAGO GND] [WAGO 12V+]
    │         │
    ▼         ▼
(Out- Fans) (To MF-R050 Fuse)
              │
              ▼
        (K1–NO W1209)
              │
              ▼
           [Fans]
```

- **K0–COM W1209** connects to WAGO node joining:
  - LM2596 OUT+
  - W1209 power V+

---

## Technical Analysis – Sunon Fans

| Parameter | Value |
|:----------|:------|
| Model | EE40101S1-0000-999 |
| Voltage | 12V DC |
| Power consumption | 0.99 W |
| Current draw | ~0.0825 A |
| Speed | 7300 RPM |
| Airflow | 5.9 CFM (~10 m³/h) per fan |

**Total airflow** with 3 fans:  
10 m³/h × 3 = **30 m³/h**

**Internal enclosure volume**:  
~12 liters (0.012 m³)

**Theoretical full air exchange time**:
- 0.012 m³ ÷ 30 m³/h ≈ 0.0004 h = **1.44 seconds**
- Accounting for turbulence and real-world losses: complete renewal every **5–10 seconds**.

---

## Reference Documentation

- **Sunon EE40101S1 Datasheet**:  
  [https://github.com/Cmod777/eBusCore/blob/main/datasheets/internal/ventilation/Sunon_Fans-EE40101S1-0000-999-datasheet.pdf](https://github.com/Cmod777/eBusCore/blob/main/datasheets/internal/ventilation/Sunon_Fans-EE40101S1-0000-999-datasheet.pdf)

- **MF-R050 Resettable Fuse Datasheet**:  
  [https://github.com/Cmod777/eBusCore/blob/main/datasheets/internal/passive/fuses/mf_r-777680.pdf](https://github.com/Cmod777/eBusCore/blob/main/datasheets/internal/passive/fuses/mf_r-777680.pdf)

---

## Best Practices and Recommendations

- Use a dedicated WAGO for GND fans and a separate WAGO for 12V+ fans.
- Always measure LM2596 output voltage before final wiring (should be 11.8–12.0V).
- Keep fan cabling short and firmly attached to avoid mechanical stress.
- Ensure W1209 is set to **cooling mode** (rising temperature triggers fan activation).

---

## Safety Tests Performed

| Test | Result |
|:-----|:-------|
| Relay switching test | Proper relay engagement at setpoint |
| Voltage test | Stable 12V at fan WAGO node |
| MF-R050 trip test | Proper protection under overload simulation |
| Thermal check | No excessive heating under continuous load |
| Full system activation | Fans activate reliably and simultaneously |

---

## Final Considerations

- **Active cooling** greatly improves thermal stability inside the enclosure.
- **Unified control** of all fans reduces complexity and ensures synchronized airflow.
- **Multiple protection layers** (LM2596, MF-R050) ensure maximum reliability.

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
