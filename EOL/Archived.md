![EOL](https://img.shields.io/badge/status-EOL-red)

# Archived Prototypes (Versions 1–3)

This folder contains all files, diagrams, and schematics related to **prototypes from versions 1.0 to 3.0** of the system. These materials are officially marked as **End of Life (EOL)** and are **no longer recommended for use** under any circumstances.

## Critical Notice

Following extensive testing and technical review, all legacy versions (1–3) have been determined to be **technically inadequate and electrically unsafe**. They lack many essential **active and passive protections**, and do not meet current standards of:

- **Electrical safety**
- **Procedural correctness**
- **Structural reliability**
- **Technical documentation quality**

These versions were useful in the early stages of development, but **must not be reused** or referenced for future implementations. Any reuse may expose users to **significant risks**, including electrical faults or system failure.

## What's Missing in Versions 1–3

These prototype versions lack several critical components and design safeguards, such as:

- **Active protections**: overcurrent limiters, thermal shutdown logic, automatic disconnection systems  
- **Passive protections**: fuses, reverse polarity diodes, PTCs, surge protectors  
- **Filtering and stability**: capacitors and inductors to prevent EMI and stabilize voltage  
- **Physical and electrical isolation**: absence of galvanic separation, lack of protected relay control  
- **Structured design**: unclear wiring logic, no separation of power and control signals  
- **Documentation**: incomplete instructions, missing test procedures, no maintenance guidelines

## Purpose of This Archive

The `EOL` folder is retained to:

- **Document the evolution** of the project  
- Ensure transparency in the design lifecycle  
- **Avoid confusion** between outdated and supported files  
- Provide historical reference for analysis or review

## Current Development

All key improvements are now part of the **new design cycle**, which introduces:

- Full integration of **electrical safety mechanisms**
- Cleaner, **modular logic and fallback design**
- **Robust structural engineering** with validated test procedures
- **Professional documentation** suitable for real-world deployment

Please refer to the root of the repository for ongoing and supported versions.

---

**Important:**  
The contents of this folder should not be reused, tested, or deployed in any context. They remain available **for archival and documentation purposes only**.
