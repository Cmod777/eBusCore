# Analysis – FAQ Proposal #001  
**Date:** 2025-04-11  
**Title:** Thermal Overload Risks Inside IP65 Enclosure

---

## 1. Context

This analysis responds to Proposal #001 regarding the risk of thermal overload inside a fully sealed IP65 enclosure used outdoors in summer conditions.

The system includes:
- SLA 12V battery (Yuasa 12Ah)
- Step-down buck converter (12V to 5V)
- Meanwell HDR-15-12 DIN PSU
- Finder relay module
- W1209 or similar thermal controller
- ESP-eBUS module (Wi-Fi active device)
- 3× 40x40mm fans (2 intake, 1 exhaust)

The enclosure is a **12-module vertical IP65 DIN box** with a transparent front panel, mounted externally.

---

## 2. Worst-Case Thermal Scenario

### Ambient Conditions:
- Outdoor air temp: **40–42°C**
- Direct sunlight: **12h continuous**
- Enclosure wall material: **ABS plastic**
- Solar exposure adds **~20–25°C** to internal ambient without ventilation.

### Internal heat sources:
- Meanwell PSU: ~3W dissipation
- Step-down module: ~1–2W
- ESP module: ~1–2W
- Relays: coil warming over long activation
- Battery: negligible self-heating, but absorbs ambient rise

**Without ventilation**, temperatures may rise up to:
- **Upper area**: 65–70°C
- **Central**: 60–65°C
- **Lower**: 55–60°C

---

## 3. Thermal Risks

### SLA Battery:
- Optimal operating temp: **20–25°C**
- Acceptable range: **0–40°C**
- Critical degradation: **>50°C**
- At **60°C**, lifespan drops to **~20–30%**, with risks of swelling, outgassing, or venting.

### Step-down module:
- Typical buck converters reduce efficiency and may shut down above **60°C**
- Possible ripple instability

### Relays:
- Coil heating increases resistance
- Possible contact welding or failure to open at extreme temps

### Meanwell PSU:
- Official derating begins at **>50°C**
- Output voltage may drift, reduced current delivery

---

## 4. Passive and Active Mitigations

### **Passive Protections:**
- Full internal lining:
  - IR reflective film (e.g. aluminum thermal sheet)
  - 2mm EVA foam (heat resistant and insulating)
- Thermal isolation from surfaces
- External installation under **awning, canopy, or partial shade**
- 4 or 8 filtered microholes (6mm) for passive airflow (IP downgraded to IP54)
- **Heat zoning** inside (hot/cold spacing)

### **Active Protections:**
- 3× 40x40mm fans (2 push at bottom, 1 pull at top)
- Controlled by W1209 thermal module
- Fan activation at 40–42°C, shutdown <35°C
- Real-time temperature monitoring with ESP/DS18B20 sensor
- Optionally integrate alerts in Home Assistant

---

## 5. Simulated Outcomes

### Scenario A – Worst case (no protection):
| Zone     | Estimated Max Temp |
|----------|--------------------|
| Upper    | 65–70°C  
| Central  | 60–65°C  
| Lower    | 55–60°C  

→ Battery lifespan cut to 12–18 months. Electronics at risk.

---

### Scenario B – Passive insulation only:
| Zone     | Estimated Max Temp |
|----------|--------------------|
| Upper    | 58–60°C  
| Central  | 50–53°C  
| Lower    | 47–50°C  

→ Still risky. Better, but battery life still shortened. PSU may derate.

---

### Scenario C – Passive + active ventilation:
| Zone     | Estimated Max Temp |
|----------|--------------------|
| Upper    | 46–50°C  
| Central  | 40–45°C  
| Lower    | 38–42°C  

→ All components within operational range. Battery life preserved.

---

### Scenario D – Mid-shade + all protections:
| Zone     | Estimated Max Temp |
|----------|--------------------|
| Upper    | 42–44°C  
| Central  | 37–40°C  
| Lower    | 35–38°C  

→ Optimal. All temps under 45°C. Long component life.

---

## 6. Design Decisions and Engineering Trade-offs

| Decision                                   | Justification |
|-------------------------------------------|---------------|
| Loss of IP65 in favor of IP54             | Required for air exchange. Fully sealed box causes thermal buildup.  
| Internal fans with filtered holes         | Improves convection, limits dust.  
| Passive insulation (IR + EVA)             | Reflects radiation, delays temperature rise.  
| Horizontal spacing of heat zones          | Prevents localized overheating.  
| Battery placement at bottom               | Keeps the most heat-sensitive component in cooler air zone.

---

## 7. Recommendations

- Accept controlled loss of IP65 in favor of thermal safety (IP54 acceptable for outdoors under cover).
- Implement real-time thermal monitoring with alert logic.
- Add maintenance routine to check filters, fans, and verify airflow.
- Consider extra thermal relay as hard shutdown at 60–65°C.

---

## 8. Conclusion

The thermal overload risk inside an IP65 box is real and dangerous, particularly for SLA batteries.  
This analysis confirms that **with correct insulation, ventilation, and monitoring**, the risks can be mitigated effectively.

The proposed layout, components, and airflow logic are solid and backed by realistic estimations.

---

**Next step:**  
This document will serve as the base for the final FAQ resolution once the monitoring hardware is confirmed and the SOP is updated.
