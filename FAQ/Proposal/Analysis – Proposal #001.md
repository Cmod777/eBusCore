# Analysis – FAQ Proposal #001  
**Date:** 2025-04-11  
**Title:** Thermal Overload Risks Inside IP65 Enclosure

![Thermal map – mid-shade scenario](mappa_termica_ip65_midshade_passive_active_comparison.png)
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


---

## 9. Additional Considerations and Extended Reasoning

Several technical discussions emerged during the planning and simulation stages that should be documented for clarity and reproducibility.

- **Avoid use of metals** inside the enclosure for passive dissipation or thermal conduction.  
  While external heatsinks might seem effective, metal elements in close proximity to electronic boards and battery terminals significantly increase the risk of **accidental short-circuits or arcing**, especially in humid conditions.  
  Therefore, no copper, aluminum, or metallic plates are used internally.

- The **IR reflective layer** used is **not a metallic foil**, but a **UV-reflective window film**, typically applied on glass. It is extremely thin, flexible, lightweight, non-conductive, and safe to use in close proximity to electronics.  
  Its goal is to **reflect incident infrared radiation** before it penetrates the box, reducing the passive heat absorption.

- The **EVA foam insulation** is chosen for its:
  - Thermal insulation properties
  - Flame retardant potential
  - Easy shaping and low thickness (2mm)
  - Electrical neutrality

- Holes for airflow (6–8 units, 6mm each) are protected using:
  - **Mesh fabric (e.g., tulle, non-woven filter cloth)**
  - **Reinforced with “inTape” mesh tape**, a durable bug-proof adhesive strip
  - This results in a passive protection roughly equivalent to **IP54**, offering airflow while minimizing ingress of dust or insects

- The **layout of components was planned using thermal zoning**:  
  Heating and semi-heating elements are distributed in such a way to **avoid direct heat stacking**, giving the fans better flow performance and minimizing hot spots.

- **Fan configuration**:
  - Two **bottom fans (PUSH)** inject fresh air
  - One **top fan (PULL)** extracts hot air
  - All fans are 40x40mm and low profile, allowing vertical DIN installation

- **Sensor probe (NTC or DS18B20)** is placed in the lower-middle region, where the battery sits, to capture the most critical thermal data for system protection.

- Considered and discarded approaches:
  - Metal fins or plates: rejected due to conduction and short-circuit risk
  - Large open slots: rejected due to loss of mechanical protection and dust ingress
  - Full active cooling (e.g., Peltier): not suitable due to space, cost, and power draw

- The enclosure is designed to work in **three thermal modes**:
  1. **Fully passive**, if fans fail: still functional up to ~60°C
  2. **Semi-passive**, with microholes only: moderate convection through filtered vents
  3. **Full active**, with 3 fans managed by a thermal controller

- If ventilation completely fails in a shaded installation, insulation alone keeps the battery below 50°C. In direct sun without fans, it may exceed safe thresholds, thus fans are strongly recommended.

- **Thermal design was iteratively improved**, based on both theoretical models and practical constraints such as:
  - Physical space within DIN box
  - Component mounting (e.g., battery position, wiring)
  - Access to airflow paths
  - Fan placement feasibility (edges, corners, lower height)

This combined design ensures that even in worst-case summer exposure, the system maintains a safe operating envelope.  
Future revisions may explore more advanced fan control, humidity sensors, or adaptive intake grilles, if needed.

---

## 10. Passive Insulation Only – Degradation Risk with Fan Failure (Mid-Shadow Scenario)

This section provides a predictive analysis of what may occur if the **mechanical ventilation system fails**, while the enclosure remains under **mid-shade (canopy or awning protection)** and retains its **full passive insulation** (IR reflective layer + EVA foam 2mm).

### Context:
- External air: ~40°C (August scenario)
- Exposure: **partially shaded**, no direct solar radiation for full duration
- Internal fans: **non-functional (failure or disconnect)**
- Microholes (6–8 units, 6mm) allow limited **natural convection** (IP54 equivalent)

---

### Estimated Internal Temperatures:
| Area          | Expected Range (°C) |
|---------------|---------------------|
| Upper Zone    | 58–60°C  
| Central Zone  | 50–53°C  
| Lower Zone    | 47–50°C  

---

### Thermal Stress and Material Degradation Risks:

#### **SLA Battery (Yuasa 12Ah)**:
- Expected temp: **47–50°C**
- **Accelerated aging** begins above 40°C
- At 50°C → battery lifespan reduced to **approx. 1.5–2 years**
- Electrolyte loss may occur over time → risk of swelling or internal vent activation

#### **Step-Down Converter**:
- Operating near thermal ceiling  
- May experience **voltage drift** or **occasional shutdowns** under sustained load  
- Plastic casing may discolor or deform over years

#### **Finder Relay**:
- Coil heating may increase due to poor heat dissipation  
- Risk of **sticking contacts** or slower switching response  
- Long-term: increased failure rate after **1–2 summers**

#### **Meanwell HDR PSU**:
- Official derating begins >50°C  
- Internal regulation may become unstable under peak draw  
- Long-term: increased thermal cycling → capacitor wear

#### **Plastic Components and Adhesives**:
- Enclosure and mountings generally rated to 70–80°C, but prolonged operation at 60°C accelerates **yellowing, plastic fatigue**, or warping of cable ducts, wire holders, and foam adhesives

---

### Summary:
This “fans failed but passively shaded” condition is **not immediately dangerous**, but **definitely suboptimal**:
- Internal temps remain **within tolerance**, but **close to degradation thresholds**
- All components age faster
- Maintenance cycle shortens (battery, relays, PSU)
- Fans must be treated as **critical components** for thermal stability

### Recommendation:
- Include this failure mode in the **SOP risk matrix**  
- Add **inspection reminders** for fan function and vent cleanliness  
- Optionally, add a **redundant thermal shutdown** relay near 60–65°C  
- Treat long-term operation in this state as **emergency fallback**, not normal condition

---

## 11. Risk Assessment – Passive Only (No Fans, Mid-Shadow)

This section details the actual risks and degradation expected when operating the system **without any active ventilation**, under **partial shading** (mid-shadow) but with **full passive thermal protection** in place.

### Scenario Details:
- **External temperature:** 40–42°C (peak summer)
- **Ventilation:** All fans inactive (mechanical failure or disconnection)
- **Exposure:** Shaded (no direct sunlight for long periods, tenda/canopy present)
- **Insulation:** Applied (IR reflective film + 2mm EVA foam on all surfaces)
- **Filtered airflow:** 6–8 microholes (Ø6 mm), protected with dual-layer mesh (IP54 equivalent)

---

### Estimated Internal Temperatures:
| Area         | Temperature Range |
|--------------|-------------------|
| Upper Zone   | 58–60°C  
| Central Zone | 50–53°C  
| Lower Zone   | 47–50°C  

---

### Degradation and Reliability Risk – Per Component:

| Component              | Thermal Stress | Lifespan Impact                          | Risk Level |
|------------------------|----------------|------------------------------------------|------------|
| **SLA Battery**        | Medium–High    | Lifespan drops to **1.5–2 years max** due to continuous operation near 50°C | **Critical**  
| **Step-down Converter**| Medium         | Gradual efficiency drop, risk of **instability or shutdown** under sustained load | **Moderate**  
| **Finder Relay**       | Medium         | Coil resistance increases, possible **sticking contacts** or reduced mechanical life | **Moderate**  
| **Meanwell PSU**       | Medium–Low     | Derating occurs above 50°C, capacitor life may reduce over time | **Mild–Moderate**  
| **Wiring and Plastics**| Low–Medium     | EVA and plastic clips may **yellow or soften**; adhesives can weaken over time | **Low**  
| **IR Film and EVA Foam**| Low           | Materials designed for ~70°C, minimal risk below 60°C | **Negligible**  

---

### Interpretation:

- This configuration is **not immediately dangerous**, but clearly **accelerates component degradation**
- It should be considered a **safe fallback mode**, not a long-term operational standard
- The battery is the most vulnerable element in this scenario
- The system should include **fan status monitoring** and possibly **thermal alarms** if fans remain offline for extended time
- Periodic **maintenance checks** must be planned to assess fan status and internal airflow

---

### Summary Recommendation:
- Define this mode as a **"degraded passive fallback"**
- Integrate it into the **risk matrix and SOP**
- Warn the user that **performance and longevity will suffer** if this condition persists
- If fan failure is detected, alert and recommend intervention within **days**, not months

---

## 12. Component Lifespan Estimate and Safety Risk – Passive Only (No Fans, Mid-Shadow)

This section provides a predictive estimate of the **realistic operating lifespan** of each core component inside the enclosure under the defined degraded condition:

- **No active ventilation (fan failure)**
- **Mid-shadow installation (partial sunlight exposure)**
- **Passive insulation only (IR film + EVA 2mm)**
- **Filtered airflow via 6–8 microholes (IP54 equivalent)**
- **Internal temperatures: ~47–60°C range depending on zone**

---

### Estimated Lifespan Under This Condition:

| Component              | Estimated Lifespan       | Normal Lifespan | Degradation Factor |
|------------------------|---------------------------|------------------|---------------------|
| **SLA Battery (Yuasa)**| ~18–24 months             | 4–5 years         | **~60% shorter**  
| **Step-down Converter**| ~2–3 years                | 4–5 years         | Moderate (thermal wear)  
| **Finder Relay**       | ~3–4 years                | 5–7 years         | Moderate (coil heating, contact fatigue)  
| **Meanwell HDR PSU**   | ~4–5 years                | 7–10 years        | Light (capacitor aging)  
| **ESP / MCU**          | ~4–6 years                | 6–8 years         | Minimal, assuming passive cooling  
| **Wiring and connectors** | ~5 years              | 8–10 years        | Aesthetic/adhesive degradation only  
| **Box plastic & EVA foam** | >7 years             | 10+ years         | Within spec, no major risk  

---

### Risk for User Safety:

| Category                  | Risk Level | Explanation |
|---------------------------|------------|-------------|
| **Electrical fire hazard**| **Low**    | No flammable buildup, no short-circuit exposure with current layout  
| **Battery leakage/gas**   | **Moderate** | If temps exceed 55°C frequently, internal pressure may vent over time  
| **Plastic melting/deformation** | **Low** | No risk below 70°C  
| **Shock hazard**          | **None**   | Fully enclosed, grounded, no external terminals exposed  
| **System shutdown or failure** | **Moderate–High** | Performance degradation may lead to loss of control, false triggers, or total outage  

---

### Conclusion:

- This condition is **not directly dangerous for the user**, but it **significantly reduces reliability and component life**
- The **SLA battery is the most affected**, with expected lifespan **halved or worse**
- Other electronics will gradually degrade and become unstable within **2–4 years**
- The setup is **tolerable for short periods**, but **should not be maintained long-term**

---

### Recommendation:

- Treat this as an **emergency passive fallback mode**, not standard operation
- **Replace fans** or restore active ventilation as soon as possible
- Add clear alerts in **SOP, maintenance, and monitoring scripts**
- If fan failure persists >1 week in summer, schedule immediate inspection

---

**Emergency Recommendation:**  
If a complete fan failure is detected or expected to persist **for more than 7 days during summer**, and no intervention is possible in that timeframe:

→ **Immediately disconnect and remove the SLA battery** from the system.  
Store it indoors, in a shaded, well-ventilated location.

> This ensures the system remains electrically safe and avoids the risk of battery overheating, swelling, or venting.  
> The rest of the circuit may remain powered (via PSU only), but with reduced functionality.  
> This passive configuration allows safe operation until proper maintenance is performed.

