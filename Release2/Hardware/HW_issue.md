## [2024-04-30 16:45] Power Supply Issues with Shelly Plus 1

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

**Tags:**  
`status:critical` `hardware:shelly` `power:12v` `power:24v` `input:unsupported` `test:pending`
