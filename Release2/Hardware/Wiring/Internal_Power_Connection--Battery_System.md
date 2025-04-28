# Section 1: Internal Power Connection - Battery System

## 1.1 Overview

The initial internal wiring stage concerns the safe and structured connection of the 230V AC incoming line and the integration of the backup battery system into the Mean Well DC-UPS module.

All incoming AC cables and battery wiring have been dimensioned and protected following best practices for reliability, serviceability, and future expansion.

## 1.2 AC Power Input

- The external 230V connection enters the enclosure via a rapid-disconnect IP-rated connector.
- Inside the enclosure:
  - **Neutral (N)** and **Protective Earth (PE)** are directly connected to an internal WAGO quick-release terminal block using 2.5 mm² cables.
  - **Phase (L)** is first routed through a **GEWISS** magnetothermal circuit breaker (datasheet reference [here](https://github.com/Cmod777/eBusCore/blob/main/datasheets/internal/power/product.datasheet.1000001.1000061.GW90025.pdf)).
  - After protection, the Phase line enters the WAGO terminal block.

> **Important:**  
> All AC cables entering the enclosure are initially dimensioned at **2.5 mm²** for safety and robustness.  
> After protection by the GEWISS circuit breaker, downstream cabling may be reduced to **1.3 mm²** if the distance is less than 1 meter, ensuring optimal flexibility without compromising safety.

## 1.3 Mean Well DC-UPS Module Input

From the WAGO terminal block:
- **Phase (protected)**, **Neutral**, and **Earth** are routed to the input side (L/N/PE) of the Mean Well module.
- This completes the 230V AC input circuit.

## 1.4 Battery Wiring

- The battery outputs **BAT+** and **BAT-** are connected to the corresponding inputs on the Mean Well DC-UPS.

Wiring details:
- **BAT+**:
  - Connected from the battery positive terminal to a **5A fast-blow fuse**.
  - From the fuse, connected to a **manual cutoff switch**.
  - From the switch, finally connected to the **BAT+ input** of the Mean Well module.
  - All connections use **1.3 mm² (16AWG)** red silicone-insulated cable.
- **BAT-**:
  - Direct connection from the battery negative terminal to the **BAT- input** of the Mean Well module.
  - Using **1.3 mm² (16AWG)** black silicone-insulated cable.

> **Important:**  
> The 5A fuse is placed **after the battery** and **before the switch** to ensure immediate overcurrent protection, preserving battery integrity and system safety.

## 1.5 Additional Recommendations

> **Physical Cable Protection:**  
> All internal wiring, especially 230V AC lines, must be mechanically protected using appropriate conduits, sleeves, or cable ties to prevent damage from vibrations, abrasion, or accidental impacts.

> **Cable Stripping Guidelines:**  
> Strip only the minimum required length of insulation on each wire to ensure a secure fit in terminal blocks and to minimize the risk of accidental short circuits.

> **Maintenance Advisory:**  
> The 5A fast-blow fuse protecting the battery positive line should be positioned for easy access to allow replacement during future maintenance operations without disassembling critical parts of the system.

> **Breaker Orientation Note:**  
> The GEWISS circuit breaker should be installed in the correct orientation, with proper Phase and Neutral alignment, to ensure optimal mechanical and electrical performance according to the manufacturer's specifications.

## 1.6 Summary Table

| Item | Cable Type | Protection | Notes |
|:---|:---|:---|:---|
| AC Incoming (Phase, Neutral, Earth) | 3G 2.5 mm² | Phase protected by GEWISS circuit breaker | |
| AC Internal Branches | 1.3 mm² (if < 1m after protection) | - | Optional section reduction |
| Battery Positive (BAT+) | 1.3 mm² (16AWG) Red Silicone | 5A Fuse + Manual Switch | |
| Battery Negative (BAT-) | 1.3 mm² (16AWG) Black Silicone | - | Direct connection |

---


# Section 1 - Wiring Diagram (Electrical ASCII Version)

```plaintext
┌──────────────────────────────┐
│   230V External Connector    │
└────────────┬─────────────────┘
             │
      ┌──────┴──────┐
      │             │
┌─────▼─────┐ ┌─────▼─────┐
│   Earth   │ │  Neutral  │
└─────┬─────┘ └─────┬─────┘
      │             │
  ┌───▼───┐     ┌───▼───┐
  │ WAGO  │     │ WAGO  │
  └───────┘     └───────┘
                   │
                   │
                ┌──▼──┐
                │Mean │
                │Well │
                │ (PE)│
                └─────┘
                   │
             [AC SIDE]

────────────────────────────────────────────────────

┌────────────┐
│  Phase (L) │
└─────┬──────┘
      │
┌─────▼──────┐
│  Breaker   │
│   [B]      │ (GEWISS)
└─────┬──────┘
      │
  ┌───▼───┐
  │ WAGO  │
  └───┬───┘
      │
      │
  ┌───▼───────┐
  │ Mean Well │
  │ (L/N AC)  │
  └───────────┘

────────────────────────────────────────────────────

             [DC SIDE - Battery Wiring]

┌────────────┐       ┌────────────┐
│  BAT+      │       │  BAT-      │
│ (Battery)  │       │ (Battery)  │
└─────┬──────┘       └─────┬──────┘
      │                   │
┌─────▼─────┐           ┌──▼────────────┐
│   Fuse    │           │  Mean Well    │
│   [F]     │ (5A)      │ (BAT- Input)  │
└─────┬─────┘           └───────────────┘
      │
┌─────▼─────┐
│  Switch   │
│   [S]     │
└─────┬─────┘
      │
┌─────▼─────┐
│  Mean Well│
│ (BAT+ In) │
└───────────┘


---

# Notes:

- `[B] = Breaker (GEWISS magnetothermal breaker)`  
- `[F] = Fuse (5A fast-blow fuse on battery positive line)`  
- `[S] = Manual Switch (battery positive line disconnection)`  
- **AC Side**: Earth and Neutral connect directly to WAGO; Phase passes through breaker first.
- **DC Side**: Battery Positive (BAT+) goes through Fuse and Switch before reaching Mean Well; Battery Negative (BAT-) connects directly.
- **Cable sizes**:
  - 230V lines: 2.5 mm² before breaker.
  - 1.3 mm² allowed after protection (short distances <1m).
  - Battery lines: 1.3 mm² (16AWG) silicone insulated.

---
