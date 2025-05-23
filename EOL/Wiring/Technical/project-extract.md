# Technical Design Report  
**Advanced Control and Backup System for eBUS-Enabled Boiler Module**  
**Project Code:** EBW-CNTRL-UPS-01  
**Author:** [*Cmod777* - Use only my Github nick]  
**Version:** 1.0  
**Date:** [11.04.2025]

---

## 1. Scope and Purpose

This document outlines the design, purpose, and functional architecture of a modular dual-unit control and backup system for domestic boiler management, based on OpenTherm and eBUS protocols.  
The system is designed for integration with remote control platforms (e.g., Home Assistant), allowing both intelligent automation and safety-grade fallback operations.

---

## 2. System Architecture Overview

The system is composed of two physically and functionally distinct modules:

- **Primary Control Unit (Centralina IP65 Primaria)**:  
  - Manages OpenTherm line switching via isolated relays
  - Provides remotely switchable 230V AC to the Tado controller
  - Allows physical interruption of heating communication logic

- **UPS Backup Unit (Centralina IP65 UPS)**:  
  - Ensures uninterrupted 5V DC power to the eBUS Wi-Fi module during blackout conditions
  - Employs a passive-failover relay and sealed 12V SLA battery
  - Integrates dual-step-down conversion for live and emergency scenarios

---

## 3. Electrical Topology

### 3.1 Power Distribution

| Source       | Path                                    | Destination                     |
|--------------|-----------------------------------------|----------------------------------|
| 230V AC      | Circuit breaker → Meanwell HDR-15-12    | 12V logic bus (relays, Shelly)  |
| 12V DC       | UPS battery (failover relay-controlled) | Step-down Bauer USB-C module    |
| 5V DC        | Step-down modules                       | eBUS Wi-Fi module               |

---

### 3.2 Communication Lines (OpenTherm)

- Physical relay switching (Finder 40.52 DPDT) of **BUS+** and **BUS−**
- OT bus normally disconnected; closed via Shelly Plus trigger logic
- Full galvanic isolation between control logic and high-voltage AC

---

## 4. Functional Blocks Description

### 4.1 Centralina IP65 Primaria

- **Shelly “AF”**: Controls the OT relay; dry contact output energizes relay coil
- **Shelly “TADO”**: Switches 230V AC to thermostat input
- **Relay Module**: Dual-channel (DPDT); 12V coil; switches OT BUS lines
- **EXIT Interfaces**:
  - **EXIT 1**: Tado (230V L/N + OT BUS)
  - **EXIT 2**: Boiler (OT BUS)
  - **EXIT 3**: Reserved for auxiliary functions

---

### 4.2 Centralina IP65 UPS

- **Primary PSU**: Meanwell HDR-15-12 supplies 12V to relay coil
- **Battery Unit**: 12V, 1.2Ah sealed lead-acid, Yuasa or equivalent
- **Failover Relay**: SPST NO, energized during normal operation
- **Step-Down A**: 230V AC to 5V DC Bauer USB-C, powers eBUS during mains
- **Step-Down B**: 12V DC to 5V DC via Bauer USB-C during blackout
- **Diodes**: Schottky (1N5822) to isolate USB-C 5V merge line

---

## 5. System Logic and Conditions

| State                | Grid | Battery | Relay | Output to eBUS | LED Indicators      |
|----------------------|------|---------|--------|------------------|----------------------|
| Normal operation     | ON   | Float   | Closed | 5V from 230V PSU | Blue                |
| Blackout             | OFF  | Active  | Open   | 5V from battery  | Red                 |
| Charging (optional)  | ON   | Float   | Closed | 5V from 230V PSU | Blue + Green        |
| Battery Full         | ON   | Float   | Closed | 5V from 230V PSU | Blue + White        |

---

## 6. Installation and Safety

- All live terminals must be protected via DIN rail breakers and fuses
- Signal-level wiring must use WAGO 221-413 connectors with ferrules
- Use of independent DIN rails and physical segregation between AC and DC paths
- Cable glands on all exits (IP65 or higher)
- All control logic (Shelly, relays) must operate at 12V DC only

---

## 7. Compliance and Maintenance

- Battery must be checked every 6 months for capacity and integrity
- Relay switching must be tested periodically using blackout simulation
- Visual inspection of LEDs required monthly
- System complies with **CE Low Voltage Directive** and **EN 60335-1** if installed properly

---

## 8. System Expansion (Optional)

- Integration of ESP32 with analog voltage reading on battery
- MQTT publishing of UPS state via Shelly or custom firmware
- Addition of temperature sensors to housing to monitor heating

---

## 9. Documentation

- Complete wiring schematics (PNG/SVG)
- Markdown block-by-block visual logic
- Material list with technical specs
- License: **CC BY-NC-SA 4.0** – Attribution, non-commercial, share alike

---

**End of Document**
