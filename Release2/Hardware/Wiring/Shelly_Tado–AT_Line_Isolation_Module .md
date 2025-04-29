# Shelly Tado – AT Line Isolation Module – Assembly and Test Report

## Module Description
Auxiliary circuit based on a **Shelly Plus 1** device, used to **physically isolate** the thermostat connection ("AT" line) between the smart thermostat and the boiler.  
The module ensures a **hardware-level disconnection** in case of **malfunction** or **undesired activation** of the smart thermostat (e.g., accidental heating system activation during summer months).

---

## Logical Circuit Name
`ShellyTadoIsolator v1.0`

---

## Materials Used
| Component | Description |
|:----------|:------------|
| Shelly Plus 1 | Wi-Fi relay with dry contact support |
| WAGO 1:1 connector | Quick terminal (1 input / 1 output) |
| 4-pin Nylon aviation connector | Mechanical connection for AT and BUS lines |
| Red/Black 0.8mm² wire | For AT line interruption |
| 230V wiring (2.5mm²) | For power supply (N, PE, L protected) |

---

## Functional Overview

- **Power Supply**:
  - Shelly powered directly from the common terminal block (protected 230V L, N, PE).
  
- **AT Line Isolation**:
  - The **Shelly O/I contact** is wired in series with the AT line.
  - **Normal operation**: Shelly contact closed → AT line connected → normal thermostat control.
  - **Isolation mode**: Shelly contact open → AT line physically disconnected → prevents unwanted boiler activation.

- **Wiring**:
  - AT wires (0.8mm²) routed through:
    - Shelly Plus 1 contact (O/I).
    - WAGO 1:1 connector for easy installation and maintenance.
    - 4-pin aviation connector (Nylon) with pin assignment:
      | Pin | Signal | Note |
      |:---:|:-------|:-----|
      | 1   | AT Line 1 | Polarity irrelevant |
      | 2   | AT Line 2 | Polarity irrelevant |
      | 3   | BUS+ | Reserved for future wiring |
      | 4   | BUS− | Reserved for future wiring |

- **Protections**:
  - No additional protection circuitry needed.
  - Shelly includes built-in protections against overloads and transients.

---

## Assembly Procedure

### 1. Component Preparation
- Verify Shelly Plus 1 wiring diagram.
- Check wire gauge and crimp terminals.

### 2. Power Connection
- Connect Shelly Plus 1 to the common terminal block (protected L, N, PE 230V).

### 3. AT Line Routing
- Cut the AT cable and insert it through Shelly’s O/I contact.
- Install WAGO 1:1 connector between Shelly and aviation connector.
- Connect to the aviation connector (Pin 1 and Pin 2 for AT line).

### 4. Final Checks
- Ensure correct mechanical fixation.
- Verify continuity and insulation.

---

## Tests Performed

| Test | Result |
|:-----|:-------|
| Power supply check | Shelly powered correctly from common terminal block |
| AT line continuity test | Proper connection when Shelly contact is closed |
| AT line disconnection test | Proper isolation when Shelly contact is open |
| Relay switching test | Normal switching, no contact sticking |
| Functional simulation | Boiler activation correctly controlled through Shelly |

---

## Final Considerations
- **Full functionality confirmed.**
- **Added physical isolation greatly enhances safety** in the heating system management.
- **Critical** to avoid unintended boiler operation during periods like summer.

---

## Extra Tip
This module was designed specifically to address a rare but critical failure scenario where the smart thermostat could incorrectly activate the heating system (e.g., during summer, causing unwanted radiator heating).  
By **physically isolating the AT line** through a remote-controlled relay (Shelly), the system ensures an extra layer of **security and reliability** beyond software-based protections.

---

## Timestamp
**Completion date:** 2025-04-28  
**Approximate time:** 22:30 local time  
**Responsible:** [GitHub nickname]

---

## Notes
- Always refer to the official datasheets and wiring instructions for each component before installation.
- Logical circuit name for documentation and maintenance: `ShellyTadoIsolator v1.0`.

---
## Functional Block Diagram – Shelly Tado Module (RelayCoilProtection v1.0)

```plaintext
[230V Mains L/N/PE]
         |
         v
[Common Terminal Block] ----+
                             |
                             +--> [Shelly Plus 1]
                                    | 
                                    +--(O/I contact wired to)--+
                                                              |
                                                      [AT Line Cut]
                                                              |
                                              +------------+-----------+
                                              |                        |
                                         [WAGO 1:1]            [4-pin Nylon Connector]
                                              |                        |
                                   (Pin 1: AT Line 1)       (Pin 2: AT Line 2)
                                   (Pin 3: BUS+ reserved)   (Pin 4: BUS- reserved)

```
---

## Diagram Notes
- Pin 3 and Pin 4 on the aviation connector are reserved for BUS+ and BUS− signals (handled in the next module).
- No additional protections are needed: Shelly internal protections are sufficient.
- The disconnection system ensures **physical hardware isolation** in case of smart thermostat failure.

---

# Licensing Notice

All original photographs, electrical schematics, and technical drawings created by the author are licensed under:

**Creative Commons Attribution - NonCommercial - NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**

Under this license:
- Copying, sharing, and redistribution of the material are allowed, provided that proper attribution is given to the original author (Cmod777).
- Commercial use is strictly prohibited.
- No modifications, transformations, or derivative works are allowed.

For full license details, refer to: [https://creativecommons.org/licenses/by-nc-nd/4.0/](https://creativecommons.org/licenses/by-nc-nd/4.0/)

---
