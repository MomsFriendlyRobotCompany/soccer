
/*
,M,,IRQ enabled: 0   read: 4
M,,*IRQ enabled: 0   read: 4
79
GGA lat: 0.000000 lon: 0.000000
buffer: 0
IRQ enabled: 0   read: 4
$GPGIRQ enabled: 0   read: 4
GA,0IRQ enabled: 0   read: 4
0011IRQ enabled: 0   read: 4
7.79IRQ enabled: 0   read: 4
9,,,IRQ enabled: 0   read: 4
,,0,IRQ enabled: 0   read: 4
00,,IRQ enabled: 0   read: 4
,M,,IRQ enabled: 0   read: 4
M,,*IRQ enabled: 0   read: 4
78
GGA lat: 0.000000 lon: 0.000000
buffer: 0
IRQ enabled: 0   read: 4
$GPGIRQ enabled: 0   read: 4
GA,0IRQ enabled: 0   read: 4
0011IRQ enabled: 0   read: 4
8.79IRQ enabled: 0   read: 4
9,,,IRQ enabled: 0   read: 4
,,0,IRQ enabled: 0   read: 4
00,,IRQ enabled: 0   read: 4
,M,,IRQ enabled: 0   read: 4
M,,*IRQ enabled: 0   read: 4
77
GGA lat: 0.000000 lon: 0.000000
buffer: 0
IRQ enabled: 0   read: 4
$GPGIRQ enabled: 0   read: 4
GA,0IRQ enabled: 0   read: 4
0011IRQ enabled: 0   read: 4
9.79IRQ enabled: 0   read: 4
9,,,IRQ enabled: 0   read: 4
,,0,IRQ enabled: 0   read: 4
00,,IRQ enabled: 0   read: 4
,M,,IRQ enabled: 0   read: 4
M,,*IRQ enabled: 0   read: 4
*/
#pragma once
#include "fifo.hpp"
#include "hardware/irq.h"
#include "hardware/uart.h"
#include "hardware/gpio.h"
#include <cstdint>

constexpr uint UART0_TX_PIN     = 0;
constexpr uint UART0_RX_PIN     = 1;
constexpr uint UART1_TX_PIN     = 8;
constexpr uint UART1_RX_PIN     = 9;

constexpr uint32_t tx_valid[2]  = { // uart0, uart1
    (1 << 0) | (1 << 12) | (1 << 16) | (1 << 28),
    (1 << 4) | (1 << 8) | (1 << 20) | (1 << 24)};
constexpr uint32_t rx_valid[2]  = { // uart0, uart1
    (1 << 1) | (1 << 13) | (1 << 17) | (1 << 29),
    (1 << 5) | (1 << 9) | (1 << 21) | (1 << 25)};
constexpr uint32_t sda_valid[2] = { // i2c0, i2c1
    (1 << 0) | (1 << 4) | (1 << 8) | (1 << 12) | (1 << 16) | (1 << 20) |
        (1 << 24) | (1 << 28),
    (1 << 2) | (1 << 6) | (1 << 10) | (1 << 14) | (1 << 18) | (1 << 22) |
        (1 << 26)};
constexpr uint32_t scl_valid[2] = { // i2c0, i2c1
  (1 << 1) | (1 << 5) | (1 << 9) | (1 << 13) | (1 << 17) | (1 << 21) | (1 << 25) | (1 << 29),
  (1 << 3) | (1 << 7) | (1 << 11) | (1 << 15) | (1 << 19) | (1 << 23) | (1 << 27)};

constexpr uint16_t UART_BUFFER_SIZE = 128;
static volatile Fifo<UART_BUFFER_SIZE> buffer_0;
static volatile Fifo<UART_BUFFER_SIZE> buffer_1;

// do I need to return size?
inline void fast_read_to_fifo(uart_inst_t *uart,
                              volatile Fifo<UART_BUFFER_SIZE> *fifo) {
  uart_hw_t *hw = (uart_hw_t *)uart;

  fifo->push((uint8_t)hw->dr);
  fifo->push((uint8_t)hw->dr);
  fifo->push((uint8_t)hw->dr);
  fifo->push((uint8_t)hw->dr);

  // #define UART_UARTFR_RXFE_BITS   _u(0x00000010)
  // If the FIFO is enabled, the RXFE bit is set when the receive FIFO is empty.
  // while ((hw->fr & UART_UARTFR_RXFE_BITS) == 2) {
  // while (!(hw->fr & UART_UARTFR_RXFE_BITS) ) {
  //   fifo->push( (uint8_t) hw->dr );
  // }
}

static void uart0_irq_func(void) {
  irq_set_enabled(UART0_IRQ, false);
  fast_read_to_fifo(uart0, &buffer_0);
  // while (uart_is_readable(uart0)) {
  //   uint8_t b = (uint8_t)uart_getc(uart0);
  //   buffer_0.push(b);
  // }
  irq_set_enabled(UART0_IRQ, true);
}

static void uart1_irq_func(void) {
  irq_set_enabled(UART1_IRQ, false);
  // printf("IRQ enabled: %u", (uint)irq_is_enabled(UART1_IRQ));
  fast_read_to_fifo(uart1, &buffer_1);
  irq_set_enabled(UART1_IRQ, true);
}

class Serial {
  uart_inst_t *uart;
  volatile Fifo<UART_BUFFER_SIZE> *buffer{nullptr};

public:
  Serial() {}
  ~Serial() { uart_deinit(uart); }

  uint init(uint baudrate, uint8_t port, uint8_t pin_tx, uint8_t pin_rx) {
    bool valid = (1 << pin_tx) & tx_valid[port];
    if (!valid) return 0;
    valid = (1 << pin_rx) & rx_valid[port];
    if (!valid) return 0;

    // IRQ will fire when 4 bytes are in FIFO RX buffer
    const bool RX_EN = true; // enable IRQ fro RX
    const bool TX_EN = false;
    if (port == 0) {
      uart     = uart0;
      buffer   = &buffer_0;
      baudrate = uart_init(uart0, baudrate);
      gpio_set_function(pin_tx, GPIO_FUNC_UART);
      gpio_set_function(pin_rx, GPIO_FUNC_UART);
      irq_set_exclusive_handler(UART0_IRQ, uart0_irq_func);
      irq_set_enabled(UART0_IRQ, true);
      uart_set_irq_enables(uart0, RX_EN, TX_EN); // uart, rx, tx
    }
    else if (port == 1) {
      uart     = uart1;
      buffer   = &buffer_1;
      baudrate = uart_init(uart1, baudrate);
      gpio_set_function(pin_tx, GPIO_FUNC_UART);
      gpio_set_function(pin_rx, GPIO_FUNC_UART);
      irq_set_exclusive_handler(UART1_IRQ, uart1_irq_func);
      irq_set_enabled(UART1_IRQ, true);
      uart_set_irq_enables(uart1, RX_EN, TX_EN); // uart, rx, tx
    }
    else return 0;

    uart_set_fifo_enabled(uart, true);
    uart_set_translate_crlf(uart, false);

    return baudrate;
  }

  inline bool is_enabled() { return uart_is_enabled(uart); }

  inline void flush() { buffer->clear(); }

  inline uint set_baud(uint baud) { return uart_set_baudrate(uart, baud); }

  inline size_t available() { return buffer->size(); }

  size_t read(uint8_t *data, size_t size) {
    size_t cnt   = 0;
    size_t bsize = buffer->size();
    while ((cnt < bsize) && (cnt < size)) {
      data[cnt++] = buffer->pop();
    }

    return cnt;
  }

  inline uint8_t read() { return buffer->pop(); }

  void write(const uint8_t *data, size_t size) {
    uart_write_blocking(uart, data, size);
  }
};
