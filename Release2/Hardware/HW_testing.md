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

# Component: Shelly Plus 1

### Specifications Summary
- **DC Supply Voltage**: 12VDC ±10%, or 24–48VDC stabilized
- **AC Supply Voltage**: 110–240V AC
- **Relay Output**: Dry contact (potential-free)
- **Max Load**: 16A / 240V AC
- **Operating Temperature**: -20°C to +40°C
- **Relevant Terminals (DC mode)**: 12V (positive), SW (GND/negative)

### Required Tool
- MESTEK TRMS Digital Clamp Multimeter

### Test Procedure

#### 1. Input Voltage (DC mode)
- **Mode**: DC Voltage (symbol: ⎓)
- **Red probe**: Terminal "12V"
- **Black probe**: Terminal "SW"
- **Expected**: 12.0–13.8 VDC

#### 2. Idle Current Draw
- **Mode**: DC Current clamp (symbol: A⎓)
- **Clamp around**: Positive wire feeding "12V"
- **Expected**: ~0.05–0.1 A (when idle, Wi-Fi on)

#### 3. Relay Output Test
- **Activate relay** via app or HTTP request
- **Check continuity** between output contacts (Normally Open closes)
- **Mode**: Continuity test (diode symbol or sound wave icon)
- **Probes**: Between relay output terminals
- **Expected**: Continuity when activated

---

### Test Results
1. Input voltage: 
2. Idle current: 
3. Relay continuity:

---

# Component: Shelly Plus Add-On

### Specifications Summary
- **Power Supply**: Provided directly via Shelly Plus 1 connector
- **Interface**: I²C or GPIO to main Shelly device
- **Supports**: DS18B20 temperature sensor, DHT22, analog inputs, binary sensors
- **Voltage Tolerance**: 0–3.3V (analog input)

### Required Tool
- MESTEK TRMS Digital Clamp Multimeter

### Test Procedure

#### 1. Supply Verification (when connected to Shelly Plus 1)
- **Mode**: DC Voltage (symbol: ⎓)
- **Red probe**: VCC or sensor pin (check with connected sensor)
- **Black probe**: GND of Add-On
- **Expected**: 3.3 VDC (provided by Shelly Plus 1)

#### 2. Analog Signal Input (Optional)
- **Connect** a known analog voltage source (e.g. 1.5V battery)
- **Measure** the voltage seen at input pin
- **Expected**: Should match within ±0.1V

#### 3. Sensor Bus Continuity
- **Mode**: Continuity test (diode or buzzer icon)
- **Check** signal/GND continuity from sensor to Add-On terminals
- **Expected**: Continuity present

---

### Test Results
1. VCC voltage: 
2. Analog input voltage: 
3. Sensor continuity:

---
# Component: Sunon EE40101S11000U999 Fan

### Specifications Summary
- **Rated Voltage**: 12 VDC
- **Power Consumption**: 0.99 W
- **Current Draw**: ~0.0825 A
- **Dimensions**: 40×40×10 mm
- **Airflow**: 13.9 m³/h
- **Speed**: 7300 RPM

### Required Tool
- MESTEK TRMS Digital Clamp Multimeter

### Test Procedure

#### 1. Voltage at Terminals
- **Mode**: DC Voltage (symbol: ⎓)
- **Red probe**: Fan positive terminal (usually red wire)
- **Black probe**: Fan negative terminal (usually black wire)
- **Expected**: 12.0 VDC ± 0.5 V

#### 2. Current Draw While Running
- **Mode**: DC Current clamp (select A⎓)
- **Clamp around** the positive wire while fan is active
- **Expected**: Approx. 80–90 mA

#### 3. Rotation & Noise
- **Observation**: Fan should spin immediately when powered
- **Expected**: Smooth spin, no grinding noise

---

### Test Results
1. Input voltage: 
2. Current draw: 
3. Mechanical rotation/noise:

---
# Component: TECNOIOT LM2596 Step-Down Converter

### Specifications Summary
- **Input Voltage Range**: 4–40 VDC
- **Output Voltage Range**: 1.25–37 VDC (adjustable)
- **Max Current**: ~2 A continuous (with heatsink)
- **Display**: Integrated digital voltmeter

### Required Tool
- MESTEK TRMS Digital Clamp Multimeter
- Small flathead screwdriver (for trimmer)

### Test Procedure

#### 1. Input Voltage Check
- **Mode**: DC Voltage (⎓)
- **Red probe**: VIN+
- **Black probe**: VIN−
- **Expected**: 13.8 V (from battery or main power line)

#### 2. Output Voltage Adjustment
- **Mode**: DC Voltage (⎓)
- **Red probe**: VOUT+
- **Black probe**: VOUT−
- Use screwdriver to rotate trimmer until output reads exactly **12.00–12.10 V**
- **Important**: Confirm value using external multimeter if display is damaged

#### 3. Output Load Test (Optional)
- Connect load (e.g. 12 V fan)
- Confirm voltage remains stable under load

### Safety Note
- Ensure input > output voltage
- Avoid shorting output when powered
- Watch for excessive heat if drawing >1 A continuously

---

### Test Results
1. Input voltage: 
2. Output voltage: 
3. Load test result:

---
# Component: DollaTek W1209 Temperature Controller

### Specifications Summary
- **Operating voltage**: 12 VDC
- **Temperature range**: -50 °C to 110 °C
- **Sensor type**: NTC thermistor probe
- **Relay rating**: 10 A @ 12 VDC
- **Output type**: Relay NO/NC terminals

### Required Tool
- MESTEK TRMS Digital Clamp Multimeter
- 12 VDC regulated power source
- Heat source (e.g. hair dryer) or cold source (ice)

### Test Procedure

#### 1. Power Supply Test
- **Mode**: DC Voltage (⎓)
- **Red probe**: VCC (marked on module input)
- **Black probe**: GND
- **Expected**: 12.0 – 12.1 VDC

#### 2. Display and Sensor Response
- Power the board with 12 V
- Ensure screen lights up and shows ambient temperature
- Hold sensor between fingers, temperature should rise
- Touch probe with ice or cold metal, temperature should drop
- **Expected**: Variation of at least ±5°C in response to thermal stimulus

#### 3. Relay Activation Test
- Set threshold temperature on board (use onboard buttons)
- Heat or cool probe past threshold
- **Expected**: Audible click + relay LED changes state
- **Check output**: Measure continuity on output terminals when relay is active

#### 4. Output Voltage Test (Optional)
- **Mode**: DC Voltage (⎓)
- **Red probe**: Relay output terminal
- **Black probe**: GND
- Confirm if output switches correctly when relay toggles

### Safety Note
- Relay should only be connected to appropriate load during final installation
- Ensure temperature thresholds are correctly set for activation

---

### Test Results
1. Input voltage:  
2. Sensor variation observed:  
3. Relay toggled (Y/N):  
4. Output switching OK (Y/N):

---
# Component: Finder 553490120040 Relay + Finder 94.74 Socket

### Specifications Summary
- **Coil voltage**: 12 VDC
- **Contacts**: 4 changeover (4RT / DPDT)
- **Max switching current**: 7 A per contact
- **Socket model**: Finder 94.74 (screw terminals)
- **Test button**: Manual test button included

### Required Tool
- MESTEK TRMS Digital Clamp Multimeter

### Test Procedure

#### 1. Coil Voltage Test
- **Mode**: DC Voltage (symbol: ⎓)
- **Red probe**: Connected to coil terminal A1 (on socket)
- **Black probe**: Connected to coil terminal A2 (on socket)
- **Apply 12 VDC**
- **Expected result**: 11.8 – 12.2 V across A1–A2

#### 2. Coil Activation Confirmation
- Listen for a **distinct click** when 12 V is applied
- **Optional**: Use **NCV mode** or visual indicator (relay LED or button)

#### 3. Contact Continuity Test
- **Mode**: Continuity (symbol: soundwave/beep or diode)
- **Probes**: 
  - NO (Normally Open) contact pair (e.g. terminal 11–14)
  - Apply 12 VDC to A1–A2
  - Check continuity: should **close** the circuit (beep)
- **Without power**: contacts should be **open** (no beep)

#### 4. Manual Test Button
- Push the **test button** on top of the relay
- Check if contact continuity behaves **as if energized**

### Safety Note
- Test with low-voltage DC **only** unless fully isolated
- Ensure correct polarity on coil terminals (A1 = + / A2 = −)

---

### Test Results
1. Coil voltage:
2. Relay click (audible):
3. NO contacts closed when powered:
4. Manual test button working:

---
# Component: Gewiss GW90025 Circuit Breaker Test

### Specifications Summary
- **Type**: Magnetothermic circuit breaker
- **Poles**: 1P+N
- **Rated voltage**: 230 V AC
- **Rated current**: Typically 10–25 A (verify your specific model)
- **Breaking capacity**: 4.5 – 6 kA (depends on variant)
- **Function**: Automatically cuts power in case of overload or short-circuit

### Required Tool
- MESTEK TRMS Digital Clamp Multimeter

### Test Procedure

#### 1. Continuity Test (Breaker ON)
- **Mode**: Continuity (symbol: sound wave or diode)
- **Red probe**: Connect to input terminal (L)
- **Black probe**: Connect to output terminal (L out)
- **Expected result**: Audible beep or 0 Ω (closed circuit)

#### 2. Continuity Test (Breaker OFF)
- Toggle switch to OFF
- **Expected result**: No beep / OL (open circuit)

#### 3. Voltage Test (Live Test, Caution!)
- **Power required**: 230 V AC
- **Mode**: AC Voltage
- **Red probe**: Input terminal (L)
- **Black probe**: Neutral terminal (N)
- **Expected input**: ~230 V
- **Then test**: Red probe on output terminal (L out), same black probe on N
- **Expected output**: ~230 V if ON, 0 V if OFF

### Safety Note
- Always test with appropriate personal protection
- Do not touch live wires with bare hands

---

### Test Results
1. Continuity (ON):  
2. Continuity (OFF):  
3. Voltage IN/OUT:

---
# Component: DEWIN 20A DC Circuit Breaker Test

### Specifications Summary
- **Type**: DC Magnetothermal Breaker
- **Rated current**: 20 A
- **Operating voltage**: 12V – 250V DC
- **Poles**: Single pole
- **Function**: Protects DC circuits from overcurrent or short-circuit

### Required Tool
- MESTEK TRMS Digital Clamp Multimeter

### Test Procedure

#### 1. Continuity Test (Breaker ON)
- **Mode**: Continuity (symbol: sound wave or diode)
- **Red probe**: Input terminal (DC+)
- **Black probe**: Output terminal (DC+ out)
- **Expected result**: Beep or ~0 Ω (circuit closed)

#### 2. Continuity Test (Breaker OFF)
- Toggle switch to OFF
- **Expected result**: No beep / OL (circuit open)

#### 3. Voltage Test (Live Test, Caution!)
- **Power required**: 13.8 V DC (or your system voltage)
- **Mode**: DC Voltage
- **Red probe**: Input terminal
- **Black probe**: GND
- **Expected input**: ~13.8 V
- **Then test**: Red probe on output terminal, same black probe
- **Expected output**: ~13.8 V if ON, 0 V if OFF

### Safety Note
- Never exceed rated voltage or current
- Use only in DC circuits — not for AC systems

---

### Test Results
1. Continuity (ON):  
2. Continuity (OFF):  
3. Voltage IN/OUT:

---
# Component: CABLEPELADO Bipolar Female Plug Test

### Specifications Summary
- **Type**: Bipolar straight female plug
- **Max current**: 10 A
- **Max voltage**: 250 V AC
- **Protection**: IP20 (no grounding)
- **Application**: AC 230 V plug for Raspberry official PSU or general appliances

### Required Tool
- MESTEK TRMS Digital Clamp Multimeter

### Test Procedure

#### 1. Continuity Check
- **Mode**: Continuity (symbol: sound wave / diode)
- **Red probe**: Insert into one terminal of the plug
- **Black probe**: Touch corresponding internal wiring or device plug pin
- **Expected result**: Multimeter beeps = internal contact is intact

#### 2. Resistance Check
- **Mode**: Ohms (symbol: Ω)
- Measure resistance across each conductor
- **Expected**: ~0 Ω or a very low value (cable + contact resistance)

#### 3. Voltage Output (Live Test, optional if powered)
- **Mode**: AC Voltage (symbol: ~V)
- **Red probe**: L (Live)
- **Black probe**: N (Neutral)
- **Expected result**: ~230 V AC (only if connected to live power source)

### Safety Note
- Never insert probes while plug is connected to the grid unless explicitly testing live voltage
- Always handle insulated parts during live measurements

---

### Test Results
1. Continuity:
2. Resistance:
3. Voltage output (if tested):

---
# Component: HERKINDNESS DIN Rail Fuse Holder

### Specifications Summary
- **Voltage rating**: Up to 250 V AC
- **Fuse type**: 5x20 mm glass or ceramic
- **Max current**: Based on inserted fuse rating (typically up to 10 A)
- **DIN rail mount**: Yes, standard 35 mm
- **Usage**: General inline AC protection for circuits up to 250 V

### Required Tool
- MESTEK TRMS Digital Clamp Multimeter

### Test Procedure

#### 1. Continuity Check (Without Power)
- **Mode**: Continuity / Ohm test (symbol: Ω or sound wave)
- **Red probe**: One terminal of fuse holder
- **Black probe**: Opposite terminal (other side of fuse)
- **Expected result**: 
  - Audible beep or ~0 Ω if fuse is intact
  - OL or no beep = blown fuse or bad contact

#### 2. Voltage Pass-Through Test (When powered)
- **Mode**: AC Voltage (symbol: V~)
- **Red probe**: Input terminal (from mains or breaker)
- **Black probe**: Output terminal (load side)
- **Expected result**: 
  - Voltage reading should match input AC (typically ~230 V)
  - 0 V = open fuse or incorrect wiring

### Safety Note
- Always **test with power off first**
- Ensure proper fuse rating before applying power
- Do not exceed rated fuse current

---

### Test Results
1. Continuity (unpowered): 
2. Voltage across terminals (powered):

---
# Component: Gewiss GW90025 - Circuit Breaker Test

### Specifications Summary
- **Type**: Automatic Circuit Breaker (MCB)
- **Rated current**: 16 A
- **Voltage rating**: 230/400 V AC
- **Breaking capacity**: 4.5 kA
- **Poles**: 1P+N
- **Trip curve**: C

### Required Tool
- MESTEK TRMS Digital Clamp Multimeter

### Test Procedure

#### 1. Continuity Test (Breaker ON)
- **Mode**: Continuity (symbol: sound wave or diode symbol)
- **Red probe**: Output terminal of breaker
- **Black probe**: Input terminal of breaker
- **Expected result**: Continuity **should beep** when breaker is ON

#### 2. Open Test (Breaker OFF)
- Switch breaker to OFF
- Repeat continuity test
- **Expected result**: **No beep** (open circuit)

#### 3. Voltage Drop Check
- **Mode**: AC Voltage
- **Red probe**: Output terminal
- **Black probe**: Input terminal
- **Breaker ON and under light load**
- **Expected result**: Voltage drop should be near **0 V**

#### 4. Load Voltage Test
- **Red probe**: Output terminal (while connected to AC source and load)
- **Black probe**: Neutral line
- **Expected result**: ~230 V (if powered and breaker is ON)

### Safety Note
- Ensure power is OFF before performing continuity tests
- Do not exceed rated current during testing

---

### Test Results
1. Continuity (ON): 
2. Continuity (OFF): 
3. Voltage drop: 
4. Load voltage:

---
# Component: Bauer DC-DC 8V–32V to 5V USB-C Converter

### Specifications Summary
- **Input Voltage Range**: 8 – 32 VDC
- **Output Voltage**: 5 VDC (regulated)
- **Output Current**: Max 3 A (15 W)
- **Connector**: USB-C output
- **Use case**: Powers low-consumption 5V devices (e.g., eBus Wi-Fi module)

### Required Tool
- MESTEK TRMS Digital Clamp Multimeter

### Test Procedure

#### 1. Input Voltage Test
- **Mode**: DC Voltage (⎓)
- **Red probe**: Positive input terminal (VIN+)
- **Black probe**: Ground input terminal (VIN-)
- **Expected**: Voltage within **8–32 V**, typically **13.8 V**

#### 2. Output Voltage Test
- **Mode**: DC Voltage (⎓)
- **Red probe**: Inserted in USB-C VBUS line via breakout/test cable
- **Black probe**: USB-C GND
- **Expected**: **5.0 – 5.1 VDC**

#### 3. Load Regulation Test (Optional)
- **Connect** 5V load (e.g., Wi-Fi module or resistive dummy load)
- Measure output again under load
- **Expected**: Output remains **5.0 V ±0.1 V**

### Safety Notes
- Ensure proper polarity on input lines
- USB-C port must not be shorted
- Avoid exceeding 3 A current draw

---

### Test Results
1. Input voltage: 
2. Output voltage (idle): 
3. Output voltage (under load):

---
