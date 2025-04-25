### 1. Introduction

The official Raspberry Pi 15W USB-C Power Supply (model **KSA-15E-051300HU**) is a highly optimized adapter, designed specifically to meet the strict power requirements of Raspberry Pi boards. A detailed teardown published by ChargerLAB highlights its robust architecture, precise voltage regulation, and high-quality components, making it an ideal reference for stable and reliable 5.1V power delivery.

In this project, we aimed to replicate the core principles of that original power adapter, but with one key difference: instead of operating from a 230V AC mains input, our version is designed to work with a **13.8V DC input**, commonly available in battery-based or mobile systems. This design allows seamless integration into environments where AC power is not guaranteed or where backup DC power is essential.

It is important to clarify that this power module is **not intended to replace** the official adapter under normal operation. The Raspberry Pi will continue to be powered through its USB-C port via the official 230V power adapter. Instead, this custom-built power supply acts as a **redundant backup source**, directly connected to the 5V and GND pins on the GPIO header.

## EN Preface

This project documents the development of a **continuous and secure power supply system** for a **Raspberry Pi 4**, integrated within a multifunction control unit.

The Raspberry Pi is powered using the **original USB-C power adapter**, in accordance with the recommendations of the **Raspberry Pi Foundation**, which advises the exclusive use of certified power supplies to ensure **electrical stability and proper operation**, even under high load conditions.

To guarantee **operational continuity during a blackout**, a **passive UPS** has been implemented, based on a secondary **13.8V DC** power supply provided by a **Mean Well** power unit, featuring automatic switching between mains power and a backup battery.

The system includes:
- A **dual power supply permanently connected** to the Raspberry:
  - **USB-C** (230V → official charger) for normal operation.
  - **GPIO (5V)** for backup power.
- A **fully passive and automatic** behavior: in case of a blackout, the secondary source activates **without switches or relays**, leveraging the inherent electrical characteristics of both circuits.

The result is a **stable, silent, and electronically transparent** system, where the Raspberry Pi **never shuts down** and **does not detect** the transition between the two power sources.

## STEP 1 – Input Stage

This section receives **13.8V DC** from a power supply with integrated UPS functionality, which automatically switches to battery power in the event of a blackout. The goal is to deliver a clean, stable, and protected voltage downstream, to power a converter module that supplies a Raspberry Pi 4. The components are arranged to ensure protection from short circuits, electromagnetic disturbances, and overcurrents—replicating the safety and stability of an official Raspberry charger, adapted to a 13.8V system.

---

### Components Used

#### 1. **Schottky Diode – 1N5822**
- **Type:** Schottky diode, 3A, 40V
- **Function:** Protects the circuit from reverse currents and prevents faults in the converter or downstream components from feeding back into the main line or affecting other devices in the control unit.
- **Reasoning:** The 1N5822 is a low forward voltage drop diode (~0.5V @ 3A), ideal for DC power lines. Its Schottky technology ensures fast switching and low losses, maintaining efficiency without compromising voltage stability.

---

#### 2. **Fuse – 0251005.MRT1L**
- **Type:** Non-resettable through-hole fuse
- **Specifications:** 5A, 125V
- **Function:** Protects against serious short circuits and overcurrents that could damage the converter or other system components.
- **Reasoning:** Rated to handle the Raspberry Pi 4's maximum load, including peak currents, without nuisance trips. Activates only in case of real faults, effectively safeguarding the entire downstream system.

---

#### 3. **Inductor – HTTI-22-6.7**
- **Type:** High-temperature toroidal inductor
- **Specifications:** 22 µH, 6.7 A
- **Function:** Series filtering of the power line, reducing high-frequency noise and attenuating transients. It serves as the first element of the LC filter stabilizing the line before the converter.
- **Reasoning:** High current handling, low resistance, high magnetic efficiency. The toroidal form minimizes EMI emissions—ideal for environments with sensitive loads.

---

#### 4. **Electrolytic Capacitor – EEU-FC1V471**
- **Type:** Panasonic FC radial electrolytic capacitor
- **Specifications:** 470 µF, 35V
- **Function:** Low-frequency filtering, ripple damping, and voltage stabilization at the input.
- **Reasoning:** High capacitance, low ESR, and a voltage rating well above 13.8V. Essential to absorb slow fluctuations and maintain power continuity.

---

#### 5. **Ceramic Capacitor – KAM21BR71H104JT**
- **Type:** MLCC ceramic capacitor, X7R, AEC-Q200
- **Specifications:** 0.1 µF, 50V, 0805 package
- **Function:** High-frequency filtering, spike suppression, and EMI noise rejection. Works in parallel with the electrolytic capacitor to complete the LC filter.
- **Reasoning:** The 50V rating ensures ample headroom over 13.8V. The X7R dielectric offers thermal stability, and the 0805 package provides robustness over smaller variants.

---

### Result

This series-parallel configuration forms a **complete LC filter** that is protected, stable, and reliable. It supplies the converter with clean and filtered DC voltage, ready to be stepped down to 5.1V, free from interference or electrical risks to the Raspberry Pi 4 or any other sensitive components.

## STEP 2 – Conversion Stage

In this phase, the filtered and protected input voltage (typically 13.0V–13.5V effective) is converted via a DC-DC step-down module into an adjustable voltage, which will be fine-tuned in the output stage. Voltage regulation is handled by a high-precision multi-turn trimmer connected to the converter’s TRIM pin.

---

### Components Used

#### 1. **Converter Module – OKX-T/5-D12N-C (Murata)**
- **Type:** Adjustable non-isolated DC-DC buck converter
- **Actual Specifications:**
  - **Operating input voltage:** 8.3V – 14.0V  
  - **Adjustable output voltage:** **0.591V – 5.5V**
  - **Maximum current:** up to 5A (depending on voltage and heat dissipation)
  - **Rated power:** 25W
- **Function:** Steps down and regulates the input voltage from 13.8V to a lower adjustable level via the TRIM pin.
- **Reasoning:** This converter is ideal for precise power delivery. It allows output tuning above 5.0V (up to 5.5V), which is essential to **compensate voltage drops** in the output section and ensure a stable 5.1V supply reaches the Raspberry Pi.

---

#### 2. **Trimmer – 3296W-1-103LF**
- **Type:** 10kΩ multi-turn vertical sealed trimmer
- **Function:** Connected to the converter’s TRIM pin, it allows fine adjustment of the output voltage.
- **Reasoning:** The goal is not to set the final desired voltage directly (e.g., 5.1V), but to **pre-compensate** for expected downstream losses so the final voltage at the Raspberry Pi is accurate. The multi-turn design enables millivolt-level precision over a broad and sensitive range.

---

### Technical Considerations

The selected Murata module provides a wide adjustment range that **comfortably includes and exceeds the 5.1V target**, which many other step-down converters cannot achieve. Its ability to operate up to 5.5V makes it an ideal choice in a power chain where compensation for downstream voltage drops is required. The trimmer + TRIM configuration ensures continuous and reliable adjustability—crucial for a mission-critical power supply.

## STEP 3 – Output – Phase 1

This section is designed to **refine, stabilize, and protect** the output voltage produced by the DC-DC converter before it is distributed to the Raspberry Pi 4. It is a crucial step to ensure that the 5.1V line is **filtered, noise-free, stable, and safeguarded** against any unexpected electrical events.

---

### Components Used

#### 1. **Electrolytic Capacitor – 860080374013**
- **Brand/Model:** Wurth WCAP-ATLI Series
- **Value:** 470 µF, 16V, 20% tolerance
- **Type:** Radial electrolytic capacitor
- **Function:** Stabilizes the output voltage by absorbing residual low-frequency ripple. It dampens slow oscillations and provides buffering for load spikes.
- **Reasoning:** High capacitance and a 16V rating provide a generous margin over the 5.1V line. The WCAP-ATLI series is renowned for its reliability and low ESR.

---

#### 2. **Ceramic Capacitor – KAM21BR71H104JT**
- **Value:** 0.1 µF, 50V, X7R dielectric, 5% tolerance
- **Package:** 0805
- **Function:** Filters high-frequency noise and EMI disturbances. Works synergistically with the electrolytic capacitor to ensure line cleanliness across the full spectrum.
- **Reasoning:** High voltage rating (50V) relative to the 5.1V line, excellent thermal stability thanks to the X7R dielectric, and mechanical robustness provided by the 0805 format—ideal for long-term reliable applications.

---

#### 3. **Bidirectional TVS Diode – 5KP5.0A**
- **Type:** TVS (Transient Voltage Suppression) protection diode
- **Nominal Voltage:** 5.0V (clamping ~6.4V), 543A peak pulse current
- **Polarity:** Bidirectional
- **Function:** Protects the output line against voltage surges, ESD discharges, inductive spikes, or hotplug events. It reacts instantly when the voltage exceeds the nominal threshold, preventing damage to the Raspberry Pi.
- **Reasoning:** Specifically designed for 5V lines. Bidirectional polarity ensures protection from disturbances in both directions. Its extremely high absorption capacity (up to 543A) makes it reliable even in critical scenarios.

---

### Electrical Configuration

All three components are connected in **parallel** between **VOUT+ and GND**, to:
- Work together to filter, stabilize, and protect the output
- Avoid introducing any voltage drops
- React passively and instantly to any variations or anomalies

---

### Objective of Phase 1

Deliver a **5.1V ±1% output line** ready for distribution, featuring:
- Low residual ripple
- Surge protection
- EMI reduction
- Stable behavior under dynamic loads

The **Phase 2** output will introduce an additional layer of directional control via a Schottky diode in series, which will be discussed separately.

---

## STEP 3 – Output – Phase 2 – Passive Dual Power Protection (Passive OR-ing)

After refining the output line (Phase 1), the circuit includes a key additional element:  
**a Schottky diode in series on the positive branch**, placed immediately before the connection to the Raspberry Pi.  
This component plays a critical role in managing the **permanent coexistence** of two distinct power sources:

- **Official 230V USB-C supply** (original Raspberry power adapter)
- **Backup regulated 5.1V line**, derived from the internal converter

---

### Component Used

#### **Schottky Diode – PMEG6030EP-QX**
- **Type:** High-temperature Schottky diode, 60V – 3A – SMD
- **Function:** Unidirectional protection for the DIPIN branch towards the Raspberry
- **Placement:** In series on the positive branch (VOUT+) of the internal circuit, **after** the output filter

---

### Concept of Passive OR-ing

This configuration is technically known as:

> **Passive diode OR-ing**

It operates on a simple and highly reliable principle:  
when two power supplies are **simultaneously** connected to a load (in this case, the Raspberry Pi),  
**the source with the slightly higher voltage "wins"**, while the other remains passive.

The Schottky diode ensures that:
- Current from the Raspberry **cannot flow back** into the backup converter
- The DIPIN branch **is not powered by the USB-C**
- In the event of a real blackout, the DIPIN branch takes over **automatically and instantly**

---

### Edge Case: UPS Malfunction

In a **worst-case scenario**, the UPS might incorrectly switch to battery even while 230V mains power is still present.  
Thus, both the USB-C and DIPIN sources would supply about 5.1V simultaneously.

Even in this situation:
- **No real double power feeding occurs**
- The Raspberry draws **current only from the source with the slightly higher voltage**
- Current flow remains **unidirectional**
- Passive OR-ing guarantees **no conflict or risk of damage**

The selection occurs **automatically, silently, and safely**, without bounces or unstable loops.  
The Schottky diode acts as a logical separator between the two sources.

---

### Conclusion

The inclusion of the PMEG6030EP-QX diode in series provides a simple and effective solution to:
- **Implement a redundant and safe power system**
- **Prevent harmful backfeeding**
- **Enable permanent simultaneous connection** of both power sources, without the need for switches or active controls

Thus, the Raspberry Pi is always powered by a **single active source**,  
even though both lines are **physically connected at the same time**.

## Appendix A – Technical Comparison with the Official Raspberry Pi Power Supply

This section compares the developed project with the original power adapter provided by the Raspberry Pi Foundation, focusing on **reliability**, **electrical continuity**, and **device protection**.

---

### Official Raspberry Pi Power Supply (USB-C, 5.1V 3A)

- **Nominal Voltage:** 5.1V ±5%
- **Maximum Power:** ~15W (continuous 3A)
- **Operation:** AC-DC switching power supply converting 230V to 5.1V
- **Advantages:**
  - Specifically designed for the required voltage
  - Direct compatibility with the Raspberry Pi’s USB-C connector
  - Built-in overcurrent and short-circuit protection
- **Limitations:**
  - **No redundancy**
  - No UPS functionality
  - No active protection during prolonged blackouts

---

### Customized Setup with 13.8V Line + Internal Converter

- **Final Output Voltage:** 5.1V regulated (with compensation)
- **Operation:** DC-DC UPS with 13.8V line, battery, and automatic switching
- **Redundancy:** Two permanently connected power sources (official USB-C + DIPIN)
- **Advanced Filtering:** Multiple capacitors + inductor + TVS protection
- **Active Protection:** Schottky diode for passive OR-ing (no backfeed)
- **Guaranteed Continuity:** No interruption even during 230V mains blackout
- **Thermal and Electrical Margin:** All components selected with wide safety margins relative to 5.1V and load

---

### Final Considerations

The customized system does not **replace** the official power supply **functionally**, but **complements** it. However, from an electrical perspective:

- It provides **enhanced protection against unexpected events**
- It ensures **operational continuity** in case of blackout (UPS functionality)
- It prevents any conflict through the **passive OR-ing system**
- It is designed with **carefully selected and safety-overrated components**

In conclusion, the configuration **outperforms the official charger** in terms of:
- **Flexibility**
- **Redundancy**
- **Resilience**

while maintaining full **electrical compatibility** with the Raspberry Pi.

## Appendix B – Safety and Electrical Continuity Considerations

This section analyzes the electrical mechanisms adopted to ensure:
- Isolation between power sources
- Continuous operation during interruptions
- Protection against unwanted current flows

---

### 1. Source Isolation

- The DIPIN circuit is separated from the USB-C line via a Schottky diode at the output.
- The diode prevents reverse current flow from the USB-C port back into the internal converter.
- There is no direct connection between the two positive lines.

---

### 2. Automatic Source Priority

- Both power sources (USB-C and DIPIN) remain connected simultaneously.
- Selection is automatic: the current is drawn from the source with the slightly higher instantaneous voltage.
- Under normal conditions, USB-C prevails. In the absence of mains power, the DIPIN line takes over.

---

### 3. Continuous Operation

- The 13.8V power supply is designed to switch to battery without any perceptible disruption.
- All downstream components tolerate minimal voltage variations during the transition.
- The load (Raspberry Pi) does not experience shutdowns or resets.

---

### 4. Prevention of Backfeed and Damage

- The output diode blocks any return current from the Raspberry Pi to the DIPIN branch.
- Current remains unidirectional under all conditions.
- The system is immune to actual dual power feeding.

---

### 5. Disturbance Protection

- The LC filter and output capacitors reduce both high- and low-frequency ripple and EMI.
- A bidirectional TVS diode absorbs any transient overvoltages on the 5V line.

---

### Summary

The configuration ensures:
- Electrical isolation between power lines
- Passive operational continuity
- No conflicts between sources
- Stable voltage even under non-ideal conditions

The logic is purely analog and requires no software management or active control components.

---

### 6. Electrical Continuity During Switching

The transition from mains to battery does not occur through relays or mechanical devices, but via internal electronic logic within the Mean Well module. This ensures a seamless and continuous transition.

#### a. Internal Capacitors in the Mean Well Module

According to the official manufacturer documentation, the internal capacitors guarantee a **hold-up time of 70 ms** at full load. This allows the module to maintain stable output voltage even during minor AC power interruptions, without noticeable drops downstream.

#### b. External Capacitors on the DIPIN Line

Downstream of the DC-DC converter, a **470 µF 16V** electrolytic capacitor is installed. Considering an estimated maximum load of **2.5 A**, and an acceptable maximum voltage drop of **ΔV = 0.2 V** (from 5.1V to 4.9V), the hold-up time can be calculated as:

`t = (C × ΔV) / I = (470 × 10^-6 × 0.2) / 2.5 = 0.0000376 s ≈ 38 ms`

#### c. Total Guaranteed Continuity

By combining the contribution of the Mean Well's internal capacitors with the external capacitor, the estimated total continuity time is:

**~108 ms**

This value exceeds the typical duration of network transients or unintended switching events, ensuring that the Raspberry Pi does not experience shutdowns or resets at any stage of the transition between mains power and battery backup.

## Appendix C – Predictive Analysis in Case of Failure (Electrical Logic)

This section evaluates the expected behavior of the system under fault conditions, based solely on the electrical structure of the project and the actually installed components. It is not based on experimental tests, but on analyses consistent with the real configuration.

---

### 1. DC-DC Converter Failure (OKX-T/5-D12N-C)

**Case:** The converter module suffers an internal failure, such as a short circuit between input and ground, or instability at the output.

**Expected behavior:**
- The **SS34 Schottky diode** in series before the converter prevents current from flowing back toward the main 13.8V line.
- The **0251005.MRT1L** (5A, 125V) through-hole fuse interrupts current in the event of abnormal consumption.
- The **HTTI-22-6.7** (22 µH, 6.7 A) inductor damps transients and protects upstream components.
- The fault is contained locally, without propagating to the Raspberry Pi or the main power supply.

---

### 2. Mean Well Module Malfunction (Incorrect Switching)

**Case:** The module erroneously switches to battery even though mains voltage is present, causing both power sources to be active simultaneously.

**Expected behavior:**
- The **PMEG6030EP-QX Schottky diode**, placed in series on the DIPIN output, prevents current from the USB-C line from flowing back into the backup branch.
- The Raspberry Pi is powered by the source with the slightly higher voltage.
- The system remains stable, with no interference between the two lines.

---

### 3. Impulse Overvoltage on the 5V Line

**Case:** A high-energy impulse or transient disturbance strikes the output line.

**Expected behavior:**
- The **5KP5.0A TVS diode** (bidirectional, ~6.4V clamping, 543A peak) instantly diverts the energy to ground.
- The Raspberry Pi is protected against brief surges, overvoltages, and electromagnetic disturbances.

---

### 4. Sudden 230V Mains Blackout

**Case:** The main USB-C power supply is suddenly interrupted.

**Expected behavior:**
- The Mean Well module automatically switches to battery power.
- The DIPIN branch takes over the Raspberry Pi supply.
- The Mean Well’s internal capacitors (hold-up time **70 ms**) and the external **470 µF** capacitor on the 5V line ensure a total estimated continuity of **~108 ms**.
- The Raspberry Pi remains powered without shutdowns or resets.

---

### 5. Simultaneous Active Power Sources

**Case:** Both power sources (USB-C and DIPIN) are connected and active simultaneously, with similar but not identical voltages.

**Expected behavior:**
- The DIPIN branch is isolated by the **PMEG6030EP-QX Schottky diode**, blocking any return towards the 13.8V supply.
- The USB-C branch, powered by the official Raspberry Pi 15W adapter (model KSA-15E-051300HU), **does not feature an output diode**, but uses an integrated synchronous rectifier (SP6536F), as evidenced by the ChargerLAB teardown:  
  [https://www.chargerlab.com/teardown-of-raspberry-pi-15w-usb-c-power-adapter-ksa-15e-051300hu](https://www.chargerlab.com/teardown-of-raspberry-pi-15w-usb-c-power-adapter-ksa-15e-051300hu)
- Thanks to ChargerLAB for publishing the complete device analysis, which made this technical evaluation possible.
- From the images and specifications, **no series diode** was found on the USB-C output, and no direct passive protection was detected on the VBUS line.
- However, in this project, **no modifications are made to the USB-C line**: it remains **unaltered**, maintaining the official adapter’s maximum stability and compatibility with the Raspberry Pi.
- The selection between sources occurs naturally: current flows only from the slightly higher voltage source. Even with minor differences, the system behaves predictably and stably.

---

### Conclusion

The adopted electrical structure ensures that faults are contained locally, avoids conflicts between power lines, securely handles abnormal events, and guarantees operational continuity for the Raspberry Pi. All protections are passive, reliable, and based on real components, with no need for digital control or external logic.

---

## Appendix D – Technical Considerations on Selected Components

### Operating Tolerances of the Raspberry Pi 4 (VBUS Input)

The Raspberry Pi 4 Model B is designed to receive power via the USB-C connector at a nominal 5.1V. According to the official technical documentation, the safe operational voltage range for VBUS is:

- **Minimum guaranteed voltage:** 4.75V  
- **Recommended nominal value:** 5.10V  
- **Maximum recommended voltage:** 5.25V

Voltages below 4.75V may cause instability, subsystem malfunctions (especially USB and HDMI), or unwanted resets. Voltages above 5.25V may compromise the integrity of sensitive circuits.  
Therefore, the entire secondary power architecture has been calibrated to ensure that, even accounting for passive component voltage drops, the voltage at the Raspberry Pi’s power input remains within the specified safe operating range.

---

### 1. Electrolytic Capacitor – 860080374013 (470 µF, 16V, ±20%)

This 470 µF electrolytic capacitor is installed at the DIPIN output, in parallel with a ceramic capacitor. The ±20% tolerance results in an actual capacitance between 376 µF and 564 µF. In 5V line stabilization applications, this range is more than acceptable. The capacitor provides a charge reservoir to absorb slow variations or moderate current transients.  
The 16V nominal voltage offers a large safety margin over the 5.1V working voltage, enhancing component longevity and operational safety.

---

### 2. Ceramic Capacitor – KAM21BR71H104JT (0.1 µF, 50V, X7R, ±5%)

This multilayer ceramic capacitor is mounted in parallel with the electrolytic capacitor and serves to filter high-frequency components. The tight ±5% tolerance ensures stable capacitance between 0.095 µF and 0.105 µF, consistent with its EMI filtering role. The X7R dielectric provides thermal stability and good long-term capacitance consistency. Its 50V rating is more than sufficient for the operating voltage, offering additional protection against voltage spikes.

---

### 3. Resistive Trimmer – 3296W-1-103LF (10kΩ, Multi-Turn)

The 10kΩ trimmer is used for fine adjustment of the DC-DC converter (OKX-T/5-D12N-C). Being a multi-turn component, it allows precise output voltage tuning, necessary to compensate for drops due to passive components, particularly the output Schottky diode. The exact resistive value is not critical; the focus is on its fine adjustment capability.

---

### 4. Schottky Diode – PMEG6030EP-QX (60V, 3A, Vf typ. 0.25V)

This diode is mounted in series on the DIPIN output, just before the Raspberry Pi’s input. Its role is to block any reverse current flow back toward the backup line when the USB-C source is active. The low typical forward voltage drop (0.25V at 2A) helps maintain the output voltage above the 4.75V minimum threshold. The diode was selected for its combination of efficiency, fast response, and high continuous current capacity. This passive isolation is one of the key elements of the system’s electrical protection.

---

### 5. Toroidal Inductor – HTTI-22-6.7 (22 µH, 6.7 A)

This toroidal inductor is installed in series on the 13.8V positive input line. It is part of an LC filter designed to reduce noise and protect the DC-DC converter. The 22 µH value was chosen to harmonize with the parallel capacitors, while the 6.7 A continuous current rating provides a wide safety margin. The toroidal structure minimizes radiation losses, contributing to the system’s electromagnetic compatibility.

---

### 6. TVS Diode – 5KP5.0A (Bidirectional Clamping, 5Vso, 543A Peak)

The 5KP5.0A TVS diode is placed on the 5V output line for transient surge protection. It can withstand up to 543A peak in an 8/20 µs pulse. Its clamping voltage (~6.4V) is appropriate for shunting disturbances without activating during normal conditions. Being bidirectional, it protects against both positive and negative spikes. It is a fundamental component for robustness against transient events, particularly in environments subject to electromagnetic or inductive disturbances.

---

## ITA Prefazione

Questo progetto documenta la realizzazione di un sistema di alimentazione **continua e sicura** per un **Raspberry Pi 4**, integrato all'interno di una centralina multifunzione.

Il Raspberry Pi è stato alimentato **con il caricabatterie originale via USB-C**, in linea con le raccomandazioni della **Raspberry Pi Foundation**, che consiglia l’uso esclusivo di alimentatori certificati per garantire **stabilità elettrica e corretto funzionamento** anche sotto carichi elevati.

Per garantire la **continuità operativa in caso di blackout**, è stato implementato un **UPS passivo**, basato su una seconda alimentazione a **13.8V DC**, erogata da un alimentatore **Mean Well** con funzione automatica di switch tra rete elettrica e batteria tampone.

Il sistema prevede:
- Una **doppia alimentazione fisicamente sempre connessa** al Raspberry:
  - **USB-C** (230V → caricatore ufficiale) per il funzionamento ordinario.
  - **GPIO (5V)** per l’alimentazione di backup.
- Un comportamento **completamente passivo** e automatico: in caso di blackout, la fonte secondaria si attiva **senza interruttori o relè**, sfruttando le normali proprietà elettriche dei due circuiti.

Il risultato è un sistema **stabile, silenzioso e invisibile** dal punto di vista elettronico, dove il Raspberry non si spegne mai e non percepisce la transizione tra le due fonti.

## STEP 1 – Ingresso

Questa sezione riceve la tensione continua da **13.8V DC**, proveniente da un alimentatore con funzione UPS che commuta automaticamente su batteria in caso di blackout. L’obiettivo è fornire una linea pulita, stabile e protetta a valle, per alimentare un modulo converter che alimenta un Raspberry Pi 4. I componenti sono disposti in modo da garantire protezione da cortocircuiti, disturbi elettromagnetici e sovracorrenti, replicando la sicurezza e stabilità tipiche di un caricatore ufficiale Raspberry, ma adattate a un sistema su 13.8V.

---

### Componenti utilizzati

#### 1. **Diodo Schottky – 1N5822**
- **Tipo:** Diodo Schottky 3A, 40V
- **Funzione:** Protegge il circuito da correnti inverse e impedisce che eventuali guasti nel converter o in uscita si riflettano sulla linea principale o su altri dispositivi della centralina.
- **Motivazione:** Il diodo 1N5822 è un componente a bassa caduta di tensione (tipicamente ~0.5V @ 3A), adatto a linee di potenza DC. La sua tecnologia Schottky consente una risposta rapida e basse perdite, garantendo efficienza senza compromettere la stabilità della tensione a valle.

---

#### 2. **Fusibile – 0251005.MRT1L**
- **Tipo:** Fusibile a foro passante non resettabile
- **Specifiche:** 5A, 125V
- **Funzione:** Protezione contro cortocircuiti gravi e sovracorrenti che potrebbero danneggiare il convertitore o altri componenti del sistema.
- **Motivazione:** Valore dimensionato per supportare il carico massimo del Raspberry Pi 4, inclusi i picchi, senza falsi interventi. Interviene solo in caso di guasti reali, proteggendo efficacemente tutto il sistema a valle.

---

#### 3. **Induttore – HTTI-22-6.7**
- **Tipo:** Induttore toroidale ad alta temperatura
- **Specifiche:** 22 µH, 6.7 A
- **Funzione:** Filtraggio in serie della linea di alimentazione, per ridurre disturbi ad alta frequenza e attenuare transitori. È il primo elemento del filtro LC che stabilizza la linea prima del converter.
- **Motivazione:** Elevata capacità di corrente, bassa resistenza, alta efficienza magnetica. Il formato toroidale riduce le emissioni EMI. Perfetto per ambienti con carichi sensibili.

---

#### 4. **Condensatore elettrolitico – EEU-FC1V471**
- **Tipo:** Condensatore elettrolitico radiale Panasonic FC
- **Specifiche:** 470 µF, 35V
- **Funzione:** Filtraggio delle basse frequenze, smorzamento di ripple e stabilizzazione della tensione in ingresso.
- **Motivazione:** Elevata capacità, bassa ESR, tensione ampiamente superiore a 13.8V. Essenziale per garantire continuità e assorbire variazioni lente sulla linea.

---

#### 5. **Condensatore ceramico – KAM21BR71H104JT**
- **Tipo:** MLCC ceramico, X7R, AEC-Q200
- **Specifiche:** 0.1 µF, 50V, formato 0805
- **Funzione:** Filtraggio delle alte frequenze, spike e interferenze EMI. Lavora in parallelo al condensatore elettrolitico per completare il filtro LC.
- **Motivazione:** La tensione di 50V garantisce ampio margine operativo rispetto ai 13.8V. Il dielettrico X7R assicura stabilità termica e il formato 0805 offre maggiore robustezza rispetto a versioni più compatte.

---

### Risultato

Questa configurazione in serie e parallelo realizza un **filtro LC completo**, protetto, stabile e affidabile. Fornisce al converter una tensione continua e filtrata, pronta per essere trasformata a 5.1V, senza interferenze o rischi elettrici per il Raspberry Pi 4 o per altri componenti sensibili.



## STEP 2 – Trasformazione

In questa fase la tensione in ingresso, dopo il filtraggio e la protezione (tipicamente 13.0V–13.5V effettivi), viene convertita tramite un modulo DC-DC step-down in una tensione regolabile, che sarà poi rifinita nella fase di uscita. La regolazione è affidata a un trimmer multigiro ad alta precisione, collegato al pin TRIM del convertitore.

---

### Componenti utilizzati

#### 1. **Modulo converter – OKX-T/5-D12N-C (Murata)**
- **Tipo:** Convertitore DC-DC buck regolabile, non isolato
- **Specifiche tecniche reali:**
  - **Tensione di ingresso operativa:** 8.3V – 14.0V
  - **Tensione d’uscita regolabile:** **0.591V – 5.5V**
  - **Corrente massima:** fino a 5A (in funzione della tensione e dissipazione)
  - **Potenza nominale:** 25W
- **Funzione:** Riduce e regola la tensione da 13.8V verso un valore più basso, adattabile tramite il pin TRIM.
- **Motivazione:** Questo convertitore è ideale per alimentazioni precise, permette regolazioni sopra i 5.0V (fino a 5.5V), necessarie per compensare le cadute di tensione nella sezione di uscita, garantendo un arrivo corretto di 5.1V al Raspberry.

---

#### 2. **Trimmer – 3296W-1-103LF**
- **Tipo:** Trimmer resistivo multigiro, 10kΩ, verticale, sigillato
- **Funzione:** Collegato al pin TRIM del converter, consente la regolazione fine della tensione d’uscita.
- **Motivazione:** Non si imposta direttamente il valore finale desiderato (es. 5.1V), ma si **compensa in anticipo** la perdita prevista nei componenti successivi, in modo che la tensione finale all'arrivo risulti corretta. Il trimmer multigiro garantisce precisione millivolt su un range ampio e sensibile.

---

### Considerazioni tecniche

Il modulo Murata selezionato consente una regolazione sufficientemente ampia da **coprire e superare i 5.1V desiderati**, cosa che non tutti i moduli step-down offrono. La possibilità di operare fino a 5.5V lo rende perfettamente adatto in una catena che richiede una compensazione di perdita a valle. La configurazione trimmer + TRIM garantisce regolabilità continua e affidabile, fondamentale per un’alimentazione critica.

## STEP 3 – Uscita – Fase 1

Questa sezione ha lo scopo di **rifinire, stabilizzare e proteggere** la tensione in uscita prodotta dal convertitore DC-DC, prima che venga distribuita al Raspberry Pi 4. È un passaggio fondamentale per assicurare che la linea da 5.1V sia **filtrata, priva di disturbi, stabile e protetta** da eventuali eventi elettrici imprevisti.

---

### Componenti utilizzati

#### 1. **Condensatore elettrolitico – 860080374013**
- **Marca/Modello:** Wurth WCAP-ATLI Series
- **Valore:** 470 µF, 16V, tolleranza 20%
- **Tipo:** Condensatore elettrolitico radiale
- **Funzione:** Stabilizza la tensione in uscita assorbendo ripple residui a bassa frequenza. Riduce le oscillazioni lente e contribuisce all’effetto tampone per picchi di carico.
- **Motivazione:** La capacità elevata e la tensione nominale di 16V offrono margine abbondante su una linea da 5.1V. La serie WCAP-ATLI è nota per affidabilità e bassa ESR.

---

#### 2. **Condensatore ceramico – KAM21BR71H104JT**
- **Valore:** 0.1 µF, 50V, X7R, tolleranza 5%
- **Formato:** 0805
- **Funzione:** Filtra le alte frequenze e i disturbi EMI. Lavora in sinergia con il condensatore elettrolitico per garantire pulizia della linea su tutto lo spettro.
- **Motivazione:** Tensione nominale elevata (50V) rispetto alla linea da 5.1V, ottima stabilità termica grazie al dielettrico X7R, robustezza meccanica garantita dal formato 0805. Ideale per applicazioni affidabili a lunga durata.

---

#### 3. **Diodo TVS bidirezionale – 5KP5.0A**
- **Tipo:** Diodo di protezione TVS (Transient Voltage Suppression)
- **Valore nominale:** 5.0V (clamping ~6.4V), 543A di corrente impulsiva
- **Polarità:** Bidirezionale
- **Funzione:** Protegge la linea d’uscita da sovratensioni impulsive, scariche elettrostatiche, spike induttivi o hotplug. Interviene istantaneamente se la tensione supera la soglia nominale, evitando danni al Raspberry.
- **Motivazione:** È specificamente progettato per linee a 5V. La polarità bidirezionale protegge da disturbi in entrambe le direzioni. Altissima capacità di assorbimento (fino a 543A) lo rende affidabile anche in situazioni critiche.

---

### Configurazione elettrica

Tutti e tre i componenti sono collegati in **parallelo** tra **VOUT+ e GND**, in modo da:

- Lavorare in sinergia per filtrare, stabilizzare e proteggere
- Non introdurre cadute di tensione
- Reagire passivamente e in tempo reale a qualsiasi variazione o anomalia della linea

---

### Obiettivo della Fase 1

Fornire una **linea d’uscita da 5.1V ±1%** pronta per la distribuzione, con:
- Basso ripple residuo
- Protezione da sovratensioni
- Riduzione EMI
- Comportamento stabile sotto carico dinamico

La **fase 2** di uscita introdurrà un ulteriore livello di controllo direzionale attraverso un diodo Schottky in serie, che vedremo separatamente.

## STEP 3 – Uscita – Fase 2 – Protezione da doppia alimentazione (OR-ing passivo)

Dopo la rifinitura della linea di uscita (fase 1), il circuito include un ulteriore elemento fondamentale:  
**un diodo Schottky in serie sul ramo positivo**, immediatamente prima del collegamento verso il Raspberry Pi.  
Questo componente ha la funzione critica di gestire la coesistenza **permanente** di due alimentazioni distinte:

- **USB-C ufficiale da 230V** (alimentatore Raspberry originale)
- **Linea regolata backup da 5.1V**, derivata dal converter interno

---

### Componente utilizzato

#### **Diodo Schottky – PMEG6030EP-QX**
- **Tipo:** Schottky ad alta temperatura, 60V – 3A – SMD
- **Funzione:** Protezione unidirezionale del ramo DIPIN verso il Raspberry
- **Posizionamento:** In serie sul ramo positivo (VOUT+) del circuito interno, **dopo** il filtro di uscita

---

### Concetto di OR-ing passivo

Questa configurazione è tecnicamente definita come:

> **OR-ing passivo a diodo**

Funziona secondo un principio semplice e affidabile:  
quando due alimentazioni sono collegate **simultaneamente** a un carico (in questo caso il Raspberry Pi),  
**la sorgente con tensione leggermente più alta "vince"**, mentre l’altra resta passiva.

Il diodo Schottky garantisce che:
- La corrente del Raspberry **non possa fluire all’indietro** verso il convertitore backup
- Il ramo DIPIN **non venga alimentato dalla USB-C**
- In caso di blackout reale, il ramo DIPIN subentra **automaticamente e istantaneamente**

---

### Caso anomalo: malfunzionamento dell’UPS

In un **caso limite**, l’UPS potrebbe erroneamente passare alla batteria anche se la 230V è ancora attiva.  
Quindi entrambe le fonti USB-C e DIPIN fornirebbero simultaneamente circa 5.1V.

Anche in questa situazione:
- **Non si genera una doppia alimentazione reale**
- Il Raspberry riceve **corrente solo dalla fonte con tensione leggermente più alta**
- Il comportamento della corrente è sempre **unidirezionale**
- L’OR-ing passivo garantisce che **non vi sia conflitto né rischio di danneggiamento**

La selezione avviene **in modo automatico, silenzioso e sicuro**, senza rimbalzi o loop instabili.  
Il diodo Schottky lavora come separatore logico tra le due fonti.

---

### Conclusione

L’inserimento del diodo PMEG6030EP-QX in serie costituisce una soluzione semplice ed efficace per:
- **Realizzare un sistema di alimentazione ridondante e sicuro**
- **Evitare ritorni di corrente dannosi**
- **Permettere l’alimentazione simultanea permanente**, senza necessità di interruttori o controlli attivi

Il Raspberry Pi viene così alimentato sempre da una **singola fonte attiva**,  
pur avendo entrambe le linee **fisicamente collegate in contemporanea**.

## Appendice A – Confronto tecnico con il caricatore ufficiale Raspberry Pi

Questa sezione confronta il progetto sviluppato con il caricatore originale fornito dalla Raspberry Pi Foundation, considerando **affidabilità**, **continuità elettrica** e **protezione del dispositivo**.

---

### Caricatore ufficiale Raspberry Pi (USB-C, 5.1V 3A)

- **Tensione nominale:** 5.1V ±5%
- **Potenza massima:** ~15W (3A continui)
- **Funzionamento:** Alimentatore switching AC-DC da 230V a 5.1V
- **Vantaggi:**
  - Appositamente progettato per la tensione richiesta
  - Compatibilità diretta con il connettore USB-C del Raspberry
  - Protezione integrata da sovracorrente e corto
- **Limiti:**
  - **Non è ridondante**
  - Nessuna funzione UPS
  - Nessuna protezione attiva in caso di black-out prolungato

---

### Configurazione personalizzata con linea 13.8V + converter interno

- **Tensione in uscita finale:** 5.1V regolata (compensata)
- **Funzionamento:** UPS DC-DC con linea 13.8V, batteria e commutazione automatica
- **Ridondanza:** Due alimentazioni permanenti (USB-C ufficiale + DIPIN)
- **Filtraggio avanzato:** Condensatori multipli + induttore + TVS
- **Protezione attiva:** Diodo Schottky per OR-ing passivo (nessun backfeed)
- **Continuità garantita:** Nessuna interruzione anche in caso di black-out 230V
- **Margine termico ed elettrico:** Tutti i componenti scelti con ampio margine rispetto a 5.1V e al carico

---

### Considerazioni finali

Il sistema personalizzato non sostituisce **funzionalmente** il caricatore ufficiale, ma lo **affianca**. Tuttavia, dal punto di vista elettrico:

- Offre **maggiore protezione contro eventi imprevisti**
- Garantisce **continuità operativa** in caso di blackout (funzione UPS)
- Evita ogni tipo di conflitto grazie al **sistema OR-ing passivo**
- È progettato con componenti selezionati e **sovradimensionati in sicurezza**

In conclusione, la configurazione **è superiore al caricatore ufficiale** in termini di:
- **Flessibilità**
- **Ridondanza**
- **Resilienza**

Pur mantenendo la stessa compatibilità elettrica finale con il Raspberry Pi.

## Appendice B – Considerazioni di sicurezza e continuità elettrica

Questa sezione analizza i meccanismi elettrici adottati per garantire:
- Isolamento tra le fonti di alimentazione
- Continuità operativa in presenza di interruzioni
- Protezione contro flussi di corrente indesiderati

---

### 1. Isolamento tra fonti

- La linea proveniente dal circuito DIPIN è separata da quella USB-C tramite diodo Schottky in uscita.
- Il diodo impedisce flussi di corrente inversi dalla porta USB-C verso il convertitore interno.
- Non esiste connessione diretta tra i due positivi.

---

### 2. Priorità automatica della fonte

- Le due alimentazioni (USB-C e DIPIN) restano collegate simultaneamente.
- La selezione è automatica: la corrente proviene dalla fonte con tensione istantanea leggermente più alta.
- In condizioni nominali, prevale la USB-C. In assenza di rete, subentra la linea DIPIN.

---

### 3. Continuità operativa

- L’alimentatore a 13.8V è progettato per commutare su batteria senza discontinuità percepibile.
- Tutti i componenti a valle tollerano variazioni di tensione minime durante la transizione.
- Il carico (Raspberry) non subisce spegnimenti o reset.

---

### 4. Prevenzione di ritorni e danni

- Il diodo in uscita blocca qualsiasi ritorno dal Raspberry verso il ramo DIPIN.
- La corrente resta unidirezionale in tutte le condizioni.
- Il sistema è immune da doppie alimentazioni effettive.

---

### 5. Protezione da disturbi

- Il filtro LC e i condensatori in uscita riducono ripple e interferenze ad alta e bassa frequenza.
- Un diodo TVS bidirezionale assorbe eventuali sovratensioni impulsive sulla linea 5V.

---

### Sintesi

La configurazione garantisce:
- Isolamento elettrico tra linee
- Continuità operativa passiva
- Nessun conflitto tra sorgenti
- Tensione stabile anche in condizioni non ideali

La logica è esclusivamente analogica e non richiede gestione software o componenti attivi.

### 6. Continuità elettrica durante la commutazione

Il passaggio da rete a batteria non avviene tramite relè o dispositivi meccanici, ma attraverso una logica elettronica interna al modulo Mean Well. Questo consente una transizione trasparente e continua.

#### a. Condensatori interni al Mean Well

Secondo la documentazione ufficiale del produttore, i condensatori interni garantiscono un hold-up time di **70 ms** a pieno carico. Questo consente al modulo di mantenere la tensione di uscita stabile anche durante microinterruzioni dell’alimentazione AC, senza cadute percepibili a valle.

#### b. Condensatori esterni sulla linea DIPIN

A valle del convertitore DC-DC, è presente un condensatore elettrolitico da **470 µF 16V**. Considerando un carico massimo stimato pari a **2.5 A**, e una tolleranza massima accettabile di **ΔV = 0.2 V** (da 5.1V a 4.9V), il tempo di sostegno è calcolabile come segue:

`t = (C × ΔV) / I = (470 × 10^-6 × 0.2) / 2.5 = 0.0000376 s ≈ 38 ms`

#### c. Totale di continuità garantita

Combinando il contributo dei condensatori interni del Mean Well con quello del condensatore esterno si ottiene un tempo totale di continuità stimato pari a:

**~108 ms**

Questo valore è superiore alla durata tipica di transitori di rete o commutazioni non intenzionali, e garantisce che il Raspberry Pi non subisca spegnimenti o reset in nessuna fase di passaggio tra rete e batteria.

## Appendice C – Analisi previsionale in caso di guasto (logica elettrica)

Questa sezione valuta il comportamento atteso del sistema in presenza di guasti, utilizzando esclusivamente la struttura elettrica del progetto e i componenti effettivamente installati. Non si basa su test sperimentali, ma su analisi coerenti con la configurazione reale.

---

### 1. Guasto del convertitore DC-DC (OKX-T/5-D12N-C)

**Caso:** Il modulo convertitore presenta un guasto interno, ad esempio un cortocircuito tra ingresso e massa, o instabilità sull'uscita.

**Comportamento atteso:**
- Il diodo Schottky **SS34** in ingresso, montato in serie prima del converter, impedisce il ritorno della corrente verso la linea principale a 13.8V.
- Il fusibile a foro passante **0251005.MRT1L** (5A, 125V) interrompe la corrente in caso di assorbimento anomalo.
- L’induttore **HTTI-22-6.7** (22 µH, 6.7 A) smorza transitori e protegge i componenti a monte.
- Il guasto viene contenuto localmente, senza propagarsi né verso il Raspberry né verso l’alimentatore principale.

---

### 2. Malfunzionamento del modulo Mean Well (commutazione errata)

**Caso:** Il modulo commuta erroneamente su batteria, pur essendo presente la tensione di rete, causando l’attivazione simultanea delle due alimentazioni.

**Comportamento atteso:**
- Il diodo Schottky **PMEG6030EP-QX**, posto in serie sull’uscita DIPIN, impedisce che la corrente proveniente dalla linea USB-C fluisca all’indietro nel ramo backup.
- L’alimentazione del Raspberry proviene dalla fonte con tensione leggermente più alta.
- Il sistema rimane stabile: nessuna interferenza tra le due linee.

---

### 3. Sovratensione impulsiva sulla linea 5V

**Caso:** Un disturbo di tipo impulsivo o transitorio ad alta energia colpisce la linea di uscita.

**Comportamento atteso:**
- Il diodo TVS **5KP5.0A** (bidirezionale, clamping ~6.4V, 543 A di picco) devia immediatamente l’energia verso GND.
- Il Raspberry è protetto contro picchi brevi, sovratensioni e interferenze elettromagnetiche.

---

### 4. Blackout improvviso della rete 230V

**Caso:** L’alimentazione principale USB-C viene a mancare improvvisamente.

**Comportamento atteso:**
- Il modulo Mean Well passa automaticamente all’alimentazione da batteria.
- Il ramo DIPIN prende in carico l’alimentazione del Raspberry.
- I condensatori interni del Mean Well (hold-up time **70 ms**) e il condensatore da **470 µF** sulla linea 5V esterna garantiscono un totale stimato di **~108 ms** di continuità elettrica.
- Il Raspberry rimane alimentato senza subire interruzioni o reset.

---

### 5. Differenza tra due alimentazioni simultanee

**Caso:** Le due fonti di alimentazione (USB-C e DIPIN) risultano collegate contemporaneamente e attive, con tensioni simili ma non identiche.

**Comportamento atteso:**
- Il ramo DIPIN è isolato tramite il diodo Schottky **PMEG6030EP-QX**, che blocca qualsiasi ritorno verso l'alimentatore a 13.8V.
- Il ramo USB-C, fornito dall’alimentatore ufficiale Raspberry Pi da 15W (modello KSA-15E-051300HU), **non presenta un diodo in uscita**, ma utilizza un rettificatore sincrono integrato (SP6536F), come evidenziato nel teardown realizzato da ChargerLAB:  
  [https://www.chargerlab.com/teardown-of-raspberry-pi-15w-usb-c-power-adapter-ksa-15e-051300hu](https://www.chargerlab.com/teardown-of-raspberry-pi-15w-usb-c-power-adapter-ksa-15e-051300hu)
- Si ringrazia il team ChargerLAB per aver pubblicato l’analisi completa del dispositivo, che ha reso possibile la valutazione tecnica dell’alimentatore Raspberry.
- Dalle immagini e dalle specifiche visibili, **non è presente un diodo in serie sull’uscita USB-C**, e non è stata rilevata alcuna protezione passiva diretta sulla linea VBUS.
- Tuttavia, in questo progetto **non si apporta alcuna modifica alla linea USB-C**: è stata **volutamente lasciata invariata**, senza aggiunte in serie, per mantenere l’alimentatore ufficiale nella sua forma originale, garantendo la massima stabilità e compatibilità con il Raspberry Pi.
- La selezione tra le due fonti avviene naturalmente: la corrente fluisce esclusivamente dalla sorgente con tensione più alta. Anche in presenza di differenze minime, il sistema si comporta in modo prevedibile e stabile.

---

### Conclusione

La struttura elettrica adottata consente di contenere i guasti localmente, evitare conflitti tra linee di alimentazione, gestire in modo sicuro eventi anomali e garantire la continuità operativa del Raspberry. Le protezioni sono tutte passive, affidabili e basate su componenti reali, senza necessità di controllo digitale o logica esterna.

## Appendice D – Considerazioni tecniche sui componenti selezionati

### Tolleranze operative del Raspberry Pi 4 (ingresso VBUS)

Il Raspberry Pi 4 Model B è progettato per ricevere alimentazione tramite connettore USB-C con una tensione nominale di 5.1 V. Secondo la documentazione tecnica ufficiale, l’intervallo operativo sicuro della tensione VBUS è il seguente:

- **Tensione minima garantita:** 4.75 V  
- **Valore nominale consigliato:** 5.10 V  
- **Tensione massima raccomandata:** 5.25 V

Tensioni inferiori a 4.75 V possono causare instabilità, malfunzionamenti nei sottosistemi (in particolare USB e HDMI), o riavvii indesiderati. Tensioni superiori a 5.25 V possono compromettere l’integrità dei circuiti sensibili.  
Per questo motivo, l’intera architettura dell’alimentazione secondaria è stata calibrata per garantire che, anche tenendo conto delle cadute di tensione nei componenti passivi, la tensione all’ingresso del Raspberry Pi resti costantemente all’interno del margine operativo previsto.

---

### 1. Condensatore elettrolitico – 860080374013 (470 µF, 16V, ±20%)

Questo condensatore elettrolitico da 470 µF è installato in uscita sul ramo DIPIN, in parallelo con un condensatore ceramico. La tolleranza di ±20% comporta una capacità effettiva compresa tra 376 µF e 564 µF. In applicazioni di stabilizzazione della linea 5V, tale intervallo è ampiamente accettabile. Il componente ha il compito di fornire riserva di carica per assorbire variazioni lente o transitori moderati di corrente.  
La tensione nominale di 16 V garantisce un margine elevato rispetto alla tensione di lavoro di 5.1 V, favorendo la longevità del componente e la sicurezza operativa.

---

### 2. Condensatore ceramico – KAM21BR71H104JT (0.1 µF, 50V, X7R, ±5%)

Questo condensatore ceramico multistrato è montato in parallelo al condensatore elettrolitico e funge da filtro per le componenti ad alta frequenza. La tolleranza stretta (±5%) assicura una capacità stabile compresa tra 0.095 µF e 0.105 µF, coerente con il ruolo di filtraggio EMI. Il dielettrico X7R garantisce stabilità termica e una buona costanza della capacità nel tempo. La tensione nominale di 50 V è più che sufficiente per la tensione in gioco, offrendo ampia protezione contro eventuali picchi.

---

### 3. Trimmer resistivo – 3296W-1-103LF (10kΩ, multigiro)

Il trimmer da 10kΩ è utilizzato per la regolazione fine del convertitore DC-DC (OKX-T/5-D12N-C). Essendo un componente multigiro, consente regolazioni precise della tensione di uscita, necessarie per compensare le cadute dovute ai componenti passivi, in particolare il diodo Schottky in uscita. La regolazione non ha lo scopo di fissare esattamente 5.1 V in uscita al modulo, ma di garantire che dopo tutte le perdite, il valore effettivo al pin di alimentazione del Raspberry risulti nel range desiderato. La tolleranza del valore resistivo nominale non è critica, poiché l'importanza risiede nella capacità di taratura.

---

### 4. Diodo Schottky – PMEG6030EP-QX (60 V, 3 A, Vf tip. 0.25 V)

Questo diodo è montato in uscita sul ramo DIPIN, immediatamente prima dell’alimentazione del Raspberry. La sua funzione è bloccare qualsiasi ritorno di corrente verso la linea backup in presenza di una tensione USB-C attiva. La bassa caduta diretta tipica (0.25 V a 2 A) consente di mantenere la tensione di uscita al di sopra della soglia minima di 4.75 V. Il diodo è stato selezionato per la sua combinazione di efficienza, risposta rapida e capacità di corrente continua elevata. L’isolamento passivo garantito da questo componente è uno degli elementi chiave della protezione elettrica del sistema.

---

### 5. Induttore toroidale – HTTI-22-6.7 (22 µH, 6.7 A)

Questo induttore toroidale è installato in serie sul ramo positivo 13.8V, nella sezione di ingresso. Fa parte di un filtro LC progettato per ridurre i disturbi e proteggere il convertitore DC-DC. Il valore di 22 µH è stato scelto per armonizzarsi con i condensatori in parallelo, mentre la capacità di corrente continua (6.7 A) offre un ampio margine di sicurezza. La struttura toroidale minimizza le perdite per irraggiamento, contribuendo alla compatibilità elettromagnetica del sistema.

---

### 6. Diodo TVS – 5KP5.0A (clamping bidirezionale, 5 Vso, 543 A peak)

Il diodo TVS 5KP5.0A è posto sulla linea 5V in uscita per la protezione contro sovratensioni impulsive. È in grado di sopportare fino a 543 A di picco in configurazione 8/20 µs. La tensione di clamping (circa 6.4 V) è adeguata per deviare i disturbi senza attivarsi in condizioni normali. Essendo bidirezionale, protegge sia da spike positivi sia negativi. È un componente fondamentale per la robustezza contro eventi transitori, in particolare in ambienti soggetti a disturbi elettromagnetici o induttivi.
