# UPS Module v3.0 – Logical Filters Specification

## Overview

This document outlines the logical filters implemented in the UPS Module v3.0. Each filter is designed to manage specific operational conditions, ensuring proper functionality and protection of the system components.8

---

## Filter 1: Battery Charging Indicator Logic

**Purpose:** 445-2Indicates when the battery is actively charging. 12

**Implementation:**

- **Input:** 563-2Voltage present after the PTC fuse and Schottky diode in the charging path. 16
- **Output:** 677-1Activates LED2 (Battery Charging Indicator). 20
- **Logic:** 739-1LED2 is ON when voltage is present at the charging path, indicating active charging. 24

**Notes:**

- 840-1Ensure the voltage drop across the diode is considered to prevent false indications. 28
- 943-0Use a pull-down resistor to avoid floating states when charging is inactive. 32

---

## Filter 2: UPS Active State Logic

**Purpose:** 1025-2Indicates when the UPS is supplying power due to grid failure. 36

**Implementation:**

- **Input:** 1147-2Voltage present at the output of the battery switch (i.e., when the UPS is active). 40
- **Output:** 1269-1Activates LED3 (UPS Active Indicator). 44
- **Logic:** 1325-1LED3 is ON when the battery is supplying power to the load, indicating UPS activation. 48

**Notes:**

- 1428-1Ensure the switch is properly debounced to prevent flickering of the LED. 52
- 1520-0Consider using a transistor buffer if the LED load affects the control logic. 56

---

## Filter 3: WiFi Module Power Indicator Logic

**Purpose:** 1603-2Indicates when the WiFi module is receiving filtered 5V power. 60

**Implementation:**

- **Input:** 1736-2Voltage present after the filtering stage (capacitors and diode) supplying the WiFi module. 64
- **Output:** Activates LED4 (WiFi Ready Indicator).67
- **Logic:** LED4 is ON when the filtered 5V is available, indicating the WiFi module is powered.70

**Notes:**

- Use low ESR capacitors in the filter to ensure stable voltage supply.73
- The diode prevents backflow; ensure its forward voltage drop is suitable for the LED operation.76

---

## Filter 4: Battery Full / Standby Indicator Logic

**Purpose:** Indicates when the battery is fully charged and the system is in standby mode.79

**Implementation:**

- **Inputs:** Inverted signals from Filter 1 (Battery Charging) and Filter 2 (UPS Active).82
- **Output:** Activates LED5 (Battery Full / Standby Indicator).85
- **Logic:** LED5 is ON only when both LED2 and LED3 are OFF, indicating no charging and UPS is inactive.88

**Circuit Example:**

- Use a dual-input NOR gate (e.g., 74HC02) with inputs connected to the outputs of Filter 1 and Filter 2.91
- The output of the NOR gate drives LED5 through a current-limiting resistor.94

**Notes:**

- Ensure proper logic level compatibility between the filters and the NOR gate.97
- Consider adding hysteresis to prevent LED5 from flickering during transition states.100

---

## General Considerations

- All LEDs should be connected with appropriate current-limiting resistors to prevent overcurrent.103
- Ensure all logic levels are compatible across different filters to maintain system integrity.106
- Test each filter individually during commissioning to verify correct operation.109

---

By implementing these logical filters, the UPS Module v3.0 provides clear and reliable indicators for system status, enhancing user awareness and system diagnostics.112
