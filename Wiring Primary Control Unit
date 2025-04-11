# Wiring Details – Module 1 (Primary Control Unit)

This section describes in detail the wiring layout for the primary control unit, including all connections, relays, power lines, and signal routing.

---

## 1. Power Input

```
[230V AC SUPPLY] 
     |
     +--→ L (Live)  → Meanwell HDR-15-12 (L)
     +--→ N (Neutral) → Meanwell HDR-15-12 (N)
     +--→ PE (Ground) → DIN Rail / Earth block
```

---

## 2. 12V DC Distribution (from Meanwell)

```
[Meanwell HDR-15-12] → Output: 12V DC

     +--→ V+ to:
     |     - Finder Relay (A1)
     |     - Shelly "AF" (12V IN)
     |     - Shelly "TADO" (12V IN)
     |     - Power LED (anode +)
     |
     +--→ V− (GND) to:
           - Finder Relay (A2)
           - Shelly "AF" (GND)
           - Shelly "TADO" (GND)
           - Power LED (cathode −)
```

**WAGO Terminals:**

- **WAGO #1 (V+)** → distributes 12V+ to all devices
- **WAGO #2 (GND)** → common ground for all devices

---

## 3. Relay Wiring (Finder 40.52 – DPDT 12V DC)

### Coil
```
A1 ← 12V+ from Meanwell (via WAGO #1)
A2 ← GND from Meanwell (via WAGO #2)
```

### Contact 1 – OT BUS+
```
COM1 ← OT BUS+ from Tado
NO1  → OT BUS+ to Boiler
```

### Contact 2 – OT BUS−
```
COM2 ← OT BUS− from Tado
NO2  → OT BUS− to Boiler
```

**WAGO Terminals:**

- **WAGO #3** → OT BUS+ split between Tado and relay COM1
- **WAGO #4** → OT BUS− split between Tado and relay COM2

---

## 4. Shelly "AF"

- **Power:**  
  - 12V IN from WAGO #1 (V+)  
  - GND from WAGO #2  
- **Relay Output (dry contact):**  
  - Controls the Finder relay A1/A2 circuit

Used to disconnect OT communication when OFF.

---

## 5. Shelly "TADO"

- **Power:**  
  - 12V IN from WAGO #1 (V+)  
  - GND from WAGO #2  
- **Relay Output (230V AC):**  
  - Powers Tado thermostat directly

Provides hard power control for Tado.

---

## 6. Power ON LED (Blue)

- **Anode (+)** → 12V from WAGO #1  
- **Cathode (−)** → GND from WAGO #2  
- Can include inline resistor (~330Ω)

---

## 7. Output Lines

- **EXIT 1 → Tado Unit:**
  - 230V AC (controlled by Shelly "TADO")
  - OT BUS+ and BUS− to relay COM1/COM2

- **EXIT 2 → Boiler:**
  - OT BUS+ and BUS− from relay NO1/NO2

- **EXIT 3 → Main Panel:**
  - Optional 230V AC passthrough or service line

---

## Optional Notes

- Cables should be labeled and color-coded:
  - **Red** = V+, **Black** = GND, **Yellow** = BUS+
  - **Blue** = BUS−, **White** = OT communication
- All wires are secured using WAGO 3-way terminals.
- DIN rail includes fuse holders for 230V input.
- LED status can be expanded for relay or Shelly monitoring.
