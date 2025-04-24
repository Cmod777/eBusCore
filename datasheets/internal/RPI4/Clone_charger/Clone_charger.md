### 1. Introduction

The official Raspberry Pi 15W USB-C Power Supply (model **KSA-15E-051300HU**) is a highly optimized adapter, designed specifically to meet the strict power requirements of Raspberry Pi boards. A detailed teardown published by ChargerLAB highlights its robust architecture, precise voltage regulation, and high-quality components, making it an ideal reference for stable and reliable 5.1V power delivery.

In this project, we aimed to replicate the core principles of that original power adapter, but with one key difference: instead of operating from a 230V AC mains input, our version is designed to work with a **13.8V DC input**, commonly available in battery-based or mobile systems. This design allows seamless integration into environments where AC power is not guaranteed or where backup DC power is essential.

It is important to clarify that this power module is **not intended to replace** the official adapter under normal operation. The Raspberry Pi will continue to be powered through its USB-C port via the official 230V power adapter. Instead, this custom-built power supply acts as a **redundant backup source**, directly connected to the 5V and GND pins on the GPIO header.

