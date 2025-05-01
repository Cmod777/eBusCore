# DRC-60A Power Supply Test Plan (with UPS Function)

This document describes the test procedure for verifying correct operation of the **Mean Well DRC-60A** DIN rail AC-DC power supply using the **MESTEK CM83E** digital clamp multimeter.

## Terminals Overview

| Terminal    | Description                  |
|-------------|------------------------------|
| **L**       | AC Line Input (Phase)        |
| **N**       | AC Neutral Input             |
| **FG**      | Protective Earth (Ground)    |
| **+V**      | Positive DC Output           |
| **-V**      | Negative DC Output (GND)     |
| **Bat.+**   | Battery Positive             |
| **Bat.-**   | Battery Negative             |
| **AC OK**   | Relay Output – AC Status     |
| **Bat. Low**| Relay Output – Battery Low   |

## Multimeter Test Procedure (MESTEK CM83E)

### 1. DC Output Voltage (+V / -V)
- **Multimeter Mode:** DC Voltage (V⎓)
- **Red probe:** +V
- **Black probe:** -V
- **Expected Value:** ~13.8 V DC

---

### 2. Battery Charge Voltage (Bat.+ / Bat.-)
- **Multimeter Mode:** DC Voltage (V⎓)
- **Red probe:** Bat.+
- **Black probe:** Bat.-
- **Expected Value:** ~13.8 V DC (when battery is being charged)

---

### 3. AC OK Signal (Relay Contact)
- **Multimeter Mode:** Continuity Test (Beep / Diode symbol)
- **Probe 1:** AC OK
- **Probe 2:** -V
- **Expected Behavior:**
  - If AC is present: **Contact closed (Beep / 0Ω)**
  - If AC is lost: **Contact open (no beep / OL)**

---

### 4. Battery Low Signal (Relay Contact)
- **Multimeter Mode:** Continuity Test
- **Probe 1:** Bat. Low
- **Probe 2:** -V
- **Expected Behavior:**
  - Battery OK: **Contact open**
  - Battery <11 V: **Contact closed (Beep / 0Ω)**

---

## Test Results

1. DC Output Voltage:  
2. Battery Voltage:  
3. AC OK Relay Status:  
4. Battery Low Relay Status:

---
