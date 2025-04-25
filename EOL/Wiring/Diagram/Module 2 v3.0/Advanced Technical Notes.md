# UPS Module v3.0 – Advanced Technical Notes

## 1. Thermal Protection and Safety

### Passive / Active Temperature Monitoring

Although the core UPS design does not include default thermal monitoring, the following are recommended:

- **Sensor:** Add a DS18B20 or NTC near the battery and relay.
- **Logic:** If battery temperature > 50°C, disable charging or UPS output via automation (relay cut-off or Shelly).
- **Optional Add-on:** Integrate with Shelly Plus Add-On using temperature probe for Home Assistant integration.

---

## 2. Manual Maintenance Override

### Manual Battery Disconnect

- The physical **UPS switch** between battery and relay allows safe disconnection during maintenance.
- No feedback current due to **diodes**, but always disconnect at switch before touching terminals.

---

## 3. Cold Start Behavior

### Low-Temperature Considerations

- Batteries may have reduced capacity below 5°C.
- PTC fuses may take longer to reset if ambient temperature is very low.
- Suggest storing UPS in environments >10°C for optimal performance.

---

## 4. Estimated Consumption Overview

| Module                  | Current Draw | Notes                                |
|-------------------------|--------------|--------------------------------------|
| Meanwell HDR-15-12      | 15W max      | Powers logic and sensors only        |
| Relay DIN               | 25–40 mA     | When closed (battery active)         |
| StepDown Module         | 10–20 mA     | Idle; increases if load present      |
| eBus WiFi Module        | 50–120 mA    | Based on signal activity             |
| LED Indicators (each)   | 5–10 mA      | @ 12V with built-in resistor         |

---

## 5. Fault Table and Troubleshooting

| Symptom                       | Possible Cause                   | Recommended Check                   |
|-------------------------------|----------------------------------|-------------------------------------|
| LED2 (Charging) always ON     | Diode leakage or wiring error    | Measure voltage after PTC+diode     |
| LED3 (UPS Active) never ON    | Switch OFF / relay not energized | Check relay V+ and battery switch   |
| WiFi never activates          | StepDown disconnected / relay KO | Measure 5V OUT after filtering      |
| Battery not charging          | Blown PTC fuse                   | Test continuity on PTC              |
| LED5 never ON (Standby)       | LED2 or LED3 logic not working   | Confirm both are truly OFF          |

---

## 6. Frequently Asked Questions (F.A.Q.)

**Q: Why use a Schottky diode in the battery line?**  
A: Low forward voltage drop (typically 0.3–0.4V) ensures efficient charging without backflow into the main supply.

**Q: Can I replace the battery with a LiFePO4 pack?**  
A: Yes, if nominal voltage is compatible (12–12.8V) and charging circuit is protected.

**Q: Can I manually activate UPS mode for tests?**  
A: Yes, switch off grid input and turn ON battery switch. Relay will activate and power the StepDown.

**Q: Will the relay fail if grid and battery are both active?**  
A: No. The relay only receives V+ from battery and activates when Meanwell is OFF (grid loss).

---

## 7. Test Points (TP) for Debugging

| TP # | Location                       | Expected Voltage (Nominal) | Condition                  |
|------|--------------------------------|-----------------------------|----------------------------|
| TP1  | Meanwell V+ output             | ~12V                        | Grid ON                    |
| TP2  | Battery charging input (post-PTC) | ~12V                     | Grid ON, charging active   |
| TP3  | StepDown OUT+ (before relay)   | ~5V                         | UPS active (grid OFF)      |
| TP4  | COM1 after relay & filter      | ~5V                         | UPS active, filtered OK    |
| TP5  | LED4 input line                | ~5V                         | WiFi power should be ON    |

---

## 8. Suggested Maintenance Routine

- Test battery voltage under load every 3–6 months
- Check LED status at least weekly
- Verify relay click (audible) during grid blackout simulation
- Clean WAGO terminals yearly to avoid oxidation
- Replace PTC fuse if UPS output never activates (fuse may be locked open)

---

This document enhances the UPS Module v3.0 with deeper diagnostics, protection measures, and test references for advanced users and integrators.
