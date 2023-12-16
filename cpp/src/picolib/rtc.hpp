
#pragma once

#include "hardware/rtc.h"
#include "pico/stdlib.h"
#include "pico/util/datetime.h"

// Not sure how useful this is ... taken from Pico-SDK
//
// Start on Friday 5th of June 2020 15:45:00
// datetime_t t = {
//   .year  = 2020,
//   .month = 06,
//   .day   = 05,
//   .dotw  = 5, // 0 is Sunday, so 5 is Friday
//   .hour  = 15,
//   .min   = 45,
//   .sec   = 00
// };
//
// set_rtc(t);
//
// rtc_get_datetime(&t);
// datetime_to_str(datetime_str, sizeof(datetime_buf), &t);
// printf("\r%s      ", datetime_str);
static
bool set_rtc(datetime_t& t) {
  rtc_init();
  bool ok = rtc_set_datetime(&t);
  if (ok == false) return false;

  // wait 64 usec to clock to sync
  sleep_us(64);
  return true;
}