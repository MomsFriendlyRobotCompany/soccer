
#pragma once

// #include "pico/stdlib.h"
// #include "pico/binary_info.h"
#include "hardware/adc.h"
#include "hardware/gpio.h"

constexpr uint A0         = 0;
constexpr uint A1         = 1;
constexpr uint A2         = 2;
constexpr uint A3         = 3;
constexpr float ADC_SCALE = 3.3f / (1 << 12);

class ADC {
public:
  ADC() { adc_init(); }
  ~ADC() {}

  bool init(const uint pin) {
    if (pin <= 3) {
      // Make sure GPIO is high-impedance, no pullups etc
      adc_gpio_init(pin + 26);
      return true;
    }
    return false;
  }

  uint16_t read_raw(const uint pin) {
    adc_select_input(pin);
    return adc_read();
  }

  inline float read(const uint pin) { return ADC_SCALE * read_raw(pin); }
};

// template<uint pin>
// bool ADC<pin>::initialized = false;
// bool ADC::initialized = false;

// static ADC adc;