# Emergency Cooling System – Assembly and Test Report

## System Overview

This module provides an **intelligent emergency override** for the active cooling system, using a **Shelly Plus Add-On** to bypass the W1209 in case of malfunction or crash.  
The system monitors temperature independently and ensures fan activation even when the primary controller fails.

---

## Logical Circuit Name
`EmergencyCoolingShelly v1.0`

---

## Materials Used

| Component | Description |
|:----------|:------------|
| Shelly Plus 1 + Add-On | Smart controller with digital I/O and 1-wire probe support |
| Sunon Fans EE40101S1 | 12V, 7300 RPM, 0.99W axial fans |
| Diodo Schottky 1N5819 | Output protection to K1-NO (W1209) |
| Cavi rosso/nero 0.8 mm² | Power and control lines |
| WAGO blocks | Power distribution for 12V+, GND, and logic branches |
| Sonde DS18B20 | High/Low zone thermal probes for Add-On |
| Heat-shrink/RTV silicone | Protection for soldered diodes and critical joints |

---

## Functional Overview

1. **Dual temperature monitoring**:
   - Two DS18B20 probes on the Shelly Add-On:
     - **High zone**: top of enclosure (heat accumulation).
     - **Low zone**: bottom (cool air intake).
   - Allows differential logic and redundancy.

2. **Input logic (pin I)**:
   - Connected to a **shared 12V+ node** supplied by both:
     - **OUT+ of LM2596 step-down**.
     - **V+ of W1209**.
   - If one module fails, the other maintains the signal.
   - Already protected by upstream fuses – **no extra diode needed**.

3. **Output logic (pin O)**:
   - Connected to **K1–NO terminal of W1209** via a **Schottky diode 1N5819**.
   - Prevents reverse current into W1209 in case of damage.
   - When triggered, Shelly closes this path, forcing 12V onto the fan line.

4. **Failure override logic**:
   - If W1209 relay fails (no contact K0–K1), Shelly Add-On acts as backup.
   - Based on sensor readings or scripted logic (e.g. delta T, timer, fixed thresholds).

5. **Complete redundancy**:
   - Shared power and GND for all 12V logic (isolated from 13.8V).
   - Smart decision-making via Home Assistant, script, or standalone config.

---

## ASCII Diagram

```plaintext
            ┌────────────┐
            │  W1209     │
            │ K0   K1    │
            │  │    │    │
12V+  ◄─────┘  │    │────┐
               │    ▼    │
           [VENTOLA +12V]◄────┐
               ▲    ▲         │
               │    │         │
           Shelly O │         │
              [D]   │         │
               │    │         │
               └────┴─────────┘
                  Shared GND

[D] = Diodo Schottky 1N5819
```

---

## Emergency Logic Notes

- **Input pin I** is safely shared from W1209 and LM2596.  
  Failure of one does **not** stop Shelly Add-On from functioning.
- **Output pin O** does **not control W1209**, but **injects 12V** into the vent line when W1209 fails to trigger it.
- W1209 mechanical failure = Shelly takes over fan activation.

---

## Safety Layers

| Component | Protection |
|:----------|:-----------|
| MF-R020, MF-R050 | Fuse per module (already in upstream branches) |
| 1N5819 diode | Reverse current blocking (Shelly → W1209 relay) |
| Scripted failover | Add-On can trigger based on time, delta-T, or conditions |

---

## Best Practices

- Use **dedicated WAGO blocks** to distribute 12V+ and GND to Add-On, LM2596, and W1209.
- Mount thermal probes firmly but **without metal contact**; use heat-shrink tubing or foam for stable ambient readings.
- Test the Shelly logic separately (simulate W1209 failure by disconnecting K0–K1).
- Document your logic in Home Assistant or Shelly Web UI for traceability.

---

## Tests Performed

| Test | Result |
|:-----|:-------|
| Sensor accuracy | DS18B20 working, delta-T tracked |
| 12V continuity | Maintained if either source is active |
| Reverse protection | Diode blocks backflow to W1209 |
| Emergency trigger | Fans activate when W1209 fails |
| Logic stability | No false triggers, script logs OK |

---

## Final Considerations

- This system ensures **critical thermal protection** even under partial system failure.
- Provides **advanced automation** beyond the capabilities of basic thermostats.
- Can be expanded with additional actions: alarms, MQTT, energy logging.

---

## Licensing Notice

All original photographs, electrical schematics, and technical drawings created by the author are licensed under:

**Creative Commons Attribution - NonCommercial - NoDerivatives 4.0 International (CC BY-NC-ND 4.0)**

Under this license:
- Copying, sharing, and redistribution of the material are allowed, provided that proper attribution is given to the original author (Cmod777).
- Commercial use is strictly prohibited.
- No modifications, transformations, or derivative works are allowed.

For full license details, refer to: [https://creativecommons.org/licenses/by-nc-nd/4.0/](https://creativecommons.org/licenses/by-nc-nd/4.0/)

---
