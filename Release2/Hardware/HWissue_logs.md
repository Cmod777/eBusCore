<details>
<summary><strong>[2024-04-30 16:45]</strong> Power Supply Issues with Shelly Plus 1  
<em>Tags:</em> <code>status:critical</code> <code>hardware:shelly</code> <code>power:12v</code> <code>power:24v</code> <code>input:unsupported</code> <code>test:pending</code></summary>

**Title:** Unreliable 12V DC operation on Shelly Plus 1

**Summary:**  
Despite documentation and user reports suggesting that the Shelly Plus 1 module supports 12V DC input (with a stated tolerance of ±10%), all real-world tests have failed to confirm reliable operation at this voltage.

**Observed Issues:**
- The device **did not power on at 13.8V**, even though this falls within the official tolerance range.
- The device **did not power on at 13.2V**, using a diode drop to stay safely inside the tolerance range.
- The device **did not power on when connected to a regulated 12.0V step-down line**.
- It **did power on instantly when connected to 230V AC**, using the same L/N terminals.
- It **did not respond when connected via the 12+ and SW terminals**, despite stable 12.0V readings at the input and a suspiciously low current draw (~0.5mA).
- **Multiple wiring variants** were tested across all 12V options, including reversed polarity on SW and direct 12V on L – with no success.
- The unit was **opened to inspect internal jumpers** (common in legacy models for switching between 12/24V), but no such jumper was found.

**Conclusion:**  
After numerous resets, factory resets, rewirings, and power cycling attempts, **the Shelly Plus 1 only successfully powers on via 230V AC**. Despite 12V DC still being printed on the device casing, **practical tests and measurements strongly suggest that 12V DC is no longer supported**, or only works on older hardware revisions.

**Next Step:**  
A test using a **DC-DC step-up module to supply 24V DC directly to the L/N terminals** will be performed.  
According to the official technical documentation, **24V–48V DC is a fully supported input range when connected to L/N**, and is now considered the recommended configuration for low-voltage DC operation.  
The role of the 12+ and SW terminals remains undocumented and potentially obsolete.

This event is logged as a major deviation between device labeling and real-world behavior.

</details>

---

<details>
<summary><strong>[2024-04-30 17:30]</strong> LM2596 Display Module Failure  
<em>Tags:</em> <code>status:partial-failure</code> <code>hardware:lm2596</code> <code>power:step-down</code> <code>display:broken</code> <code>test:manual-needed</code> <code>recommendation:replacement</code></summary>

**Title:** Burned-out voltage display on LM2596 step-down module

**Summary:**  
During setup and early testing, one LM2596 step-down module (model with integrated 3-digit voltmeter) experienced partial failure: the voltage display stopped functioning, although the regulator itself continued to output the correct voltage.

**Observed Behavior:**
- The onboard digital display **no longer shows any values** (blank screen).
- **Output voltage remains stable and correct**, as confirmed by multimeter testing.
- No deviation in performance was detected, and the module appears to **regulate voltage correctly**.
- The issue was **limited to the display circuit**, not the voltage regulation path.

**Implications:**
- Without onboard readings, **manual multimeter testing is required** to confirm voltage values.
- This increases testing time and introduces a risk of configuration or wiring errors.
- In ongoing or long-term installations, **lack of visual feedback makes monitoring inconvenient and error-prone**.

**Recommendation:**  
It is advised to **replace the module with another LM2596 model featuring a working display**.  
In general, **choosing a step-down regulator with an integrated voltage screen is strongly preferred**, as it allows for:
- Easier and faster configuration
- Quick visual diagnostics
- Fewer direct probe measurements on output terminals
- Better usability in enclosed or remote setups

</details>

---
<details>
<summary><strong>[2024-04-30 18:10]</strong> Dependent component tests blocked by upstream Shelly failure  
<em>Tags:</em> <code>status:blocked</code> <code>hardware:downstream</code> <code>dependency:shelly</code></summary>

**Title:** Dependent component tests blocked by upstream Shelly failure

**Summary:**  
Due to the unexpected failure of Shelly Plus 1 modules to operate under 12V DC (see related event), **no downstream device tests were performed**. The anomaly in power delivery made it impossible to validate the behavior of any components relying on Shelly output or status.

**Reason for test interruption:**
- Shelly modules failed to power on under all 12V configurations.
- Devices wired *downstream* (ventilation modules, relays, sensors, automation triggers) **never received signal, voltage, or trigger events**.
- Running tests in this state would **produce invalid or misleading results**.
- Waiting for further validation of Shelly behavior or stable power is necessary before retesting the chain.

**Planned action:**  
Tests will be resumed only after confirming Shelly operation with alternative power input (e.g. 24V DC via step-up module). Until then, all cascading logic is suspended.

</details>

---
