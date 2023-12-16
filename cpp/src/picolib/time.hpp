
#pragma once

#include <cstdint>
#include "pico/time.h"

/*
typedef struct {
  int16_t year;
  int8_t month;
  int8_t day;
  int8_t dotw;
  int8_t hour;
  int8_t min;
  int8_t sec;
} datetime_t;
*/

static
uint64_t time_since_boot_us() {
  absolute_time_t t = get_absolute_time();
  return to_us_since_boot(t);
}

static
uint32_t time_since_boot_ms() {
  absolute_time_t t = get_absolute_time();
  return to_ms_since_boot(t);
}