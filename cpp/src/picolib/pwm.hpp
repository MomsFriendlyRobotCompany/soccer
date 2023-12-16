
#pragma once

#include "hardware/clocks.h"
#include "hardware/pwm.h"
#include "pico/stdlib.h"
#include "hardware/gpio.h"

constexpr uint16_t SERVO_MAX_PULSE_WIDTH = 2000UL;
constexpr uint16_t SERVO_MIN_PULSE_WIDTH = 1000UL;

class Servo {
  uint32_t slice_num{0};
  // uint channel{0}; // maybe rewrite to bring this back?
  uint32_t pin{0};
  uint16_t max_us; // max + min is the total signal time for 180 def
  uint16_t min_us; // minimum signal time for 0 deg

  // If overclocked to something other than 125MHz, need
  // to change these calculations. Servo operate on a
  // 50Hz window (0.020 sec) and are supposed to look at
  // a pulse between 1-2 msec (1000 - 2000 usec) long
  //
  // uint32_t clk = clock_get_hz(clk_sys);
  // clockDiv = 64;
  // wrap = uint16_t(0.02f / ((float)clkDiv / clk))
  //
  // period = clkDiv / clk_sys * wrap
  // 0.02 sec = 64 / 125MHz * 39,062.5
  const uint32_t clkDiv{64};
  const uint16_t wrap{39063};

public:
  Servo() {}
  ~Servo() {}

  void init(const uint32_t pwm_pin, uint16_t max_pwm_us = SERVO_MAX_PULSE_WIDTH,
            uint16_t min_pwm_us = SERVO_MIN_PULSE_WIDTH) {

    pin = pwm_pin;
    gpio_set_function(pwm_pin, GPIO_FUNC_PWM);
    // Determine slice/channel pin belongs to
    slice_num = pwm_gpio_to_slice_num(pwm_pin);
    // channel   = pwm_gpio_to_channel(pwm_pin);

    max_us = uint16_t((max_pwm_us - min_pwm_us) / 20E3 * wrap);
    min_us = uint16_t(min_pwm_us / 20E3 * wrap);

    pwm_config config = pwm_get_default_config();
    pwm_config_set_clkdiv_int(&config, clkDiv);
    pwm_config_set_wrap(&config, wrap);
    pwm_init(slice_num, &config, true);
  }

  void write_us(uint16_t pulse_width_us) {
    if (pulse_width_us > max_us) pulse_width_us = max_us;
    // pwm_set_chan_level(slice_num, channel, pulse_width_us);
    pwm_set_gpio_level(pin, pulse_width_us + min_us); // helper, might be better to get slice/channel
  }

  void write(float percent) {
    if (percent > 100.0f) percent = 100.0f;
    if (percent < 0.0f) percent = 0.0f;

    pwm_set_gpio_level(pin, percent*max_us + min_us); // helper, might be better to get slice/channel
    // pwm_set_chan_level(slice_num, channel, percent*max_us + min_us);
  }
};

using ESC = Servo; // just an alias ... want to do better esc stuff later

// class ESC: public Servo {
//   public:
// };