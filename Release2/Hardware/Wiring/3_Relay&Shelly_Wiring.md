# Section 2 - Relay and Shelly Wiring (Base Configuration)

## Description

In this phase, the 12V DC output from the Mean Well power supply is distributed to the main WAGO terminal blocks, organizing the V+ (positive) and V- (negative) lines separately.  
The goal is to supply power to a Shelly Plus 1 device and a Finder relay while maintaining a clean, safe, and scalable structure.

The Shelly Plus 1 acts as a remote-controlled switch that manages the Finder relay coil, allowing future integrations with smart automation scripts.  
No additional protections (such as fuses or TVS diodes) are installed in this phase; they will be considered in the next project step.

Special attention has been given to wire sizes and connections:
- Mean Well output terminals are extremely small, thus 0.8 mm² cables are used and manually stripped (without crimp terminals).
- Proper cable management and safe current handling have been respected throughout the layout.

All systems must be able to tolerate a Mean Well output voltage of 13.8V nominal.

---
# Relay Protection Module – Assembly and Test Report

| Field | Details |
|:------|:--------|
| **Circuit Name** | RelayCoilProtection v1.0 |
| **Function** | Relay coil spike suppression and voltage stabilization |
| **Version** | 1.0 |
| **Completion Date** | 2025-04-28 |
| **Responsible** | [GitHub nickname] |

---

# Relay Protection Module – Assembly and Test Report

## Module Description
Protection circuit for relay coil consisting of:
- **Flyback diode** (1N4007) for spike suppression.
- **Ceramic capacitor** 0.1µF 50V for high-frequency noise filtering.
- **Polymer capacitor** 220µF 25V for voltage stabilization and slow spike absorption.
- **Mounted on standard perforated PCB**.
- **Mechanical protection** with RTV silicone.

> **Logical circuit name:** `RelayCoilProtection v1.0`

---

## Materials Used
| Component | Description |
|:----------|:------------|
| 1N4007 | Flyback protection diode |
| Ceramic capacitor | 0.1µF 50V (X7R) |
| Polymer capacitor | 220µF 25V |
| Perforated PCB | Standard millefori board |
| RTV silicone | Post-soldering elastic protection |
| Red/Black wires | Positive/negative identification |

---

## Assembly Procedure

### 1. Component Preparation
- Individual verification of capacitors.
- Polarity check for diode and polymer capacitor.

### 2. PCB Soldering
- Soldered on both sides of the PCB as needed.
- Adequate amount of solder applied to ensure electrical continuity.
- RTV silicone applied to fragile components.

### 3. Main Connections
- **Red wire** connected to positive (V+).
- **Black wire** connected to negative (GND).
- Polarity respected in all connections.

### 4. Installation in Final Circuit
- Module installed inside the final structure.
- Direct connection to relay coil terminals.

---

## Tests Performed

| Test | Result |
|:-----|:-------|
| Short-circuit check | No short between V+ and GND |
| Capacitor test | Proper charging (resistance increasing) |
| Relay operation test | Relay activates normally without disturbances |
| Full system test | No abnormal noise or behavior |

---

## Final Considerations
- **Functionality confirmed.**
- **Expected high reliability** due to passive filtering.
- **Aesthetic appearance secondary to functionality** (perforated board not optimal for aesthetics).
- **No modifications necessary** to the built circuit.

---

## Timestamp
**Completion date:** 2025-04-28  
**Approximate time:** 21:xx local time  
**Responsible:** [Insert name or GitHub nickname]

---

## Notes
- Always refer to the official datasheets of individual components before assembly or replacement.
- Circuit name for internal documentation and future upgrades: `RelayCoilProtection v1.0`.

---

## Wiring Diagram (ASCII)

```plaintext
                   ┌───────────────────────┐
                   │  Mean Well 12V Output  │
                   └─────────┬──────────────┘
                             │
          ┌──────────────────┴──────────────────┐
          │                                      │
      ┌───▼───┐                              ┌───▼───┐
      │  WAGO │ (V+)                         │  WAGO │ (V-)
      └───┬───┘                              └───┬───┘
          │                                      │
    ┌─────▼─────┐                          ┌─────▼─────┐
    │ Shelly    │                          │ Shelly    │
    │ Plus 1    │                          │ Plus 1    │
    │ 12V+ (I)  │                          │ GND (N)   │
    └─────┬─────┘                          └─────┬─────┘
          │                                      │
          │                                      │
    ┌─────▼──────┐                        ┌──────▼───────┐
    │  Shelly    │                        │   Finder     │
    │ Output [O] │───[Controlled Line]────▶│   COM2 Coil  │
    └─────┬──────┘                        └──────┬───────┘
          │                                       │
    ┌─────▼─────┐                           ┌─────▼─────┐
    │ V+ (WAGO) │                           │ V- (WAGO) │
    │  Common   │                           │  Common   │
    └───────────┘                           └───────────┘

---

## Notes

- **Cable Sizes**:
  - 0.8 mm² silicone-insulated cables are used for all connections (red for V+, black for V-).
  - Cables are manually stripped to fit Mean Well small terminals, avoiding crimping.

- **Power Distribution**:
  - V+ and V- from the Mean Well are connected directly to separate WAGO common terminals.
  - Positive and negative wires are kept clearly separated.

- **Shelly Plus 1 Wiring**:
  - Shelly Plus 1 is powered directly from the WAGO common terminals.
  - The device supports the nominal 13.8V output voltage from the Mean Well power supply.

- **Finder Relay Wiring**:
  - The relay coil is powered through the Shelly Plus 1 output channel.
  - The positive side (V+) is switched by Shelly; the negative side (V-) comes directly from the WAGO terminal.

- **Functional Overview**:
  - The Shelly Plus 1 acts as a smart switch, allowing remote and programmable control of the Finder relay.
  - Future integrations with scripts and smart automation are possible.

- **Protections**:
  - No additional protections (fuses, TVS diodes) are installed at this stage.
  - Protections will be discussed and added in later phases.

---

## Licensing Notice

All original photographs, electrical schematics, and technical drawings created by the author are licensed under:

**Creative Commons Attribution - NonCommercial - NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**

Under this license:
- Copying, sharing, and redistribution of the material are allowed, provided that proper attribution is given to the original author (Cmod777).
- Commercial use is strictly prohibited.
- No modifications, transformations, or derivative works are allowed.

For full license details, refer to: [https://creativecommons.org/licenses/by-nc-nd/4.0/](https://creativecommons.org/licenses/by-nc-nd/4.0/)
