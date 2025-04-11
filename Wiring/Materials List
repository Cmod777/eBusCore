# Materials List – Complete System (Centralina IP65 + UPS)

This document includes all components used in the dual-module system:  
Primary Control Unit + UPS Backup Unit.

---

## 1. DIN Rail Components

| Qty | Component                            | Model / Spec                         | Notes                             |
|-----|--------------------------------------|--------------------------------------|-----------------------------------|
| 2   | Power Supply 12V DC                  | Meanwell HDR-15-12                   | DIN mount, 230V AC → 12V DC       |
| 2   | Relay DPDT 12V DC                    | Finder 40.52.9.012.0000              | DIN socket (95.05) or soldered    |
| 2   | Shelly Plus 1 Mini                   | Shelly (12V DC version)              | DIN clip required                 |
| 1   | DIN Mini Circuit Breaker             | 2A C-Curve 1P                        | Protects Meanwell input           |
| 1   | Residual current circuit breaker     | 2P 16A 30mA                          | For 230V main protection          |

---

## 2. UPS Components

| Qty | Component                            | Model / Spec                         | Notes                             |
|-----|--------------------------------------|--------------------------------------|-----------------------------------|
| 1   | Sealed Lead-Acid Battery             | Yuasa 12V 1.2Ah (97x43x52mm)         | Backup power                      |
| 1   | Step-down Converter 12V → 5V         | Bauer USB-C 15W                      | Battery to USB-C                  |
| 1   | Step-down Converter 230V → 5V        | Bauer USB-C 15W                      | Grid to USB-C                     |
| 2   | Diode Schottky                       | 1N5822                               | To isolate USB-C outputs          |

---

## 3. Indicators (LED)

| Qty | LED Color | Function               | Notes                     |
|-----|-----------|------------------------|---------------------------|
| 1   | Blue      | Power ON               | 330Ω resistor required    |
| 1   | Red       | Battery in use         | Triggered via relay path  |
| 1   | Green     | Charging (optional)    | Depends on charger module |
| 1   | White     | Battery full (optional)| Logic-controlled          |

---

## 4. Terminals and Wiring

| Qty | Component                     | Model / Spec                 | Notes                             |
|-----|-------------------------------|------------------------------|-----------------------------------|
| 10+ | WAGO 221-413                  | 3-way lever connector        | Used for all V+, GND, BUS lines   |
| 3   | Exit Cable Gland + Clamp      | M20 + strain relief          | EXIT 1 / EXIT 2 / EXIT 3          |
| 1   | USB-C panel port              | USB-C female to screw terminal| eBUS output                       |

---

## 5. Wire (Recommended)

| Type            | Color      | Section     | Use                              |
|------------------|------------|-------------|----------------------------------|
| H05V-K           | Red        | 0.5–1.0 mm² | 12V+, battery V+                 |
| H05V-K           | Black      | 0.5–1.0 mm² | GND                              |
| H05V-K           | Yellow     | 0.5 mm²     | OT BUS+                          |
| H05V-K           | Light Blue | 0.5 mm²     | OT BUS−                          |
| H05V-K           | Brown      | 1.0–1.5 mm² | 230V Line                        |
| H05V-K           | Blue       | 1.0–1.5 mm² | 230V Neutral                     |
| H07V-K           | Green/Yellow | 1.5–2.5 mm² | Earth/Ground                    |

---

## 6. Fasteners & Accessories

| Qty | Component               | Description                         |
|-----|-------------------------|-------------------------------------|
| –   | Self-tapping screws     | For DIN rails and supports          |
| –   | DIN rail mounting clips | For Shelly and LED bases            |
| –   | Heat shrink tubing      | For LED and diode protection        |
| –   | Adhesive cable tags     | Labeling WAGO, exits, wiring        |

---

## 7. Optional / Diagnostic

| Qty | Component           | Purpose                     |
|-----|---------------------|-----------------------------|
| 1   | ESP32 or ESP8266    | Battery voltage monitor     |
| 1   | Volt/Current meter  | For diagnostics             |

---

**Note:**  
All cables must be dimensioned according to their real path length and current.  
DIN case assumed: **IP65, 12 modules, vertical**.
