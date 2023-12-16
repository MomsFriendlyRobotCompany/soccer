
#pragma once

#include <cstdint>
#include <cstdio>
#include "tusb.h" // wait for USB

void write_stdout(const uint8_t *buffer, size_t size) {
  if (tud_cdc_connected() == false) return;

  size_t sent = 0;
  while (size > 0) {
    sent += fwrite(&buffer[sent],1,size,stdout);
    size -= sent;
  }

  // char c = '\n';
  // fwrite(&c,1,1,stdout); // send '\n' to flush
}

uint32_t read_stdin(uint8_t *buffer, uint32_t size, uint32_t timeout=10) {
  if (tud_cdc_connected() == false) return 0xffffffff;

  uint32_t cnt = 0;
  int b;
  while (cnt < size) {
    b = getchar_timeout_us(timeout);
    if (b == PICO_ERROR_TIMEOUT) break;
    buffer[cnt++] = (uint8_t)b;
  }
  return cnt;
}



// class SerialUSB {
// public:
//   SerialUSB() {}
//   ~SerialUSB() {}

//   uint32_t read(uint8_t *buffer, uint32_t size, uint32_t timeout=10) {
//     uint32_t cnt = 0;
//     int b;
//     while (cnt < size) {
//       b = getchar_timeout_us(timeout);
//       if (b == PICO_ERROR_TIMEOUT) break;
//       buffer[cnt++] = (uint8_t)b;
//     }
//     return cnt;
//   }

//   int read(uint32_t timeout=10) {
//     int b = getchar_timeout_us(timeout);
//     if (b == PICO_ERROR_TIMEOUT) return -1;
//     return (uint8_t)b;
//   }

//   void write(const uint8_t *buffer, size_t size) {
//     while (size > 0) {
//       size -= fwrite(buffer,1,size,stdout);
//     }
//     char c = '\n';
//     fwrite(&c,1,1,stdout); // send '\n' to flush
//   }

//   void write(const uint8_t b) {
//     fwrite(&b,1,1,stdout);
//   }
// };