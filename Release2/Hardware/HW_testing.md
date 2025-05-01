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
# Component: Yuasa NP7-12 Battery Test

### Specifications Summary
- **Nominal voltage**: 12 VDC
- **Full charge voltage**: 13.5 – 13.8 V (Float)
- **Charging current (standard)**: 2.1 A max (0.3 C)
- **Discharge cutoff voltage**: 10.5 V (recommended minimum)
- **Capacity**: 7.0 Ah @ 20h rate

### Required Tool
- MESTEK TRMS Digital Clamp Multimeter

### Test Procedure

#### 1. Voltage Check (No Load)
- **Mode**: DC Voltage (symbol: ⎓)
- **Red probe**: Battery positive terminal
- **Black probe**: Battery negative terminal
- **Expected result**: 
  - ≥ 12.6 V = fully charged
  - 12.0 – 12.5 V = medium charge
  - < 11.8 V = low charge

#### 2. Voltage Under Load
- **Connect** a 12 V load (e.g. 5–10 W resistor or fan)
- Repeat voltage measurement during operation
- **Expected**: Voltage should stay above **11.5 V**

#### 3. Current Draw (Optional)
- **Mode**: DC Current clamp (select A⎓)
- **Clamp around** one of the battery output wires (positive preferred)
- **Expected draw**: Depends on connected load; must not exceed safe discharge rate (~7 A continuous)

### Safety Note
- Avoid discharging below 10.5 V
- Recharge if voltage drops under 12.0 V when idle

---

### Test Results
1. Voltage (idle): 
2. Voltage (under load): 
3. Load current:

---
