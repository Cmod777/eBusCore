## Block 5 – Step-Down Modules + USB-C Output (Normal + Backup)

This block handles the regulated 5V DC power supply to the eBUS Wi-Fi module via USB-C.  
Two separate step-down converters ensure uninterrupted power, depending on the grid state.

---

### Functional Roles

| Source        | Condition     | Step-Down Active | eBUS Powered |
|---------------|---------------|------------------|---------------|
| 230V Grid     | Present        | 230V → 5V module | Yes           |
| 12V Battery   | Grid lost      | 12V → 5V module  | Yes           |

---

### Step-Down A – Grid Powered

- **Input:** 230V AC  
- **Output:** 5V DC (USB Type A or terminal)
- **Used when grid is ON**

```
[230V AC] → [Step-Down 230V → 5V] → USB-C → [eBUS Module]
```

---

### Step-Down B – Battery Powered (UPS)

- **Input:** 12V DC (from battery via relay)
- **Output:** 5V DC (USB Type A or terminal)
- **Used when grid is OFF**

```
[12V Battery] → [Relay] → [Step-Down 12V → 5V] → USB-C → [eBUS Module]
```

---

### Wiring Diagram

```
                +---------------------------+
                |     USB-C OUTPUT LINE     |
                +---------------------------+
                      ↑              ↑
         [5V OUT] ←───┘              └───→ [5V OUT]
      (From Step-Down A)           (From Step-Down B)

Both step-down modules are wired to the same USB-C output.
Only one will be active depending on power state.
```

---

### USB-C Line (Shared)

- Output can be:
  - USB-C female socket embedded in panel
  - Terminal block to USB-C adapter
- Only **one source is powered** at a time (never simultaneous)
- Optionally, add **diodes** to isolate outputs (e.g., Schottky 1A)

---

### Wire Specifications

| Line       | Color  | Section     | From → To                  |
|------------|--------|-------------|----------------------------|
| 230V IN    | Brown  | 1.0–1.5 mm² | AC → Step-Down A           |
| Step-Down A OUT | Red/Black | 0.5 mm² | → USB-C                   |
| 12V IN     | Red    | 1.0 mm²     | Relay NO → Step-Down B     |
| Step-Down B OUT | Red/Black | 0.5 mm² | → USB-C                   |

---

### Best Practices

- Secure step-down modules to DIN rail with adapters or adhesive base
- Use heatshrink over output wires
- Add inline 5V fuse (e.g., 0.5A) if eBUS module has no internal protection
- Test both power paths independently before finalizing wiring

---

### Optional Isolation

If needed, use **Schottky diodes (e.g., 1N5822)** on both 5V OUT lines before merging to USB-C:

```
Step-Down A 5V ──>|──┐
                  |         +──→ [USB-C +5V]
Step-Down B 5V ──>|──┘
```

---

### Summary

| Module      | Source     | State Required | Use Case         |
|-------------|------------|----------------|------------------|
| Step-Down A | 230V AC    | Grid Present   | Default Power     |
| Step-Down B | 12V Battery| Grid Lost      | Emergency Backup  |
