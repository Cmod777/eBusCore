# FAQ Proposal Log  
This file collects all open technical proposals, questions or unresolved ideas.  
Each entry is uniquely numbered and dated. When merged, it will be moved to `FAQ/merged.md`.

---

### Proposal #001 – [2025-04-11]  
**Title:** Thermal Overload Risks Inside IP65 Enclosure  
**Status:** pending  
**Description:**  
A question was raised regarding potential overheating inside the sealed IP65 enclosure housing the SLA battery and other active components (relays, step-down modules, power supply).

During summer, with direct sun exposure, internal temperatures may rise significantly above 40°C, possibly reaching 55–60°C. This could affect:

- **SLA batteries**: reduced lifespan, outgassing, swelling
- **Step-down modules**: output instability or shutdown
- **Relays**: increased coil resistance, sticking contacts
- **Meanwell HDR PSU**: derating above 50°C

**Concern Origin:**  
“What happens if the battery goes above 40°C? Could it explode? Should we add a temperature monitoring system or a disconnection safety?”

**Proposed Solutions:**  
1. Add a DS18B20 or similar temperature probe inside the case  
2. Monitor temperature via ESP32 or integrate with Home Assistant  
3. Set alert thresholds (e.g., warning at 45°C, critical at 60°C)  
4. Use a thermal relay to cut battery load above 60°C  
5. Add thermal warnings in the maintenance manual and SOP section  
6. Reposition enclosure in shade or with passive ventilation

**Next Step:**  
Evaluate monitoring implementation and draft a new SOP if needed.  
When finalized, this FAQ should be integrated into the official documentation.
