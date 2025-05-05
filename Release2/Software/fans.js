let HIGH_THRESHOLD = 40.0;  // Start fans if either sensor exceeds this
let LOW_THRESHOLD = 37.0;   // Stop fans when the average drops below this
let CHECK_INTERVAL = 5000;  // Check every 5 seconds

function checkTemperatures() {
  let t1 = Shelly.getComponentStatus("temperature:0").tC;
  let t2 = Shelly.getComponentStatus("temperature:1").tC;

  // If one of the sensors is unavailable, skip this cycle
  if (t1 === null || t2 === null) return;

  let avg = (t1 + t2) / 2;

  // Turn on fans if either sensor exceeds the high threshold
  if (t1 >= HIGH_THRESHOLD || t2 >= HIGH_THRESHOLD) {
    Shelly.call("Switch.Set", { id: 0, on: true });
  }

  // Turn off fans if the average drops below the low threshold
  else if (avg <= LOW_THRESHOLD) {
    Shelly.call("Switch.Set", { id: 0, on: false });
  }
}

Timer.set(CHECK_INTERVAL, true, checkTemperatures);

// This script controls the Add-On with two temperature probes to manage forced ventilation using the Shelly relay.
// When either probe exceeds 40°C, the fan is turned on. It turns off when the average drops below 37°C.
