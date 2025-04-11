# Wiring Details – Module 2 (UPS Backup Unit)

This section describes in detail the wiring layout for the backup UPS control unit, which provides automatic power to the eBUS Wi-Fi module in case of a blackout.

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
     |     - Relay Coil (Normally Open)
     |     - LED Power ON (optional)
     |
     +--→ V− (GND) to:
           - Relay Coil (GND)
           - LED Power ON (GND)
```

**WAGO Terminals:**

- **WAGO #1 (V+)** → 12V+ to relay, LED
- **WAGO #2 (GND)** → GND shared

---

## 3. Relay Wiring (Blackout Logic)

- **Relay type:** SPST Normally Open (12V DC coil)
- Relay is **open** when 230V is present  
  → eBUS is powered from grid

- Relay is **closed** when 230V fails  
  → switches to battery backup

### Coil
```
A1 ← 12V+ from Meanwell (via WAGO #1)
A2 ← GND from Meanwell (via WAGO #2)
```

### Contact
```
COM  ← Battery 12V (+)
NO   → Input of 12V → 5V USB Step-Down
```

**WAGO Terminals:**

- **WAGO #3** → Battery 12V distribution
- **WAGO #4** → GND from battery

---

## 4. Battery Block

- **Type:** Sealed Lead-Acid 12V  
- **Connected to:**  
  - COM of relay (positive)  
  - WAGO #3 (positive)  
  - WAGO #4 (GND)

Battery powers the eBUS module when 230V fails.

---

## 5. Step-Down Modules

### A. Normal Operation (grid active)

```
230V AC → Step-Down Module → 5V USB
        |
        +--→ USB-C → eBUS Wi-Fi module
```

### B. Blackout Operation (via relay)

```
Battery 12V → Relay → Step-Down → 5V USB
                           |
                           +--→ USB-C → eBUS Wi-Fi module
```

---

## 6. USB-C Output

- Final output to eBUS Wi-Fi module
- Routed through both step-down modules
- Only one source active at a time:
  - Grid (default)
  - Battery (fallback)

---

## 7. LED Indicators (Optional)

- **Blue** → System powered
- **Green** → Battery charging
- **Red** → Running on battery
- **White** → Battery fully charged

Each LED wired through a resistor and WAGO:

- **WAGO #5** → LED V+ line
- **WAGO #6** → Common GND

---

## Notes

- Relay switches automatically with power loss.
- USB-C power is uninterrupted during the transition.
- It’s recommended to include diodes to prevent reverse current.
- Step-down modules should be filtered with capacitors.
- WAGO terminals used for all major distribution branches.
- DIN enclosure is vertical, 12 DIN-modules width.
