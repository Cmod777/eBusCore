# Advanced Boiler Control System – High-Level Overview EOL (End-of-Life)

## Logical Architecture (Module 1 + Module 2)

```
                [230V AC MAIN SUPPLY]
                        |
            +-----------+-----------+
            |                       |
            v                       v
 [Module 1 - Primary Control Unit]  [Module 2 - UPS Backup Unit]
            |                       |
            |                       |
     +------+--------+        +-----+-----+
     | Meanwell 12V  |        | Meanwell 12V  |
     +------+--------+        +-----+-----+
            |                       |
   +--------+-------+         +-----+------------------+
   |                |         |                        |
   v                v         v                        v
[Relay (OT BUS)] [Shelly "AF"] [Battery 12V]  [Relay UPS → DC/USB-C]
   |                |             |                 |
   |                v             |                 |
   |       [Relay trigger]        |        [Step-down to 5V USB-C]
   |                              |                 |
   +-----> [BUS+ / BUS−] <--------+-----------------+
              (switched)
                  |
               [BOILER]
```

---

## Functional Summary

- **Module 1** handles OT communication between the Tado controller and the boiler, with Shelly devices managing relay and power control.
- **Module 2** provides automatic **UPS backup** to the eBUS WiFi module in case of power failure, using a sealed lead-acid battery and a relay-driven step-down to USB-C.
- The modules are **independent but coordinated**: Module 2 activates only during blackouts and feeds Module 1’s core eBUS device.

---

## Next Steps

- Add full wiring details: WAGO connectors, LEDs, fuses, diodes
- Document real-time logging scripts
- Define UPS trigger logic and fallback mode
- Home Assistant integration and automation examples



# Module 1 – Primary Control Unit (IP65 Enclosure)

## Functional Overview

The primary control unit manages the connection between the Tado thermostat and the boiler via the OT (OpenTherm) communication bus.  
It provides relay-controlled line switching, independent power supply management, and automation interfaces via Wi-Fi using Shelly modules.

---

## Block Diagram

```
                    [ 230V AC INPUT ]
                           |
                +----------+-----------+
                |                      |
        +-------v------+       +-------v------+
        | Meanwell 12V |       | Shelly TADO  |
        |  HDR-15-12   |       | (controls     |
        | (DIN mount)  |       |  Tado power)  |
        +-------+------+       +-------+------+
                |                      |
                |                      +--> [ TADO Controller 230V ]
                |
                +--> V+ --+
                |         |
                |     +---v--------------------------+
                |     | Shelly AF (controls OT BUS) |
                |     +---+--------------------------+
                |         |
                |         v
                |    +----+------------------+
                |    |  Relay (FINDER 40.52) |
                |    |   12V DC DPDT Relay   |
                |    +----+------------------+
                |         |
                |    [ A1 / A2 coil ]  → V+ / GND from Meanwell
                |         |
                |     Contacts:
                |       - COM → BUS+ / BUS− from Tado
                |       - NO  → BUS+ / BUS− to Boiler
                |
                +--> V+ --> [ Power ON LED (Blue) ]
                |
                +--> GND (shared by all components)
```

---

## Component List

- **Meanwell HDR-15-12** – 230V to 12V DC power supply (DIN rail)
- **Finder 40.52 Relay (12V DC, DPDT)** – switches BUS+ and BUS−
- **Shelly Plus 1PM “AF”** – controls OT relay (disables/enables line)
- **Shelly Plus 1PM “TADO”** – controls 230V power to Tado thermostat
- **Blue LED** – indicates 12V DC presence
- **WAGO 3-way connectors** – used throughout for power and signal distribution

---

## Output Lines

- **EXIT 1 → TADO**
  - 230V AC (controlled by Shelly “TADO”)
  - OT BUS+ and BUS− to relay COM terminals

- **EXIT 2 → Boiler**
  - BUS+ and BUS− (switched via relay NO terminals)

- **EXIT 3 → Main panel**
  - Optional 230V output (for service or backup line)

---

## Notes

- The OT line is physically interrupted by the relay.
- The Shelly “AF” module toggles the relay coil (A1/A2) via 12V DC.
- All low-voltage lines (12V) are supplied by the Meanwell and shared using WAGO terminals.
- The Power ON LED is optional but recommended for quick diagnostics.
- The entire setup is housed in an IP65 DIN-rail compatible enclosure.


# Module 2 – UPS Backup Unit (DIN Vertical Enclosure)

## Functional Overview

The UPS backup unit ensures that the eBUS Wi-Fi module remains powered during a blackout.  
It provides automatic switching from grid power to a 12V battery, and delivers 5V via USB-C using a step-down module.  
Activation is handled by a relay triggered only when the 230V supply is lost.

---

## Block Diagram

```
                 [ 230V AC INPUT ]
                         |
              +----------+----------+
              |                     |
     +--------v-------+   +---------v--------+
     | Meanwell 12V   |   |  Relay: Normally |
     |  HDR-15-12     |   |  Open (Blackout) |
     |  (DIN mount)   |   +---------+--------+
     +--------+-------+             |
              |                     |
              |             +-------v--------+
              |             |  Battery 12V    |
              |             |  (Lead-acid)    |
              |             +-------+--------+
              |                     |
        +-----v------+      +-------v--------+
        | USB Step-Down |    | USB Step-Down |
        | 230V → 5V USB |    | 12V → 5V USB   |
        +-----+--------+    +-------+--------+
              |                     |
              +---------+----------+
                        |
                        v
            [ USB-C OUTPUT → eBUS WiFi Module ]
```

---

## Component List

- **Meanwell HDR-15-12** – Converts 230V AC to 12V DC (primary source)
- **Relay (12V DC, Normally Open)** – Closes only during blackout
- **Sealed Lead-Acid Battery 12V** – Backup power source
- **USB Step-Down Module 230V → 5V USB** – Active under normal power
- **USB Step-Down Module 12V → 5V USB** – Active only under blackout
- **Diodes & Capacitors** – For reverse current protection and filtering
- **WAGO 3-way terminals** – Distribution of power and logic
- **LED Indicators (optional):**
  - Blue → System ON
  - Green → Charging
  - Red → Battery Active (blackout)
  - White → Battery Full

---

## Logic Summary

- Under normal conditions, the eBUS module receives power via the 230V → 5V step-down.
- When the 230V input fails, the relay closes and switches to battery mode.
- The 12V battery feeds the 5V step-down via the relay.
- The system automatically returns to AC power when restored.
- No manual intervention or system restart required.

---

## Notes

- The USB-C output is connected directly to the eBUS Wi-Fi module.
- The battery is charged externally or via a smart charging module (not shown here).
- The relay coil is powered by the same 12V line from the Meanwell.
- Filtering capacitors are recommended on both step-down outputs.
- The DIN enclosure is vertical, 12 modules wide, and fully isolated.
