# Phase 1: Preparation of the External Structure

## Objective of This Phase

This phase defines the external housing structure that provides the first layer of protection for all internal components.  
A properly selected and configured enclosure ensures electrical safety, environmental resistance, and long-term system durability.

The goal is to establish a secure, maintainable, and adaptable external framework before integrating any internal modules or wiring.

---

## Enclosure Selection Criteria

The choice of enclosure depends on the specific installation context and must be aligned with environmental conditions, accessibility, and safety requirements.

A suitable enclosure should meet the following minimum criteria:

- **Ingress Protection (IP):** Sufficient to protect against dust, moisture, or accidental contact. A minimum of **IP44** is recommended for indoor protected areas, while **IP65 or higher** may be required for outdoor or semi-exposed environments.
- **DIN Rail Capacity:** It is recommended to use an enclosure with at least **36 DIN modules**.  
  While smaller enclosures could be used depending on the minimum number of installed components, a 36-module structure ensures:
  - Easier internal organization and wiring
  - Safer and more accessible maintenance
  - Pre-allocation of space for future expansions or upgrades
  
  Choosing a sufficiently large enclosure prevents the need for major rework when additional features are added to the system.
- **Material:** Flame-retardant, insulating, and durable (e.g., thermoplastic or fiberglass-reinforced plastic).
- **Accessibility:** Transparent or hinged cover for inspection, with lock or screw closure to prevent accidental opening.
- **Compliance:** Should conform to standards such as **IEC 60670-24** or **IEC 62208**, or equivalent local regulations.

> Note: Over-specifying enclosure protection (e.g., using IP65 in covered outdoor areas) is not strictly required but may improve system reliability and reduce future maintenance, especially in harsh environments.

---

## Project Case Example

In this project, the selected enclosure is a [DIN 36-module IP65-rated external case](https://github.com/Cmod777/eBusCore/blob/main/datasheets/external/case/Product%20datasheet.pdf).

Although the system is installed in a covered outdoor area, where an IP65 rating was not strictly necessary, a higher protection level was intentionally chosen. This decision was made based on the principle of long-term reliability, minimizing potential maintenance, and protecting the internal components even against unexpected environmental conditions.

> Important: The choice of enclosure must always be adapted to the actual installation environment. If the system is installed indoors or in a well-protected area, lower IP ratings (e.g., IP44) may be sufficient. However, any modifications to the enclosure, such as drilling for cable entries, must preserve the original protection rating by using certified IP-rated accessories.

---

## Critical Considerations During Modifications

Once an enclosure has been selected, its rated level of protection (e.g., IP65) must be preserved throughout the entire installation process. Any mechanical modifications—such as drilling holes for cable glands, ventilation, mounting accessories, or inserting external connectors—can compromise the enclosure's protective properties if not properly handled.

The overall protection level of the system is determined by **the weakest point**. For example, adding a non-rated cable entry to an IP65 enclosure may reduce its effective protection to IP20 or lower.

To ensure protection integrity:
- Use only **IP-rated certified cable glands and accessories**, matching or exceeding the enclosure’s original rating.
- Avoid over-drilling, excessive openings, or improper sealing materials.
- Ensure that all external penetrations are protected against water ingress, dust, and mechanical stress.
- Validate all modifications with physical inspection and testing.

> Consider the IP rating as a system-wide value, not just a label on the box. Every component added to the enclosure must uphold the same level of protection for the rating to remain valid.

---

## Cable Routing and Ventilation Openings

Any modifications made to the enclosure, such as drilling holes for cable routing or ventilation, must be planned carefully.  
Unnecessary or excessive openings can compromise the mechanical integrity and ingress protection (IP) rating of the enclosure.

In this project, **two cable entry holes** were created:
- One dedicated to **power supply cables**
- One dedicated to **low-voltage signal cables**

This separation was specifically chosen to:
- Reduce the risk of **electromagnetic interference (EMI)**
- Preserve the **signal integrity** of sensitive communication lines
- Ensure safe and independent routing of power and control systems

> **Disclaimer:**  
> Do not create unnecessary openings. All drillings should be justified by the actual layout and wiring needs.  
> Mixing power and signal lines in the same conduit or gland can lead to long-term reliability issues, especially in systems that use sensitive data or communication signals.  
> Always use **IP-rated cable glands** or seals matching the enclosure's rating to avoid accidental degradation of protection.

---

## External Connectors

In this project, we have chosen to use [WEIPU SP13 Series 4-pin circular connectors](https://github.com/Cmod777/eBusCore/blob/main/datasheets/external/enclosure-feedthroughs/SP13-Series-WEIPU-Connector.pdf) for external connections.

These connectors offer several advantages:

- **High Ingress Protection:** With an IP68 rating, they provide superior protection against dust and water ingress, ensuring the integrity of the enclosure even in harsh environments.
- **Compact Design:** Their small size makes them suitable for applications with limited space, without compromising on performance.
- **Ease of Maintenance:** The threaded coupling mechanism allows for quick and secure connections, facilitating easy disconnection and reconnection during maintenance or upgrades.
- **Versatility:** Available in various configurations, they can accommodate different cable diameters and contact arrangements, making them adaptable to various system requirements.

> **Note:** When integrating such connectors, it's crucial to ensure that the installation maintains the overall IP rating of the enclosure. Proper sealing and mounting techniques should be employed to prevent any compromise in protection.

In the following steps of this same phase, we will also describe how to correctly wire and secure these connectors, ensuring both mechanical stability and proper electrical contact.

Before that, however, we will address the topic of **ventilation openings**, which are essential for thermal management and must be planned without compromising the enclosure’s protection rating.

---

## Ventilation Openings

Proper thermal management is critical to ensure system reliability and longevity. Passive airflow based on natural convection ("gravity ventilation") allows heat to dissipate without introducing active cooling systems, thus maintaining simplicity and robustness.

However, achieving professional-grade ventilation requires more than simply drilling holes into the enclosure:

- Unprotected openings would immediately compromise the IP rating, drastically lowering the enclosure's resistance to dust and water ingress.
- A non-sealed hole can reduce a standard IP65 enclosure to IP20 or even lower, exposing internal components to severe environmental risks.

To maintain protection while enabling ventilation, it is necessary to use **certified IP-rated ventilation devices**, such as:

- **Breathable membranes** allowing air exchange while blocking water and dust (e.g., IP66/IP68 vent plugs)
- **Filtered ventilation glands** that maintain a controlled airflow without open exposure
- **Dedicated air vents** with labyrinth seals for enhanced protection

> **Note:**  
> Always select ventilation products with a certified IP rating matching or exceeding that of the original enclosure. Proper installation according to manufacturer guidelines is mandatory to preserve the declared protection level.

---

## Ventilation Strategy and Airflow Calculation

To ensure effective passive ventilation within the enclosure, a chimney-effect airflow system has been implemented. This consists of placing vent plugs in the lower and upper sections of the box to enable natural convection: cooler air enters from below, heats up inside the enclosure, and exits through the top.

### Vent Plug Selection

The [Keystone Electronics 8612 Vent Plug](https://github.com/Cmod777/eBusCore/blob/main/datasheets/external/enclosure-feedthroughs/534-8612_ventplug.pdf) was selected for this purpose. This component features:

- **Material:** Nylon 6/6, UL 94V-2
- **Mounting:** Snap-in installation
- **Nominal diameter:** 25.78 mm
- **Rated protection:** IP67
- **Function:** Allows gas exchange while limiting ingress of dust and moisture

> **Note:**  
> The official datasheet for this specific model does not specify the airflow rate.  
> However, based on comparable vent plug designs with similar dimensions and structure, the estimated airflow is assumed to be between **1000 and 1500 ml/min**, under standard pressure differential conditions.

### Recommended Vent Plug Configuration

- **Minimum:** 1 vent plug at the bottom and 1 at the top
- **Recommended:** 2 at the bottom and 2 at the top
- **Maximum:** 3 at the bottom and 3 at the top

Adding more than 3 per side generally provides diminishing returns and may unnecessarily weaken the structure or complicate sealing.

### Enclosure Volume

Based on the actual dimensions of the [ETI ECH-36PT enclosure](https://github.com/Cmod777/eBusCore/blob/main/datasheets/external/case/Product%20datasheet.pdf):

- **Height:** 508 mm  
- **Width:** 319 mm  
- **Depth:** 144 mm  
- **Approximate internal volume:** **23.4 liters**

### Air Exchange Time Estimate

Assuming an airflow rate of **1250 ml/min per vent plug** (average estimation), the estimated full air exchange times are as follows:

| Vent Plugs (Total) | Estimated Airflow | Exchange Time for 23.4 L |
|--------------------|-------------------|---------------------------|
| 2 (1 bottom, 1 top) | ~2500 ml/min      | ~9.4 minutes              |
| 4 (2 bottom, 2 top) | ~5000 ml/min      | ~4.7 minutes              |
| 6 (3 bottom, 3 top) | ~7500 ml/min      | ~3.1 minutes              |

> These values are theoretical and assume ideal placement and airflow paths. Actual performance may vary based on installation conditions and environmental factors.

### Conclusion

Ventilation is critical to maintain thermal stability and prevent condensation. Using professional-grade vent plugs allows for controlled gas exchange without compromising the enclosure’s IP rating. Placement and quantity must be planned according to enclosure size and heat dissipation requirements.

---

## Air Temperature Drop Estimate (Theoretical Model)

In addition to providing ingress protection, controlled passive ventilation significantly improves the internal thermal management of the enclosure.

Based on the **first-order exponential cooling law** (derived from Newton's Law of Cooling), we can estimate the theoretical temperature reduction over time, assuming passive air replacement through the vent plugs.

### Assumptions for the Model

- **Enclosure internal volume:** 23.4 liters
- **Passive airflow rate (estimated with 4 vent plugs):** ~5000 ml/min
- **Initial internal temperature (spring conditions):** ~35°C
- **External ambient temperature (spring average):** ~20°C
- **Ideal air exchange and no major obstructions**

### Theoretical Model and Governing Law

The temperature decrease can be modeled using the following formula:

T(t) = Text + (T0 - Text) * e^(-t / tau)

Where:
- `T(t)` = internal temperature at time `t`
- `T0` = initial internal temperature
- `Text` = external ambient temperature
- `tau` = time constant (minutes), calculated as:

tau = V / Q

with:
- `V` = internal volume (liters)
- `Q` = airflow rate (liters per minute)

### Specific Calculation

Given:

- V = 23.4 liters
- Q = 5.0 liters/minute

then:

tau = 23.4 / 5 = 4.68 minutes

After one time constant (≈ 4.7 minutes), the internal temperature would decrease by approximately **63%** of the initial temperature difference relative to the ambient temperature.

| Time | Estimated Internal Temperature |
|------|-------------------------------|
| 0 min | 35°C (initial)                |
| 5 min | ~25.5°C                       |
| 10 min | ~21.3°C                      |

### Important Disclaimer

> **Disclaimer:**  
> This model is based on ideal physical assumptions and does not consider:
> - Internal heat generation by electronic components (which always occurs to some extent)
> - Variations in ambient temperature, humidity, or direct solar radiation
> - Real-world inefficiencies in air movement and obstruction inside the enclosure
>
> In real applications, internal temperatures are typically higher than the ambient environment, especially during active operation.  
> Nevertheless, even basic passive ventilation significantly helps to stabilize internal conditions and reduce thermal stress on components.

---

## External Connector Installation – Mechanical Preparation

To ensure a professional and reliable installation of the external connectors, the mechanical preparation of the enclosure must be carefully executed.

### Drilling the Hole

According to the connector's technical datasheet, the recommended hole diameter should match the specific requirements of the model used.  
In standard cases, it is strongly suggested to use a drill bit that precisely matches the specified diameter to guarantee a secure and tight fit.

However, in this specific project, due to limitations in available drill bits and considering the material of the enclosure, a different method was adopted:

- A drill bit with a diameter as close as possible to the required size was used to create an initial hole.
- The hole was then carefully widened using a fine-grain hand file, working progressively and checking frequently.
- The goal was to achieve the exact target diameter without introducing burrs, deformations, or compromising the IP rating integrity.

### Connector Mounting and Locking

Once the hole was properly sized:

- The connector was inserted into the hole following the datasheet’s recommendations regarding insertion direction and seating.
- The locking ring (or nut, depending on the model) was tightened by hand first, then gently secured using appropriate tools, ensuring not to over-tighten and damage either the connector body or the enclosure wall.
- Care was taken to preserve the O-ring (or sealing gasket) to maintain the maximum achievable IP rating.

> **Note:**  
> Careful mechanical preparation of the mounting hole is crucial for maintaining the enclosure's sealing and protection properties, especially in outdoor or humid environments.

---

## External Connector Wiring – Pin Crimping and Soldering

After preparing and mounting the external connectors, the next step involves properly wiring the internal side of the connector to ensure electrical safety, mechanical stability, and long-term reliability.

### Wiring Strategy and Safety Considerations

The type of connector used in this project (a circular multi-pin aeronautical-style connector) provides excellent mechanical stability but comes with a common limitation: **closely spaced pins**.  
For this reason, particular care must be taken during wiring and soldering operations to avoid short circuits, false contacts, or the formation of electrical arcs under load.

### Recommended Procedure

- **Crimp First:**  
  Each wire should first be **crimped using appropriate terminals** to ensure a clean mechanical contact and to simplify handling during soldering.
  
- **Presoldering Outside the Shell:**  
  Whenever possible, wires should be **tinned and pre-positioned outside the connector housing**, to minimize the time needed for actual soldering inside the confined connector space.
  
- **Pin Layout Strategy:**  
  To maximize electrical separation:
  - **Phase (L)** and **Neutral (N)** wires should be placed on opposite sides of the connector.
  - The **Ground (PE)** wire should always be positioned **in the center**, physically separating the two power conductors.

- **Soldering Technique:**  
  Once positioned, each wire should be soldered quickly and precisely:
  - Avoid excessive heating, which could deform the plastic pin body.
  - Ensure the solder joint is shiny, smooth, and free from cold joints or blobs.

- **Post-solder Protection:**  
  After soldering:
  - Apply **heat-shrink tubing** to each wire individually to prevent accidental contact between terminals.
  - Double-check that no solder spills or metallic residues remain between pins.

### Materials and Cable Recommendations

- **Solder type:**  
  Preferably use **solder with integrated flux** to improve wetting and reliability.  
  If using **lead-free solder**, keep in mind that it melts at a slightly higher temperature, so additional care is required to avoid overheating the pins or insulation.

- **Cable sectioning:**  
  For power conductors (e.g., mains voltage), use cables with a cross-section of **at least 1.5 mm²**.  
  A cross-section of **2.5 mm² is strongly recommended** to provide additional safety margin, reduce voltage drop, and ensure thermal stability over time.

> **Note:**  
> Given the small pitch of the pins, it's strongly recommended to check the finished connection using a continuity tester or multimeter before powering the system.  
> Proper wiring of the connectors is critical to avoid arc faults or damage to internal equipment, especially under high humidity or outdoor conditions.

### Additional protection after wiring

Once the crimping, soldering, and heatshrink insulation of the connector pins are completed,  
it is **highly recommended** to apply a small amount of **neutral-cure RTV silicone** over the soldered area.

This provides:
- Extra electrical insulation
- Improved mechanical stability
- Enhanced thermal resistance
- Additional protection against humidity and microvibrations

**Note:** Always use **neutral-cure RTV silicone** to avoid potential corrosion issues (avoid acetic types).  
Apply carefully over the joint area without obstructing the connector’s mechanical function.

### Internal Wiring Strategy and Distribution Options

Given that this type of connector is designed for quick external connection/disconnection, the internal pins are not meant to be reworked frequently. To maintain the quality and reliability of the soldered connection over time, it is advisable to avoid future reintervention on the connector side.

Two recommended strategies are:

- **Derivation Block (if space allows):**  
  If there is enough room inside the enclosure, route the 2.5 mm² power cables to a small internal distribution point (e.g., terminal blocks or compact busbars).  
  This approach simplifies further wiring and makes future expansions easier, without disturbing the original solder joints.

- **Compact modular blocks (if space is limited):**  
  In more constrained spaces, use compact connectors such as WAGO-type terminals with lever actuation.  
  These allow safe branching and future modularity without compromising the integrity of the original cabling.

In both scenarios:

- Keep signal and power lines physically separated, even within the enclosure.
- Place each bundle as close as possible to opposite sides of the case.
- Position entry holes (cable glands or plugs) slightly apart to further reduce the risk of electromagnetic interference between circuits.

> **Tip:**  
> Use CLIMP-style cable retainers or adhesive tie mounts to secure wires neatly along the enclosure walls and avoid mechanical stress on the connector pins.

---

### Final Considerations and Best Practices

Although this type of circular connector includes clearly numbered pin markings on both male and female sides, it is strongly recommended to:

- **Solder one pin at a time**, and double-check continuity and correct placement before proceeding to the next.
- This is especially important because the connector can only be inserted in one direction, and any mistake in the wiring would require full desoldering and rework.

Regarding cable identification:

- **External labeling is discouraged** for aesthetic and practical reasons.
- However, **internal labeling is suggested** to simplify future inspections, maintenance, or upgrades.
- Even basic internal wire markers or color-coded heat-shrink sleeves can be helpful, as long as they do not interfere with enclosure closure or IP sealing.

### Final Electrical Test

Before closing the enclosure and putting the system into service, it is advisable to:

- Perform a complete **continuity and isolation test** using a multimeter.
- Connect the system under **controlled power-up conditions**, and monitor voltage and current at the connector terminals.
- Only once all connections are verified and stable should the enclosure be sealed permanently.

> This approach ensures not only safe operation, but also avoids having to reopen and rework a fully cabled and soldered connector due to preventable mistakes.
