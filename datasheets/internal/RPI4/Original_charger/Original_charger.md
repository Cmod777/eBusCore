# Teardown of Raspberry Pi 15W USB-C Power Adapter (KSA-15E-051300HU)

**Original source**: [ChargerLAB](https://www.chargerlab.com/teardown-of-raspberry-pi-15w-usb-c-power-adapter-ksa-15e-051300hu/)  
**Author**: Joey – ChargerLAB Team  
**Date**: July 21, 2023

> **Disclaimer**  
> The following content is a direct quotation from a publicly accessible article published by ChargerLAB.  
> It is reproduced here solely for documentation and reference purposes, with full credit and source link clearly provided.  
> We do not claim authorship or ownership of the material, and no copyright infringement is intended.  
> All rights remain with the original author(s) and ChargerLAB.  
> Please refer to the original publication at: [https://www.chargerlab.com/teardown-of-raspberry-pi-15w-usb-c-power-adapter-ksa-15e-051300hu/](https://www.chargerlab.com/teardown-of-raspberry-pi-15w-usb-c-power-adapter-ksa-15e-051300hu/)
---

## Introduction

As a fan of ChargerLAB, you probably know that the Raspberry Pi has become a go-to choice for tech enthusiasts, hobbyists, and professionals in the realm of computing and DIY projects. Its versatility and compact design make it a favorite among users worldwide. However, often overlooked is the essential component that powers this remarkable mini-computer – the Raspberry Pi power adapter.

Recently, we obtained an original USB-C power adapter for the Raspberry Pi 4. Curious to see the level of craftsmanship behind this small device? Let's delve into it and discover its construction quality together!

---

## Product Appearance

This power adapter uses a pure white cube design with matte surface.  
And the classic Raspberry Pi logo is located on the top.  
All specs info is printed below the two-prong plug. Model is **KSA-15E-051300HU**.  
It can support input of **100-240V~50/60Hz 0.5A**, and the output is **5.1V 3A**.  
The adapter has passed **FCC** and **UL** certifications.  
The joint between the output cable and the power adapter has been reinforced.  
The USB-C connector also adopts matte design.  
The length of this power adapter is about **45mm (1.77 inches)**.  
The width is also about **45mm (1.77 inches)**.  
And the height is about **27mm (1.06 inches)**.  
And the output cable is about **1.7M (5' 6.92'')**.  
This is how it looks like on hand.  
And the total weight is **98g (3.46 oz)**.  
The ChargerLAB POWER-Z KM002C shows it only supports **Samsung 5V2A protocol**.  
However, this is quite reasonable since not many people would use it to charge their smartphones or laptops.

---

## Teardown

As always, use a spudger to pry along the gap and open the power adapter.  
There is a large thermal pad inside to enhance heat dissipation.  
The input and output are all connected to the PCBA by soldering.  
Here is the AC input end.  
And here is the output end.

The **fuse**, **high-voltage filter capacitor**, **common mode choke**, **transformer**, and **capacitor that powers the master control chip** are on the **front** of the PCBA module.  
And the **bridge rectifier**, **master control chip**, **feedback optocoupler**, and **synchronous rectification chip** are on the **back**.

ChargerLAB discovered that this original Raspberry Pi power adapter utilizes **QR flyback topology**, with the output voltage feedback provided by an **optocoupler**.  
The PCB is designed with slots and inserted with an insulation board for isolation between the primary and secondary sides.

Now, let's begin our exploration of its components, starting from the input end.

The **filter capacitor** and **transformer** are fixed with potting compound.  
And the input **fusible resistor** is insulated with heat-shrinkable tubing.  
The **bridge rectifier** is from **Pingwei**, model is **ABS210** – 2A 1000V.  
The high-voltage **filter capacitor** is from **ManYue** – 15μF 400V.  
And the **ferrite core** of the **common mode choke** is wound and insulated with yellow tape.  
The other two **filter capacitors** have the same specifications: **12μF 400V**.  
The **master control chip** is from **Shengting Micro**, model **D8548HF**, which incorporates **MOSFET internally**.  
And the **filter capacitor** that provides power for this chip is right next to it.

---

## Summary

This Raspberry Pi 15W USB-C charger is built by **Ktec**.  
The components used are of decent quality, and the overall design is compact.  
It adopts a standard **QR flyback topology** with an optocoupler feedback and synchronous rectification.  
It has good build quality, proper layout, good filtering, and sufficient safety measures, such as glue and insulation sheet.  
It offers **5.1V output at 3A**, perfect for powering the Raspberry Pi 4.

---

**Original article and full image gallery**:  
[https://www.chargerlab.com/teardown-of-raspberry-pi-15w-usb-c-power-adapter-ksa-15e-051300hu/](https://www.chargerlab.com/teardown-of-raspberry-pi-15w-usb-c-power-adapter-ksa-15e-051300hu/)
