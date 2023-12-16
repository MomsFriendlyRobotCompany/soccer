

#pragma once

#include "pico/mutex.h"

/**
 A simple mutex class modelled somewhat after the Python
 version. It defaults to blocking but can also be set to
 nonbolocking if a timeout > 0 is set.

 Mutex m; // blocking
 Mutex n(100); // timeout in msec

 // nonblock, returns false after 100 msec of waiting
 if (n.acquire()) {
  ...
  n.release();
 }

 m.acquire(); // block
 ...
 m.release();
*/
class Mutex {
  mutex_t mutex;
  uint32_t timeout_ms{0};

  public:
  Mutex(uint32_t msec=0): timeout_ms(msec) { mutex_init(&mutex); }
  ~Mutex() { mutex_exit(&mutex); }

  void set_timeout(uint32_t msec) { timeout_ms = msec; }

  bool acquire() {
    if (timeout_ms > 0) return mutex_enter_timeout_ms(&mutex, timeout_ms);
    mutex_enter_blocking(&mutex);
    return true;
  }

  void release() { mutex_exit(&mutex); }
  bool is_ready() { return mutex_is_initialized(&mutex); }
};
