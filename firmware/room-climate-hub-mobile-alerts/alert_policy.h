#pragma once
#include <cmath>
struct AlertPolicy {
  bool active=false; unsigned confirmations=0;
  bool update(float temperature, float humidity, float pressure) {
    if (!std::isfinite(temperature)||!std::isfinite(humidity)||!std::isfinite(pressure)||temperature < -40||temperature > 85||humidity < 0||humidity > 100||pressure < 300||pressure > 1100) { confirmations=0; active=false; return false; }
    if (temperature >= 30) { if (confirmations<3) ++confirmations; if(confirmations==3) active=true; }
    else { confirmations=0; if(temperature<=28) active=false; }
    return true;
  }
};
