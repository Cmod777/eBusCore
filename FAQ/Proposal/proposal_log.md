FAQ Proposal Log

This file collects all open technical proposals, questions or unresolved ideas.
Each entry is uniquely numbered and dated. When merged, it will be moved to FAQ/merged.md.


---

Proposal #001 – [2025-04-11]

Title: Thermal Overload Risks Inside IP65 Enclosure
Status: pending
Description:
A question was raised regarding potential overheating inside the sealed IP65 enclosure housing the SLA battery and other active components (relays, step-down modules, power supply).

During summer, with direct sun exposure, internal temperatures may rise significantly above 40°C, possibly reaching 55–60°C. This could affect:

SLA batteries: reduced lifespan, outgassing, swelling

Step-down modules: output instability or shutdown

Relays: increased coil resistance, sticking contacts

Meanwell HDR PSU: derating above 50°C


Concern Origin:
“What happens if the battery goes above 40°C? Could it explode? Should we add a temperature monitoring system or a disconnection safety?”

Proposed Solutions:

1. Add a DS18B20 or similar temperature probe inside the case


2. Monitor temperature via ESP32 or integrate with Home Assistant


3. Set alert thresholds (e.g., warning at 45°C, critical at 60°C)


4. Use a thermal relay to cut battery load above 60°C


5. Add thermal warnings in the maintenance manual and SOP section


6. Reposition enclosure in shade or with passive ventilation



Next Step:
Evaluate monitoring implementation and draft a new SOP if needed.
When finalized, this FAQ should be integrated into the official documentation.


---

Proposal #002 – [2025-04-12]

Title: Automatic Sun-Triggered UPS Enclosure Covering
Status: pending
Description:
Idea to integrate a light sensor (e.g., lux-based) on the balcony near the UPS enclosure, to detect when it is hit by direct sunlight. The system would automatically trigger a covering mechanism (such as a motorized curtain or tilt cover) to shade the UPS and reduce internal heat buildup.

This could work in tandem with internal thermal sensors to ensure heat remains within safety margins, especially during summer months.

Proposed Solutions:

1. Mount an external lux sensor with proper orientation


2. Use a Shelly or similar relay to control a shading device


3. Define lux thresholds (e.g., >40k lux = cover)


4. Integrate with existing Home Assistant automations


5. Optional manual override or conditionals (e.g., only if UPS is online)



Next Step:
Evaluate feasibility and hardware placement. Possibly prototype on test enclosure before full integration.

---

### Proposal 3 – Real-time Battery Voltage Monitoring

**Date:** 2025-04-13  
**Title:** Real-time Battery Voltage Monitoring  
**Status:** Pending  
**Description:**  
The current UPS module works correctly but does **not include any live voltage monitoring** for the battery. In case of battery degradation, under-voltage, or anomalies, there would be no visual or digital feedback.  
Adding real-time voltage monitoring would enhance system awareness, allowing detection of low battery levels, charging issues, or aging cells before failure occurs.

**Proposed solution:**  
- **Basic mode (analog):** add a **12V panel voltmeter**, connected to the battery terminals via a dedicated line or small switch, to provide direct voltage reading.
- **Advanced mode (smart):** connect an analog voltage sensor to a free input of the **Shelly Plus Add-On**, allowing live monitoring in Home Assistant.
- **Optional alarm:** trigger a notification in Home Assistant if the battery drops below a threshold (e.g., <11.5V).
- The system must be **non-invasive** and must not interfere with the main power path.

---

### Proposal 4 – Battery Temperature Sensor

**Date:** 2025-04-13  
**Title:** Battery Temperature Sensor  
**Status:** Pending  
**Description:**  
The UPS module currently does not monitor the battery temperature. However, certain battery chemistries (e.g., LiFePO4) may require controlled charging behavior depending on temperature.  
Adding a temperature sensor allows for safer operation and can help avoid battery damage in case of charging at low or high temperatures.

**Proposed solution:**  
- Use a **temperature probe** (e.g., DS18B20 or NTC) placed near or in contact with the battery.
- Connect the sensor to the **Shelly Plus Add-On** to allow live temperature readings inside Home Assistant.
- Optionally implement logic in Home Assistant to disable charging or trigger a warning if temperature is out of range (e.g., below 0°C or above 45°C).
- This sensor can also support future maintenance or diagnostics routines.

---

### Proposal 5 – Periodic UPS Self-Test

**Date:** 2025-04-13  
**Title:** Periodic UPS Self-Test  
**Status:** Pending  
**Description:**  
The UPS system currently relies on external power loss to trigger the battery switchover. However, there is no built-in mechanism to verify the correct behavior of the UPS logic during idle periods.  
A scheduled self-test routine would help confirm that all components (relay, battery, step-down, filters) operate correctly when needed.

**Proposed solution:**  
- Implement a **controlled simulation of power failure** once every 30 days.
- This can be done via **smart relay or Shelly** (e.g., Shelly 1PM) that temporarily cuts 230V input to the MeanWell.
- During the test, monitor expected behavior:
  - Relay activation
  - LED status changes (e.g., Using, WiFi Ready)
  - Shelly uptime via 5V line
- Optionally log the test result or alert if behavior does not match expected patterns.

---

### Proposal 6 – Quick Diagnostic Port

**Date:** 2025-04-13  
**Title:** Quick Diagnostic Port  
**Status:** Pending  
**Description:**  
During maintenance or troubleshooting, manually probing key voltage points inside the UPS module can be time-consuming or unsafe due to tight wiring.  
A dedicated, clearly labeled diagnostic port would allow fast and safe testing using a multimeter or tester without disassembling the system.

**Proposed solution:**  
- Add a **small terminal block or 2-pin sockets** (DIN-rail mountable) to expose:
  - Battery voltage
  - Step-down 5V output
  - GND reference
- Mark terminals clearly (e.g., VBAT, VOUT5V, GND).
- Ensure ports are protected against accidental shorts (e.g., recessed terminals or fused).
- This feature improves maintainability and encourages routine voltage checks.
