# Active Cooling System – Assembly and Test Report

## Cooling Strategy Overview

The thermal management system includes:
- **Passive cooling** (previously described using the "chimney effect"):  
  Natural air movement caused by vertical design and vent placement promotes heat dissipation without energy use.
- **Active cooling**, starting with this section:  
  Uses a **W1209 temperature controller** to control fans or extraction systems based on measured internal air temperature.

---

## Logical Circuit Name
`ActiveCoolingControl v1.0`

---

## Materials Used
| Component | Description |
|:----------|:------------|
| LM2596 Step-down Module | Adjustable DC-DC converter 13.8V → 12V |
| W1209 Temperature Controller | Thermostat module with NTC sensor and relay |
| MF-R025 Resettable Fuse | Fuse on step-down input (V+) |
| MF-R020 Resettable Fuse | Fuse on W1209 input (V+) |
| WAGO Terminal Blocks | 13.8V source and wiring distribution |
| Red/Black cables 0.8 mm² | Power cabling |
| NTC Thermistor Probe | Pre-wired, placed at center of enclosure |
| Heat-shrink tubing or RTV silicone | Protection on soldered fuse joints (if applicable) |

---

## Functional Overview

1. **Voltage Regulation**:
   - The system cannot power the W1209 directly at 13.8V.
   - A **step-down converter (LM2596)** reduces voltage to a safe level (ideally 11.8–12.0V).
   - LM2596 supports **input range from 4V to 40V** (per datasheet).

2. **Input Protection**:
   - The **V+ input line** to the LM2596 is protected with an **MF-R025 resettable fuse**.
   - This prevents overcurrent conditions from the MeanWell PSU or other shared loads.

3. **Controller Power Filtering**:
   - The **regulated 12V output** is further filtered with a **MF-R020 resettable fuse** before reaching the W1209.
   - This ensures the W1209 is independently protected in case of internal faults.

4. **Sensor Placement**:
   - The **NTC probe** is pre-connected and positioned at the **center** of the enclosure.
   - It is **elevated**, not in contact with any surface, for accurate **ambient air temperature** measurement.

5. **Relay Output (K0/K1)**:
   - Not handled in this section.
   - Will be documented separately in the next control module.

---

## Wiring Diagram (ASCII)

```plaintext
[13.8V WAGO V+] ----> [MF-R025 Fuse] ----> [LM2596 Step-down]
                                         IN+       IN-
                                          │         │
                                          ▼         ▼
                                     [Regulated 12V Output]
                                          │
                                   [MF-R020 Fuse]
                                          │
                                          ▼
                                      [W1209]
                                       │   │
                                     K0   K1 (handled later)

                      [NTC Sensor Probe]
                               │
                        (elevated in air)
```

---

## Cable Sizing and Justification

- **Recommended cable section**: **0.8 mm²**  
  (equivalent to ~18 AWG)

**Justification**:
For short runs (<1 m), using Ohm's Law:

- Assume W1209 load = 0.3 A max  
- Voltage drop (ΔV) = I × R × 2L  
- For 0.8 mm², R ≈ 0.025 Ω/m →  
  ΔV ≈ 0.3 × 0.025 × 2 × 1 = **0.015V**, negligible

Therefore, 0.8 mm² ensures:
- Minimal voltage loss
- Mechanical robustness
- Adequate thermal tolerance

---

## Reference Documentation

- **W1209 Datasheet**:  
  [https://github.com/Cmod777/eBusCore/blob/main/datasheets/internal/active/W1209_guide-1.pdf](https://github.com/Cmod777/eBusCore/blob/main/datasheets/internal/active/W1209_guide-1.pdf)

- **MF-R025 and MF-R020 Datasheet**:  
  [https://github.com/Cmod777/eBusCore/blob/main/datasheets/internal/passive/fuses/mf_r-777680.pdf](https://github.com/Cmod777/eBusCore/blob/main/datasheets/internal/passive/fuses/mf_r-777680.pdf)

---

## Best Practices

- Measure output voltage with a tester **before** connecting to W1209.
- If using **inline soldered fuses**, protect with **heat-shrink tubing or RTV silicone**.
- Ensure **sensor is suspended**, not touching walls or hot components.
- Mount W1209 relay side in a way that keeps high-voltage contacts isolated.
- Future output control (fan, extraction) should consider inrush current if inductive loads are used.

---

## Tests Performed

| Test | Result |
|:-----|:-------|
| Step-down regulation | Stable output 11.8V–12.0V |
| Fuse trip test | MF-R025 and MF-R020 functioned correctly |
| NTC sensor reading | Consistent and accurate ambient values |
| Thermal check | No overheating under load |
| W1209 function | Activated relay at set threshold (cooling mode) |

---

## Final Considerations

- The system is now ready for **intelligent cooling automation**.
- Provides **double-layer protection**: one for step-down, one for controller.
- Designed for **safe, remote-controllable thermal management** of enclosed electronics.

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
