# Emergency Cooling Circuit – Revision and Logic Update

## Logical Name: `EmergencyCoolingSystem v2.0`  
*(now functionally integrated into the CerberusVent© module)*

---

## Overview

This document outlines the functionality and progressive revision of the **Emergency Cooling Circuit**, designed to guarantee forced ventilation in the event of failure of the primary thermostat module (**W1209**).

During initial prototyping, the system was implemented with a logic that allowed the **Shelly Plus Add-On** to directly override the W1209 relay via the **K1–K0 terminals**. However, after multiple field tests and logic evaluations, several design limitations emerged. These included potential contention on relay contacts, voltage drop inconsistencies, and insufficient isolation between control paths.

As a result, the circuit identified as `EmergencyCoolingShelly` has been **fully updated** to operate through an **independent activation path**, bypassing the W1209 logic entirely. It now delivers voltage to the fan line autonomously, based on sensor data and scripted conditions.

While it now operates as one of the internal branches of the **CerberusVent©** redundant control system, this circuit retains its original logical name for version tracking and functional documentation purposes.

---

## Multi-Path Redundancy: Rationale and Structure

The updated emergency ventilation system is designed around a **three-path architecture**, each with distinct activation logic and power sources. This modular setup ensures operational continuity even in the event of partial or total system failure.

- **Circuit 1** (Standard Ventilation – W1209)  
  Handles basic cooling operations under normal conditions. Controlled via relay K1–K0 of the **W1209** and powered by a dedicated LM2596 step-down. It uses a single integrated thermal probe and is **not part of the emergency system**.

- **Circuit 2** (Logical Emergency – Shelly Add-On + LM2596)  
  Bypasses both the **W1209** and its onboard sensor. It draws power from the same LM2596 that feeds the W1209. This circuit is triggered by independent logic and thermal data from two DS18B20 probes connected directly to the Shelly Plus Add-On.

- **Circuit 3** (Full Emergency – Shelly Add-On + UPS)  
  Acts as a complete fallback solution, bypassing both the **W1209** and its power supply. It is powered directly from the 13.8V UPS line and is engaged only if both the thermostat module and its step-down regulator fail.

This design addresses multiple potential points of failure:
- A faulty W1209 relay (Circuit 1 failure)
- A damaged W1209 sensor or logic crash (Circuit 2 engagement)
- A dead LM2596 or complete controller loss (Circuit 3 engagement)

Unlike the W1209, which is limited to a single onboard sensor, the Shelly Plus Add-On utilizes **two independent DS18B20 probes**, positioned in different thermal zones within the enclosure (e.g. top for heat accumulation, bottom for intake). This ensures broader thermal coverage and supports more advanced logic conditions, such as delta temperature thresholds and asymmetrical activation.

> **Note:** `EmergencyCoolingShelly v1.0` is now structurally embedded within the `CerberusVent©` logic block. Any future revisions of the emergency control path will retain compatibility with this naming convention for traceability purposes.

---

## Circuit 2 – Logic and Implementation

### Power Path and Hardware Structure

- **Source Voltage**: 12V regulated output from the LM2596 step-down converter (same source used by the W1209).
- **Activation**: Managed by Shelly Plus 1 using the Add-On module.
- **Wiring Flow**:
    - LM2596 → 1N5822 (D1) → Shelly Add-On (O → I)
    - Shelly I → 1N5822 (D2) → Ventilation Line
- **Total Diodes**: 2 (1 on input, 1 on output)
- **Estimated Voltage Drop**: ~0.7V total (0.35V per diode)
- **Effective Voltage at Fans**: ~11.3V
- **RPM Performance Loss**: Approx. 5.8%

This circuit is fully independent from the W1209 logic and relay. It provides a redundant activation path powered by the same regulator, allowing fallback control in case the W1209 logic or sensor fails.

---

### Trigger Logic and Sensor Data

- **Temperature Monitoring**:  
  Two **DS18B20 digital sensors** connected directly to the Shelly Add-On.  
  - **Probe A**: upper section of the enclosure (heat accumulation zone)  
  - **Probe B**: lower section near intake (cool air zone)

- **Activation Conditions**:
  - Defined via Home Assistant automation or native Shelly scripting.
  - Examples:
    - Delta T condition (e.g. upper > lower by X°C)
    - Threshold-based (e.g. upper > 42°C)
    - Time-based or fallback override

- **Logic Isolation**:  
  Even though the LM2596 is shared with the W1209, the control and sensor logic is fully isolated. This ensures that if the W1209 freezes, misreads or becomes unresponsive, the Shelly can still independently activate the fans.

---

### Operational Purpose

Circuit 2 is intended as the **first level of emergency response**. It comes into play when:
- The W1209 fails to activate its relay
- The W1209's sensor malfunctions or detaches
- The W1209 logic enters a fault or frozen state

It is **not** reliant on the W1209's logic or output state, and thus provides a critical redundancy layer without overlapping control paths.
---

## Circuit 3 – Full Emergency via UPS

### Power Path and Hardware Structure

- **Source Voltage**: 13.8V regulated UPS output (independent from LM2596 and W1209).
- **Activation**: Managed by Shelly Plus 1 using the Add-On module.
- **Wiring Flow**:
    - UPS 13.8V → 1N5822 (D1) → 1N5822 (D2) → Shelly Add-On (O → I)
    - Shelly I → 1N5822 (D3) → 1N5822 (D4) → Ventilation Line
- **Total Diodes**: 4 (2 on input, 2 on output)
- **Estimated Voltage Drop**: ~1.4V total (0.35V × 4)
- **Effective Voltage at Fans**: ~12.4V
- **RPM Performance Loss**: 0% (fans operate at nominal speed)

This circuit is fully decoupled from both the W1209 and its step-down converter, acting as an isolated, high-availability power path. It ensures proper fan operation even in case of complete controller or power failure upstream.

---

### Trigger Logic and Fault Condition

- **Primary Trigger**:
  - Activated only if both Circuit 1 (W1209) and Circuit 2 (LM2596 + Shelly) are non-functional or absent.
  - Designed for critical fallback when no regulated 12V source is available.

- **Recommended Implementation**:
  - Home Assistant or internal Shelly logic should monitor:
    - Power presence on LM2596 (via voltage sensor or relay feedback)
    - W1209 activity status (optional digital input or derived state)
    - UPS availability (should be always ON)

- **Priority Handling**:
  - Circuit 3 must remain inactive during normal operations.
  - It must engage automatically and silently in failure scenarios without requiring external validation.

---

### Operational Purpose

Circuit 3 represents the **last line of defense** in the emergency cooling hierarchy. It guarantees continued airflow in case of:
- LM2596 failure or detachment
- W1209 total shutdown
- Disconnection of the low-voltage control system

The UPS line (13.8V) not only compensates for voltage drop due to multiple Schottky diodes, but also guarantees maximum fan performance under stress or power fluctuation. This makes Circuit 3 the most resilient and performant path in the system, despite being used only in critical scenarios.

---
## Comparative Summary – Redundant Cooling Paths

| Circuit | Activation Logic             | Power Source         | Diodes | Output Voltage | RPM Impact | Emergency Tier |
|:--------|:-----------------------------|:---------------------|:-------|:----------------|:------------|:----------------|
| 1       | W1209 internal relay (K1–K0) | LM2596 (12V)         | 1–2    | ~11.1–11.65 V   | ~3–8%       | Not Emergency   |
| 2       | Shelly Add-On (logic-based)  | LM2596 (12V)         | 2–3    | ~10.65–11.3 V   | ~6–15%      | Level 1         |
| 3       | Shelly Add-On (failover)     | UPS 13.8V (direct)   | 4      | ~12.4 V         | ~0%         | Level 2 (Critical) |

---

## Final Notes and System Philosophy

The cooling architecture designed around **CerberusVent©** ensures that airflow is preserved under all foreseeable failure conditions. Each circuit has been engineered with:

- **Electrical isolation**, to prevent feedback and inter-path interference.
- **Voltage tolerance**, using Schottky diodes to optimize drop control.
- **Logical independence**, where control paths are not reliant on the same sensors or microcontrollers.

While Circuit 1 provides baseline ventilation, only Circuits 2 and 3 contribute to the **resilient emergency framework**. Circuit 3 stands out as the most reliable and performant path thanks to its UPS-powered autonomy and stable voltage.

This tiered logic allows future modules to evolve or expand (e.g. Raspberry Pi-controlled fans, variable speed logic, environmental adaptation) without compromising the current safety net.

> **All redundant paths are automatically engaged as needed, without manual switching, relying entirely on logic-based triggers and failover heuristics.**

System status can be monitored and logged via Home Assistant or MQTT integrations for long-term diagnostics and alerts.
---

<details>
<summary><strong>Deprecated: Legacy Version – EmergencyCoolingShelly v1.0</strong></summary>

```md
# Emergency Cooling System – Assembly and Test Report

## System Overview
This module provides an **intelligent emergency override** for the active cooling system, using a **Shelly Plus Add-On** to bypass the W1209 in case of malfunction or crash.
The system monitors temperature independently and ensures fan activation even when the primary controller fails.

---

## Logical Circuit Name
`EmergencyCoolingShelly v1.0`

---

## Materials Used

| Component               | Description                                        |
|:------------------------|:---------------------------------------------------|
| Shelly Plus 1 + Add-On | Smart controller with digital I/O and 1-wire probe support |
| Sunon Fans EE40101S1   | 12V, 7300 RPM, 0.99W axial fans                   |
| Diodo Schottky 1N5819  | Output protection to K1-NO (W1209)                |
| Cavi rosso/nero 0.8 mm²| Power and control lines                          |
| WAGO blocks            | Power distribution for 12V+, GND, and logic branches |
| Sonde DS18B20          | High/Low zone thermal probes for Add-On           |
| Heat-shrink/RTV silicone | Protection for soldered diodes and critical joints |

---

## Functional Overview

1. **Dual temperature monitoring**:
   - Two DS18B20 probes on the Shelly Add-On:
     - **High zone**: top of enclosure (heat accumulation).
     - **Low zone**: bottom (cool air intake).
   - Allows differential logic and redundancy.

2. **Input logic (pin I)**:
   - Connected to a **shared 12V+ node** supplied by both:
     - **OUT+ of LM2596 step-down**.
     - **V+ of W1209**.
   - If one module fails, the other maintains the signal.
   - Already protected by upstream fuses – **no extra diode needed**.

3. **Output logic (pin O)**:
   - Connected to **K1–NO terminal of W1209** via a **Schottky diode 1N5819**.
   - Prevents reverse current into W1209 in case of damage.
   - When triggered, Shelly closes this path, forcing 12V onto the fan line.

4. **Failure override logic**:
   - If W1209 relay fails (no contact K0–K1), Shelly Add-On acts as backup.
   - Based on sensor readings or scripted logic (e.g. delta T, timer, fixed thresholds).

5. **Complete redundancy**:
   - Shared power and GND for all 12V logic (isolated from 13.8V).
   - Smart decision-making via Home Assistant, script, or standalone config.

---

```md
## ASCII Diagram

```plaintext
┌────────────┐
│  W1209     │
│  K0  K1    │
│            │
│            │
12V+ ◄─────┘ │
      │────┐  │
      ▼    │  │
[VENTOLA +12V]◄────┐
                   ▲
                   │
              Shelly O
                 [D]
                   │
                   │
         └────┴─────────┘
               Shared GND
[D] = Diodo Schottky 1N5819
```

---

## Emergency Logic Notes

- **Input pin I** is safely shared from W1209 and LM2596. Failure of one does **not** stop Shelly Add-On from functioning.
- **Output pin O** does **not control W1209**, but **injects 12V** into the vent line when W1209 fails to trigger it.
- W1209 mechanical failure = Shelly takes over fan activation.

---

## Safety Layers

| Component         | Protection                                              |
|:------------------|:--------------------------------------------------------|
| MF-R020, MF-R050  | Fuse per module (already in upstream branches)         |
| 1N5819 diode      | Reverse current blocking (Shelly → W1209 relay)        |
| Scripted failover | Add-On can trigger based on time, delta-T, or conditions |

---

## Best Practices

- Use **dedicated WAGO blocks** to distribute 12V+ and GND to Add-On, LM2596, and W1209.
- Mount thermal probes firmly but **without metal contact**; use heat-shrink tubing or foam for stable ambient readings.
- Test the Shelly logic separately (simulate W1209 failure by disconnecting K0–K1).
- Document your logic in Home Assistant or Shelly Web UI for traceability.

---

## Tests Performed

| Test               | Result                                  |
|:-------------------|:------------------------------------------|
| Sensor accuracy    | DS18B20 working, delta-T tracked         |
| 12V continuity     | Maintained if either source is active    |
| Reverse protection | Diode blocks backflow to W1209           |
| Emergency trigger  | Fans activate when W1209 fails           |
| Logic stability    | No false triggers, script logs OK        |

---

## Final Considerations

- This system ensures **critical thermal protection** even under partial system failure.
- Provides **advanced automation** beyond the capabilities of basic thermostats.
- Can be expanded with additional actions: alarms, MQTT, energy logging.

---

## Licensing Notice

All original photographs, electrical schematics, and technical drawings created by the author are licensed under:
**Creative Commons Attribution - NonCommercial - NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**

Under this license:
- Copying, sharing, and redistribution of the material are allowed, provided that proper attribution is given to the original author (Cmod777).
- Commercial use is strictly prohibited.
- No modifications, transformations, or derivative works are allowed.

For full license details, refer to:
[https://creativecommons.org/licenses/by-nc-nd/4.0/](https://creativecommons.org/licenses/by-nc-nd/4.0/)
```
---

## EmergencyCoolingDualCircuit v1.0

### System Overview
This improved emergency cooling system introduces **full dual-path redundancy** using a **Shelly Plus Add-On**.
The Shelly can now:
- Force the W1209 relay contact (K0–K1) to close.
- **AND** directly provide stabilized 12V+ to the fan power line.

This ensures that even in the event of a **complete W1209 failure** (including mechanical relay damage), **the fans will still operate correctly**.

---

### Logical Circuit Name
`EmergencyCoolingDualCircuit v1.0`

---

### Materials Used

| Component               | Description                                        |
|:------------------------|:---------------------------------------------------|
| Shelly Plus 1 + Add-On | Smart controller for logic and backup actions      |
| 2× Schottky Diode 1N5819 | Output protection for relay and direct path      |
| Sunon EE40101S1 Fans   | 12V axial fans (7300 RPM, 0.99W each)              |
| LM2596 Step-down       | 13.8V to 12V stabilized converter                  |
| Cables 0.8 mm²         | Robust power and control lines                     |
| WAGO Terminal Blocks   | Organized distribution for 12V+ and GND            |
| Heat-shrink / RTV      | Protection for soldered diodes and joints          |

---

### Functional Overview

#### Dual Redundant Action:
- **First Path (Relay Assist)**:
  - Shelly closes the W1209 K0–K1 relay contact via a **Schottky diode**.
- **Second Path (Direct Feed)**:
  - Shelly also provides **direct 12V stabilized power** to the fan line through another **Schottky diode**.

**Both circuits are always ready.**  
If the W1209 is partially functional, the Shelly helps trigger it.  
If the W1209 is completely broken, the Shelly powers the fans directly.

---

### Electrical Block Diagram (ASCII)

```plaintext
┌───────────────┐
│  LM2596 12V   │
└──────┬────────┘
       │
       ▼
(Shared 12V+ Bus)
       │
┌─────────┴─────────┐
│                   │
[DIODE 1]       [DIODE 2]
Relay Assist     Direct Feed
  │                   │
  ▼                   ▼
K0 W1209        WAGO V+ Fans
  │                   │
  ▼                   ▼
K1-NO W1209     Fan Positives

---

### Logic Description

- **DIODE 1** (Assist Relay):  
  Output from Shelly `O` to K0 W1209, protected against feedback.
  
- **DIODE 2** (Direct Power):  
  Output from Shelly `O` to WAGO 12V+ ventole, also protected.

- **Fans will always activate** if either:  
  - The W1209 closes its relay (normal operation).  
  - Shelly forces activation (backup action).

- **Protection is guaranteed** by two Schottky diodes:  
  - Prevents interference between paths.  
  - Ensures clean isolation even in the case of partial damage.

---

### Cabling Instructions

- **Shelly Add-On O output** splits into two lines:  
  - One to K0 W1209 (with DIODE 1).  
  - One to WAGO 12V+ Ventole (with DIODE 2).  
- Use robust **0.8 mm² cables** for both branches.  
- Protect diode solder joints with **heat-shrink tubing or RTV silicone**.

---

### Practical Benefits

| Feature         | Benefit                                      |
|:----------------|:----------------------------------------------|
| Relay assist    | Extends W1209 relay life                     |
| Direct feed     | Full override even in case of hardware failure |
| Dual protection | No current loops, no interference            |
| Fully passive   | No firmware dependency on Shelly             |
| Scalable        | Can be upgraded with further scripts or alarms |

---

### Tests and Results

| Test                   | Result                                   |
|:------------------------|:------------------------------------------|
| Single relay assist     | Fans activated via W1209 relay            |
| W1209 failure simulation| Fans activated via direct Shelly feed     |
| Reverse current test    | No current reflows detected               |
| Redundant continuity    | No dropouts, no misfire events            |
| Thermal stability       | No overheating of relay or wires          |

---

---

## EmergencyCoolingTripleRedundancy v1.0 – Final Version

This advanced version of the emergency cooling circuit ensures **triple redundancy** by:

- Forcing the W1209 relay closure via Shelly (`O` output).
- Directly supplying 12V to the fans from LM2596 step-down.
- Directly supplying 12V (via voltage drop) from 13.8V main line if the step-down fails.

Every line is protected with **Schottky diodes** to prevent backflow and overvoltage.

---

### Logical Circuit Name
`EmergencyCoolingTripleRedundancy v1.0`

---

### Materials Used

| Component             | Description                                      |
|:----------------------|:--------------------------------------------------|
| Shelly Plus 1 + Add-On| Intelligent controller                           |
| 1N5819 Schottky Diodes| Fast diodes for voltage drop and backflow protection |
| LM2596 Step-down      | 13.8V to 12V converter                           |
| Sunon EE40101S1 Fans  | 12V, 7300 RPM, 0.99W fans                        |
| WAGO Terminal Blocks  | Organized cable management                       |
| Cables 0.8mm²         | Power and logic lines                            |

---

### Triple Redundancy Cases

| Case | Shelly O Connection                        | Shelly I Connection         | Diodes Needed | Voltage at Fans | Estimated RPM | RPM Variation | Power Variation |
|:----:|:------------------------------------------:|:---------------------------:|:--------------:|:----------------:|:--------------:|:---------------:|:----------------:|
| 1    | To K0 W1209 (1 diode)                      | From WAGO 12V+ (no diode)   | 1              | ~11.5V           | ~7004 RPM      | -4%             | -7–8%            |
| 2    | To WAGO V+ Ventole (1 diode)              | From OUT+ LM2596 (1 diode)  | 2              | ~11.5V           | ~7004 RPM      | -4%             | -7–8%            |
| 3    | From 13.8V line → 2 diodes → WAGO V+ Ventole | From 12V+ Ventole (1 diode)| 3              | ~12.8V           | ~7787 RPM      | +6.6%           | +13–15%          |

---

### Electrical Diagrams

#### Case 1 – Forcing W1209 Relay

Shelly O → [DIODE 1] → K0 W1209  
Shelly I → WAGO 12V+ Common  
Fans powered by W1209 K0–K1 relay closure

- 1 DIODE on O to protect Shelly output.  
- Caduta tensione ~0.5V → 11.5V effective.

---

#### Case 2 – Direct feed from LM2596

Shelly O → [DIODE 1] → WAGO V+ Ventole  
Shelly I → [DIODE 2] → OUT+ LM2596  
Fans powered directly if W1209 fails

- 1 DIODE on O + 1 DIODE on I.  
- Caduta tensione ~0.5V → 11.5V effective.

---

#### Case 3 – Direct feed from 13.8V with double drop

Shelly O → [DIODE 1] → [DIODE 2] → WAGO V+ Ventole  
Shelly I → [DIODE 3] → WAGO 12V+ Ventole  
Fans powered directly from 13.8V in step-down failure

- 2x DIODEs in series on O + 1 DIODE on I.  
- Caduta tensione totale ~1.0V → 12.8V effective.

---

## Practical Effects

| Condition                  | Effect                                 |
|:---------------------------|:----------------------------------------|
| Normal operation           | Fans controlled by W1209 relay         |
| W1209 partial failure      | Shelly forces relay closure (Case 1)   |
| W1209 full failure + step-down OK | Shelly directly powers fans from LM2596 (Case 2) |
| W1209 and step-down failure| Shelly powers fans from 13.8V (Case 3) |

---

## RPM and Power Variation Analysis

- **At ~11.5V**:  
  - RPM drops ~4%.  
  - Power drops ~7–8% (P ∝ V² approximately for small motors).  

- **At ~12.8V**:  
  - RPM increases ~6.6%.  
  - Power increases ~13–15%.

**All values are safe** for Sunon EE40101S1 fans as per official datasheet (10.2–13.8V operating range).

---

## Safety Best Practices

- Always use heat-shrink tubing or RTV silicone to insulate soldered diode joints.  
- Keep fan wiring separated from 230V lines to minimize EMI (Electromagnetic Interference).  
- Label each WAGO terminal with the correct line identification.  
- Test all failover modes manually before final closing of the enclosure.

---

## Tests and Results

| Test                     | Result                                      |
|:-------------------------|:---------------------------------------------|
| Relay assist             | OK (Shelly closure, fans activation)        |
| Direct feed LM2596       | OK (Shelly direct power, fans activation)   |
| Direct feed 13.8V        | OK (Shelly direct power, higher RPM detected) |
| Reverse current          | No backfeed detected                        |
| Redundancy simulation    | 100% successful fans activation             |

---

## Licensing Notice

All original photographs, electrical schematics, and technical drawings created by the author are licensed under:  
**Creative Commons Attribution - NonCommercial - NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**

Under this license:  
- Copying, sharing, and redistribution of the material are allowed, provided that proper attribution is given to the original author (Cmod777).  
- Commercial use is strictly prohibited.  
- No modifications, transformations, or derivative works are allowed.

For full license details, refer to:  
[https://creativecommons.org/licenses/by-nc-nd/4.0/](https://creativecommons.org/licenses/by-nc-nd/4.0/)

---

## Deprecation Rationale and Transition to CerberusVent©

Following the progressive development and field validation of multiple redundancy configurations (single override, dual path, triple fallback), it became evident that a more integrated and resilient architecture was necessary.

The legacy logic, while effective in test scenarios, suffered from key limitations:
- Voltage drop inefficiencies when relying on Schottky diodes and passive fallback
- Limited thermal sensing coverage (single or dual probe)
- No true separation between control logic and power lines
- No clean failover coordination between step-down, W1209, and Shelly

As a result, all previous versions (`EmergencyCoolingShelly v1.0`, `DualCircuit v1.0`, and `TripleRedundancy v1.0`) are now **officially deprecated** and replaced by the **CerberusVent©** architecture, which introduces:
- A dedicated emergency module with separate control logic
- Multi-source sensing from distributed DS18B20 probes
- Full power source decoupling (step-down + UPS + fallback relay)
- Hardware isolation and modular circuit prioritization

These improvements guarantee **higher reliability**, **simplified debugging**, and **modular expandability**—core requirements for a system deployed in long-term unattended environments.

</details>
