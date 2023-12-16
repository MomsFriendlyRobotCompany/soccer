
#pragma once

#include "hardware/watchdog.h"

/**
 Not sure how useful this is compared to C functions ...
*/
class WatchDog {
  public:
  WatchDog() {}
  ~WatchDog() {}

  inline // max is 8.3 sec (8300 msec)
  void enable(uint32_t delay_ms) { watchdog_enable(delay_ms, true); }
  inline // reset
  void touch() { watchdog_update(); }
  inline
  bool caused_reboot() { // double check  need both funcs
    return watchdog_caused_reboot() || watchdog_enable_caused_reboot();
  }
  inline
  uint32_t time_left_us() { return watchdog_get_count(); }
};