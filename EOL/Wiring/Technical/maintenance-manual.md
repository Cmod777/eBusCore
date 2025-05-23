# Maintenance and Inspection Manual  
**System:** Advanced eBUS Wi-Fi Boiler Control + UPS Backup  
**Project Code:** EBW-MAINT-01  
**Version:** 1.0  
**Document Type:** Technical Maintenance Program  
**Author:** [*Cmod777* use my GitHub nick]  
**Date:** [11.04.2025]  

---

> **Important Notice**  
> This project is released under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.  
> It is not certified for commercial or industrial use and must not be used in CE-compliant or production-grade environments without explicit authorization.  
> All references to standards (EN, CEI, CE, WEEE) are for informational and educational purposes only.

---


## 1. Introduction

This document provides the complete operational and maintenance plan for the integrated control and backup system designed for domestic boiler applications, based on OpenTherm and eBUS standards.

The system is designed to ensure reliability in heat management, remote control, and uninterrupted power supply during electrical failures.

---

## 2. Purpose and Scope

The purpose of this manual is to:

- Define all required maintenance actions and intervals
- Specify the tools, responsibilities and procedures required for safe operation
- Ensure long-term performance and compliance of the system
- Provide a traceable structure for inspections and preventive actions

This document applies to the full installation, including:

- **Primary Control Module (Centralina IP65)**
- **Backup Power Module (UPS Unit)**
- All internal and external cabling and connected sensors/modules

---

## 3. System Overview

| Module        | Functionality Summary                                                    |
|---------------|---------------------------------------------------------------------------|
| Control Unit  | Relay-driven OT bus switching, remote 230V control to Tado, LED feedback |
| UPS Unit      | 12V SLA battery failover logic, USB-C dual step-down, relay switching     |
| eBUS Device   | Powered via USB-C from both modules, handles boiler communication         |

The system is modular and can be inspected, tested, and maintained independently or in full.

---

## 4. System Technical Specifications

### 4.1 Electrical Characteristics

| Parameter                     | Value                             | Notes                                      |
|-------------------------------|------------------------------------|--------------------------------------------|
| Main input voltage (AC)       | 230V ±10%, 50Hz                    | Supplied via DIN rail breaker              |
| DC bus (logic, relays)        | 12V DC (Meanwell HDR-15-12)        | Powering relay coils, Shelly modules       |
| Backup battery voltage        | 12V nominal (SLA/AGM)              | 13.0V full, 12.0V nominal, <11.5V replace   |
| Step-down output (USB-C)      | 5V DC @ 1.5A max                   | Used to power eBUS module                  |
| Relay coil voltage            | 12V DC, nominal 20–40mA            | Finder 40.52 or equivalent                 |
| Relay contact rating          | ≥ 2A @ 24V DC                      | Switching OT BUS and battery               |

---

### 4.2 Cabling Requirements

| Line Type      | Suggested Cable     | Section        | Color Code        | Notes                        |
|----------------|---------------------|----------------|--------------------|-------------------------------|
| 230V AC        | H07V-K / H05V-K      | 1.5 mm²        | Brown / Blue       | L/N conductors, DIN wiring    |
| PE Ground      | Green/Yellow        | 1.5–2.5 mm²    | G/Y                | Connected to DIN rail         |
| 12V DC Power   | H05V-K               | 0.75–1.0 mm²   | Red / Black        | From Meanwell to relays/WAGO |
| OT BUS lines   | Twisted Pair, 0.5 mm²| 0.5 mm²        | Yellow / Blue      | BUS+ and BUS−                 |
| USB-C Out      | Shielded 2-core     | 0.5 mm²        | Red / Black        | From step-down to eBUS       |
| Battery lines  | Flexible, fused     | 1.0–1.5 mm²    | Red / Black        | Short & direct to relay/WAGO |

---

### 4.3 Thermal Ratings

| Component               | Max Operating Temp | Notes                          |
|-------------------------|--------------------|---------------------------------|
| Meanwell HDR-15-12      | 70°C               | Mounted vertically              |
| SLA Battery             | 40°C               | Use in ventilated space         |
| Relays (Finder)         | 85°C               | Ensure airflow or spacing       |
| Step-Down Converters    | 60°C               | Mount on vented DIN bracket     |
| LED Indicators          | 60°C               | Panel mount or DIN clip mount   |

---

### 4.4 Insulation and Safety Classes

| Component             | Insulation Class | Notes                          |
|------------------------|------------------|---------------------------------|
| Meanwell Power Supply  | Class II         | Double insulation              |
| Relay (Finder)         | Class I          | Grounded via DIN socket        |
| Shelly Modules         | SELV             | Powered via 12V only           |
| Step-Down Modules      | SELV             | Output 5V only                 |
| USB-C Line             | SELV             | Protected via diodes/fuse      |

---

### 4.5 System Protection Devices

| Device Type               | Location                 | Rating / Spec         |
|---------------------------|--------------------------|------------------------|
| AC Circuit Breaker        | Control Unit Input       | 2A C-Curve DIN rail    |
| Battery Fuse              | Near battery terminal    | 2A inline or blade     |
| Step-down Output Fuse     | USB-C line (optional)    | 0.5A fast-blow         |

---

All components shall comply with CE, RoHS, and where applicable, EN 60335-1 and EN 60950 safety directives.

---

## 5. Component Datasheet Summary

This section provides a concise technical summary of each key component in the system, including its function, voltage, contact type, mounting format, and isolation class.

---

### 5.1 Active Components

| Component Name            | Model / Ref             | Voltage      | Mount Type     | Function                             | Isolation Class |
|---------------------------|--------------------------|--------------|----------------|--------------------------------------|------------------|
| Meanwell Power Supply     | HDR-15-12                | 230V AC / 12V DC | DIN rail     | DC logic power supply                | Class II         |
| Finder Relay (OT Control) | 40.52.9.012.0000         | 12V DC coil    | DIN w/ base    | DPDT relay for OT BUS lines          | Class I          |
| Shelly "AF"               | Shelly Plus 1 Mini (12V) | 12V DC input   | DIN clip       | OT relay control via dry contact     | SELV             |
| Shelly "TADO"             | Shelly Plus 1 Mini (12V) | 12V DC input   | DIN clip       | 230V AC control to thermostat        | SELV             |
| USB-C Step-Down (grid)    | Bauer 230V→5V 15W        | 230V AC       | Bracket        | Primary eBUS power                   | SELV             |
| USB-C Step-Down (UPS)     | Bauer 12V→5V 15W         | 12V DC        | Bracket        | Backup eBUS power                    | SELV             |
| Battery Relay (Failover)  | Generic SPST 12V NO      | 12V coil      | DIN mountable  | Switches battery to step-down       | Class I          |

---

### 5.2 Passive Components

| Component         | Value / Spec      | Function                              | Notes                          |
|-------------------|-------------------|----------------------------------------|---------------------------------|
| SLA Battery        | 12V, 1.2–7Ah       | Backup power for UPS                  | Maintenance every 3–5 years     |
| Diode (Schottky)   | 1N5822             | Prevents 5V backfeeding                | Between step-downs and USB-C    |
| LED Indicators     | 3mm or 5mm (Blue, Red, Green, White) | Status indicators   | Use series resistor (330–470Ω) |
| Resistors          | 330Ω–470Ω, ¼ W     | Current limiting for LEDs             | 1 per LED                       |

---

### 5.3 Connectors and Interfaces

| Component         | Model / Type         | Poles | Function                            | Mount Type     |
|-------------------|----------------------|-------|--------------------------------------|----------------|
| WAGO Terminals     | 221-413              | 3     | All internal wiring + OT BUS         | DIN rail       |
| USB-C Output Port  | Panel-mount socket   | 5V+ / GND | Power to eBUS module               | Panel or clip  |
| Cable Glands       | M20, nylon or rubber | 1 per EXIT | Protect exits (IP65)             | Panel thread   |

---

### 5.4 External Exits

| Exit  | Destination      | Voltage Types     | Cables Required         | Protection Level |
|-------|------------------|-------------------|--------------------------|------------------|
| EXIT 1| Tado controller  | 230V AC + OT BUS  | 4-core: L, N, BUS+, BUS− | Cable gland IP65 |
| EXIT 2| Boiler OT input  | OT BUS only       | 2-core: BUS+, BUS−       | Cable gland IP65 |
| EXIT 3| Reserved         | Optional AC/DC    | Depends on future use    | As needed        |

---

All components must be mounted in accordance with their datasheet mechanical specs and derating values.

---

## 6. Compliance and Regulatory Reference

The entire system is designed in accordance with European electrical safety and environmental standards. The following directives, standards, and classification schemes apply.

---

### 6.1 Electrical Safety Standards

| Regulation / Standard     | Scope                                                | Applicability                    |
|----------------------------|------------------------------------------------------|----------------------------------|
| **EN 60335-1**             | General requirements for household electrical devices| All 230V components              |
| **EN 60950 / EN 62368**    | IT and low-voltage control equipment                 | Step-down modules, Shelly        |
| **EN 50110-1**             | Safety of maintenance personnel                      | Required for all interventions  |
| **EN 61439-1**             | Low-voltage switchgear assemblies                    | Control and UPS enclosures       |

---

### 6.2 Low Voltage and SELV Guidelines

| Classification   | Description                                | Application                        |
|------------------|--------------------------------------------|-------------------------------------|
| **SELV**          | Safety Extra Low Voltage (<50V DC)         | 5V USB-C, 12V relays and Shelly     |
| **Class I**       | Grounded insulation (metal parts earthed)  | Relays, DIN rail, boiler interfaces |
| **Class II**      | Double/reinforced insulation (no ground)   | Meanwell HDR-15-12 power supply     |

---

### 6.3 Environmental & Disposal Standards

| Directive / Symbol      | Purpose                                 | System Elements Covered              |
|--------------------------|------------------------------------------|--------------------------------------|
| **RoHS 2011/65/EU**      | Restriction of hazardous substances      | All electronic modules               |
| **WEEE 2012/19/EU**      | Waste disposal for electronics and batteries | SLA battery, Shelly, relays       |
| **Battery Directive**    | Recycling of sealed lead-acid batteries | Battery block                        |

---

### 6.4 Markings and Labels (Mandatory)

| Item                | Requirement                         | Label Type / Location              |
|---------------------|--------------------------------------|------------------------------------|
| Main Enclosure      | System ID, Voltage, Warning Symbol   | Permanent engraved or printed      |
| Terminals (WAGO)    | Voltage type (AC/DC), Polarity       | Printed marker or color coded      |
| EXIT Lines          | Destination (TADO, BOILER, AUX)      | Permanent label or heatshrink tag  |
| Battery Compartment | “Sealed Lead-Acid – Do Not Open”     | Inside or lid-mounted              |

---

### 6.5 Electrical Protection Requirements

- All 230V AC lines must be protected by DIN rail-mounted **MCB (Miniature Circuit Breakers)** rated **2A C-Curve**
- The SLA battery must be fused with a **1–2A inline blade fuse** within 15 cm of the positive terminal
- USB-C step-down outputs should include a **fast-blow fuse 0.5A** for device protection

---

Failure to comply with the above standards may result in loss of CE conformity and invalidate the safety profile of the system.

---

## 7. Extended Maintenance Program

This section provides a detailed maintenance and verification schedule, broken down by inspection frequency, assigned responsibility, required instruments, and acceptable operational thresholds.

---

### 7.1 Monthly Tasks

| Task                               | Tool / Instrument       | Acceptable Range        | Performed By      |
|------------------------------------|--------------------------|--------------------------|-------------------|
| Visual inspection of LED status    | None                     | LEDs functioning         | User / Technician |
| Panel and gland integrity check    | Visual                   | No cracks / water ingress| Technician        |

---

### 7.2 Quarterly Tasks (Every 3 Months)

| Task                               | Tool / Instrument       | Expected Value / Range   | Notes                        |
|------------------------------------|--------------------------|---------------------------|-------------------------------|
| Battery voltage under no load      | Digital Multimeter       | ≥12.4V (float)            | Below 12.0V → monitor         |
| Battery voltage under load         | DMM + 0.5A test load      | ≥11.8V                    | Below 11.5V → replace soon    |
| Relay activation test (Shelly "AF")| Manual toggle or HA cmd  | Audible click, relay closes| Confirm BUS path continuity |

---

### 7.3 Semi-Annual Tasks (Every 6 Months)

| Task                               | Tool / Instrument       | Expected Outcome         | Notes                         |
|------------------------------------|--------------------------|---------------------------|-------------------------------|
| Full continuity test of OT BUS     | DMM / continuity tester  | <2 Ohms                   | Tado to Boiler via relay path |
| Check all WAGO terminals           | Manual tug test          | No movement               | Tighten or replace if loose   |
| Step-down USB output test          | DMM                      | 4.8V–5.2V under 500mA     | From both modules             |

---

### 7.4 Annual Tasks

| Task                               | Tool / Instrument       | Expected Outcome         | Notes                          |
|------------------------------------|--------------------------|---------------------------|--------------------------------|
| Simulate blackout (UPS test)       | Disconnect 230V input    | eBUS remains powered      | Confirm red LED ON             |
| Battery capacity stress test       | 5V load @ 1A for 10min   | ≥11.4V post-test          | Check step-down temperature    |
| Firmware update of Shelly modules  | Web UI or App            | Latest version installed  | Backup config before update    |

---

### 7.5 Replacement Timelines

| Component        | Expected Life     | Condition for Replacement |
|------------------|-------------------|----------------------------|
| SLA Battery      | 3–5 years          | Voltage sag / swelling     |
| Finder Relays    | 100,000 operations | Sticking / click failure   |
| LED indicators   | 10+ years          | Burnout / no response      |
| Step-down modules| 5–7 years          | Output instability         |
| WAGO terminals   | N/A                | If loose / discolored      |

---

### 7.6 Maintenance Record Template

Below is a Markdown-compatible table for recording regular maintenance:

| Date       | Task Performed           | Result               | Technician    | Notes              |
|------------|---------------------------|-----------------------|---------------|---------------------|
| 2025-04-01 | Battery voltage check     | 12.6V, OK             | Name1         | Float mode verified |
| 2025-04-01 | Blackout simulation test  | eBUS remained powered | Name2         | LED Red active      |
| 2025-04-01 | WAGO terminal inspection  | All tight, no damage  | Name3         | No oxidation        |

---

All interventions should be logged, signed, and stored in digital format or in the enclosure binder (if available).

---

## 8. Functional Testing Protocols

This section defines a series of validation steps to confirm full system functionality after installation, maintenance, or troubleshooting.

Each test includes its purpose, method, expected values, and corrective action if results deviate.

---

### 8.1 OT Relay Switching Test

**Purpose:** Verify proper operation of OT BUS relay triggered by Shelly “AF”

| Step                                       | Tool       | Expected Result         | Action if Failed               |
|--------------------------------------------|------------|--------------------------|--------------------------------|
| Manually activate Shelly “AF”              | Shelly App | Audible click from relay | Check wiring and 12V supply    |
| Measure continuity between COM and NO      | DMM        | <1 Ohm (closed)          | Replace relay or check coil    |
| Deactivate Shelly “AF”                     | App        | Relay opens (no contact) | Check NO/COM configuration     |

---

### 8.2 Shelly “TADO” 230V Control Test

**Purpose:** Confirm that Tado receives controlled AC via Shelly

| Step                                       | Tool       | Expected Result           | Action if Failed               |
|--------------------------------------------|------------|----------------------------|--------------------------------|
| Activate Shelly “TADO”                     | Shelly App | 230V at EXIT 1 (L/N)       | Verify wiring, relay, breaker  |
| Deactivate and re-measure                  | Multimeter | 0V                        | Check Shelly relay             |

---

### 8.3 USB-C 5V Output Test (Normal + Backup)

**Purpose:** Validate that eBUS module is powered in all conditions

| Condition         | Tool       | Expected 5V Output | Action if Failed                       |
|-------------------|------------|--------------------|----------------------------------------|
| Grid ON           | DMM        | 4.8–5.2V            | Check 230V step-down & fuse            |
| Simulated blackout| DMM        | 4.8–5.2V            | Verify battery voltage, relay, fuse    |
| Return to grid    | DMM        | Stable switchback   | Confirm relay deactivates correctly    |

---

### 8.4 LED Behavior Test

**Purpose:** Verify visual status indicators for system state

| LED    | Trigger Condition         | Expected State | Action if Not Lit            |
|--------|----------------------------|----------------|------------------------------|
| Blue   | 230V present                | ON             | Check 12V Meanwell & resistor|
| Red    | 230V OFF (battery active)  | ON             | Check relay and 12V battery  |
| Green  | Battery charging (opt.)    | ON             | Check charging module        |
| White  | Battery full (opt.)        | ON             | Check float detection logic  |

---

### 8.5 BUS Line Integrity Test

**Purpose:** Ensure continuity between Tado and Boiler only when relay is active

| Step                                     | Tool       | Expected Result             | Action if Failed             |
|------------------------------------------|------------|------------------------------|------------------------------|
| Relay OFF (AF inactive)                  | DMM        | No continuity (infinite)     | Confirm relay NO contacts    |
| Relay ON (AF active)                     | DMM        | <2 Ohms continuity           | Check BUS wiring / terminals |

---

Testing should be repeated after every hardware modification or firmware upgrade.  
Logs must be recorded in the Maintenance Log Template.

---

## 9. Emergency Procedures and Recovery

This section describes recommended actions in case of critical failure, including hardware fallback operations, recovery protocols, and system bypass options when applicable.

---

### 9.1 Power Failure Recovery (Blackout)

| Condition                     | Immediate Action                          | Notes                              |
|-------------------------------|--------------------------------------------|-------------------------------------|
| Grid power loss               | UPS module activates automatically         | Confirm Red LED is ON               |
| eBUS not powered during outage| Check relay, battery voltage, 5V output    | Switch back to grid after recovery  |
| After power returns           | Relay opens, returns to grid-sourced 5V    | Ensure USB-C switching is clean     |

---

### 9.2 Battery Failure

| Symptom                        | Diagnosis Steps                        | Recovery Action                     |
|--------------------------------|----------------------------------------|-------------------------------------|
| eBUS turns off in blackout     | Measure battery: <11.5V                | Replace SLA battery immediately     |
| Battery bloated or warm        | Visual + temperature inspection        | Disconnect and dispose properly     |
| Charging LED never turns off   | Possible float circuit fault           | Verify voltage stabilizer or charger|

---

### 9.3 Relay Stuck or Fails to Switch

| Symptom                        | Diagnosis Steps                        | Recovery Action                     |
|--------------------------------|----------------------------------------|-------------------------------------|
| Relay doesn’t click (AF or UPS)| Measure 12V coil                       | Check fuse or replace relay module  |
| Relay always closed (bypassed) | Remove control signal + check contact  | Replace or isolate module           |

---

### 9.4 Step-Down Failure (5V USB-C)

| Symptom                        | Diagnosis Steps                        | Recovery Action                     |
|--------------------------------|----------------------------------------|-------------------------------------|
| No 5V output on USB-C          | Measure input, then output             | Replace module or check fuses       |
| USB-C only works on one source | Check diode orientation (1N5822)       | Replace failed diode or converter   |

---

### 9.5 Shelly Module Failure

| Module       | Common Failures                 | Suggested Response               |
|--------------|----------------------------------|----------------------------------|
| Shelly “AF”  | No relay output / no connection | Power cycle or factory reset     |
| Shelly “TADO”| No 230V to thermostat            | Check app + verify wiring        |
| Both         | Unreachable on network          | Restart router / reflash firmware|

---

### 9.6 Temporary Bypass (for emergency heating)

If the eBUS Wi-Fi module is not operational and urgent heating is required:

1. **Disconnect EXIT 1 (Tado)** if stuck
2. **Manually short OT BUS+ and BUS−** from Tado to Boiler (if safe)
3. **Power Tado directly via external 230V socket**
4. **Monitor boiler from local interface only**

> This bypass is temporary and must be undone once system is repaired.

---

Always log all emergency actions, failures, and corrective measures in the Maintenance Record Template.

---

## 10. Document Control and Revision History

This manual is a controlled technical document. All modifications must be versioned, logged, and approved by the project maintainer or system integrator.

---

### 10.1 Version Tracking

| Version | Date       | Author               | Description                           |
|---------|------------|----------------------|---------------------------------------|
| 1.0     | 2025-04-11 | [Your GitHub Username] | Initial release – full maintenance program |
| 1.1     | TBD        |                      |                                       |
| 1.2     | TBD        |                      |                                       |

---

### 10.2 File Location and Access

| Location Type     | Path or Link                                | Notes                               |
|-------------------|----------------------------------------------|-------------------------------------|
| GitHub Repository | `https://github.com/Cmod777/eBusCore        | Main project files and README       |
| Printed Copy      | Inside DIN cabinet (optional)               | Must be updated with digital version|
| PDF Export        | `/docs/maintenance-manual.pdf`              | For distribution to technicians     |

---

### 10.3 Authorization (For professional use only)

| Role               | Name                  | Signature       | Date         |
|--------------------|------------------------|------------------|--------------|
| System Designer    |                        |                  |              |
| Installation Lead  |                        |                  |              |
| Maintenance Lead   |                        |                  |              |

> Use this section if the system is deployed in a professional or certified environment.

---

---

## 11. Risk Assessment Matrix

This section identifies and classifies potential risks associated with the operation, maintenance, and installation of the system.

| Risk ID | Description                              | Likelihood | Severity | Risk Level | Mitigation Measures                         |
|---------|------------------------------------------|------------|----------|------------|---------------------------------------------|
| R-01    | Electric shock from 230V terminals        | Medium     | High     | **High**   | Use DIN breakers, label terminals, use PE   |
| R-02    | Battery short-circuit (12V SLA)           | Low        | High     | **Medium** | Inline fuse, covered terminals, WAGO usage  |
| R-03    | Relay fails to switch (OT BUS frozen)     | Low        | Medium   | **Low**    | Test relay semi-annually                    |
| R-04    | eBUS module unpowered during blackout     | Low        | Medium   | **Low**    | Simulate blackouts yearly, check 5V supply  |
| R-05    | Overheating of power modules              | Low        | Medium   | **Low**    | Use vented DIN case, thermal inspection     |
| R-06    | Incorrect Shelly command triggers heating | Medium     | Low      | **Medium** | Use Home Assistant automation failsafes     |
| R-07    | Wire detachment inside DIN enclosure      | Medium     | Medium   | **Medium** | Use ferrules, retighten WAGO every 6 months |
| R-08    | Unsupervised firmware updates             | Medium     | High     | **High**   | Perform updates manually, with rollback     |

> Risk levels are classified using the EN ISO 12100 methodology.

---

## 12. Standard Operating Procedures (SOP)

The following are official Standard Operating Procedures for safe operation, maintenance, and reconfiguration of the system.

Each SOP must be executed by qualified personnel only.

---

### SOP-01: Safe Power-Off Procedure

1. Notify all users of service interruption.
2. Disconnect 230V AC input using main DIN breaker.
3. Confirm power-off with voltage tester at:
   - EXIT 1 (L/N)
   - Meanwell 12V terminals
   - Step-down input terminals
4. Wait at least 30 seconds before opening the DIN case.

> Always test before touching.

---

### SOP-02: Replacing the SLA Battery

1. Execute SOP-01.
2. Disconnect WAGO terminals #3 (V+) and #4 (GND) from battery.
3. Remove battery using insulated gloves.
4. Check for swelling, corrosion, leaks.
5. Install new SLA 12V battery of same spec.
6. Reconnect WAGO terminals, tighten.
7. Re-enable AC power and test voltage.

---

### SOP-03: Simulating a Blackout

1. Ensure eBUS is connected via USB-C.
2. Execute SOP-01.
3. Confirm Red LED turns ON.
4. Measure USB-C voltage: must stay at 4.8–5.2V.
5. Measure battery voltage under load.
6. Reconnect AC input and confirm Blue LED returns.

---

### SOP-04: Relay Switching Test (Shelly “AF”)

1. Log into Shelly interface or Home Assistant.
2. Activate relay from software.
3. Listen for relay click and confirm BUS contact continuity.
4. Deactivate and verify relay opens.
5. Log result in maintenance record.

---

### SOP-05: Shelly Firmware Upgrade

1. Back up current settings.
2. Check manufacturer site for latest firmware.
3. Apply update via Web UI.
4. Monitor upgrade completion.
5. Test post-update functionality:
   - Relay switching
   - AC output (Shelly “TADO”)
   - Automation integration

---

Each SOP must be logged in the system maintenance record if executed.  
Only certified installers may add or modify SOPs.


---

## 13. Warranty and Disclaimer

### 13.1 Scope of Warranty

This system is provided “as-is”, without any express or implied warranty of functionality, performance, or fitness for a particular purpose.  
The author does not guarantee uninterrupted operation or fault tolerance of this design in any commercial or safety-critical application.

---

### 13.2 User Responsibilities

The user is solely responsible for:

- Correct installation and configuration
- Verification of electrical safety measures
- Regular inspection and maintenance as per this manual
- Ensuring compliance with local electrical codes and directives
- Performing all updates and replacements as recommended

---

### 13.3 Liability Limitation

Under no circumstances shall the system designer, contributor, or maintainer be held liable for:

- Damage to property, data loss, fire or electric shock
- Loss of functionality due to incorrect modifications
- Failures due to incompatible hardware integrations
- Injuries or accidents during installation or maintenance

---

### 13.4 License

All documentation and software associated with this project are distributed under the following terms:

**License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

- **Attribution Required** → You must credit the author (GitHub username only)
- **Non-Commercial Use Only** → Commercial use is strictly prohibited
- **Share Alike** → Derivatives must be shared under the same license

> For full license terms, visit:  
> [https://creativecommons.org/licenses/by-nc-sa/4.0](https://creativecommons.org/licenses/by-nc-sa/4.0)

---

### 13.5 Final Notice

By deploying, modifying, or reproducing this system, you agree to the above terms.  
If you do not accept these conditions, do not use this project.

---

### 14. End of Document

This concludes the technical maintenance manual for the Advanced eBUS Wi-Fi Control System and UPS Backup Module.  
For additional documentation (wiring diagrams, datasheets, licensing), refer to the project root folder or the GitHub repository.

