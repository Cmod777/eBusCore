# eBus WiFi Power Relay – Assembly and Test Report

## Module Description
This module integrates the **power supply control** for the eBus WiFi module using a Finder relay.  
It ensures a **safe shutdown and reboot** by physically interrupting both the **power supply** and, in the next stage, the **eBus signal** (to prevent unwanted back-powering scenarios).  
The system is **automatable** via Shelly Plus 1, allowing **remote reset** and **controlled reboot** procedures.

---

## Logical Circuit Name
`eBusPowerRelay v1.0`

---

## Materials Used
| Component | Description |
|:----------|:------------|
| Finder Relay 12V DC | Relay for controlled switching of power lines |
| Shelly Plus 1 | Automation control for relay switching |
| Bauer DC-DC Converter 13.8V → 5V USB-C | Power supply for eBus WiFi module |
| MF-R050 Resettable Fuse | 5A resettable PTC fuse for Bauer input protection |
| WAGO Terminal Block | 13.8V common distribution |
| Red/Black cables 0.8mm² | Power wiring to Bauer |
| Heat-shrink tubing or RTV silicone | Solder protection (for fuse installation) |

---

## Functional Overview

- **Power Supply Flow**:
  - 13.8V and GND are taken from the **common WAGO terminal block**.
  - Routed through **COM1/NO1** and **COM2/NO2** contacts of the **Finder Relay**.
  - The **positive line** is protected by a **resettable MF-R050 fuse** before reaching the Bauer converter.

- **Fuse Installation Options**:
  - **Option 1**: Quick connection using **WAGO terminal blocks** on both sides of the MF-R050 fuse.
  - **Option 2**: **Direct soldering** of the fuse inline, with mandatory protection using **heat-shrink tubing** or **RTV silicone** to mechanically and electrically secure the joints.

- **Bauer Converter**:
  - Receives protected 13.8V input and provides a clean 5V USB-C output to power the eBus WiFi module.

- **Protection Strategy**:
  - General upstream protection is already guaranteed (main fuse, MeanWell UPS, etc.).
  - Local additional protection on the Bauer input line using MF-R050.

- **Objective**:
  - Enable **safe remote resets** and **controlled reboots** of the eBus WiFi module.
  - Physically isolate both **power** and **bus signal** in emergency or maintenance scenarios.

---

## Assembly Procedure

### 1. Component Preparation
- Verify relay wiring and Shelly Plus 1 setup.
- Pre-test the MF-R050 fuse (low resistance check).
- Prepare cable sections (0.8 mm²) and insulation materials.

### 2. Power Routing
- Connect 13.8V V+ and GND from WAGO to the relay's COM1 and COM2 terminals.
- Wire the NO1 and NO2 outputs toward the Bauer converter.

### 3. Fuse Installation
- Insert the MF-R050 on the positive line, choosing between:
  - WAGO quick connection.
  - Direct soldering with heat-shrink tubing or RTV silicone encapsulation.

### 4. Final Wiring
- Connect Bauer 5V USB-C output directly to the eBus WiFi module.
- Check all mechanical fixations and wire routing.

---

## Tests Performed

| Test | Result |
|:-----|:-------|
| Relay switching | Proper toggling, no mechanical faults |
| Power supply test | Stable 13.8V routed to Bauer input |
| MF-R050 fuse behavior | Correct protection and automatic reset |
| 5V output stability | Stable 5V USB-C to eBus WiFi module |
| System isolation test | Total power cut verified on Shelly deactivation |

---

## Final Considerations
- **System functionality confirmed** with full remote reset capability.
- **Increased reliability** thanks to localized fuse protection.
- **Flexibility in fuse installation** depending on field constraints.

---

## Reference Documentation

- **MF-R050 Fuse Datasheet**:  
  [https://github.com/Cmod777/eBusCore/blob/main/datasheets/internal/passive/fuses/mf_r-777680.pdf](https://github.com/Cmod777/eBusCore/blob/main/datasheets/internal/passive/fuses/mf_r-777680.pdf)

---

## Functional Block Diagram

```plaintext
[13.8V Common WAGO] 
         │
         ▼
   [Finder Relay]
 (COM1/NO1 & COM2/NO2)
         │
         ▼
 [MF-R050 Resettable Fuse]
 (Quick-connect via WAGO or protected soldering)
         │
         ▼
  [Bauer DC-DC Converter]
 (13.8V → 5V USB-C)
         │
         ▼
 [eBus WiFi Module]
```

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
