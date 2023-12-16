
#pragma once

#include "hardware/spi.h"
#include "hardware/gpio.h"

constexpr uint32_t SPI_20MHZ = 20000000; // maximum
constexpr uint32_t SPI_10MHZ = 10000000;
constexpr uint32_t SPI_1MHZ = 1000000;
constexpr uint32_t SPI_100KHZ = 100000;
constexpr uint32_t SPI_DEFAULT_BAUD = 48000; // default rate

constexpr uint32_t SPI_8BIT_MODE = 8;
constexpr uint32_t SPI_16BIT_MODE = 16;

class SPI {
  public:
  SPI() {}
  ~SPI() { spi_deinit(port); }

  bool init(
        const uint8_t port_num,
        uint32_t baud,
        const pin_t miso,
        const pin_t mosi,
        const pin_t sck,
        const pin_t cs) {
    if (port_num == 0) port = spi0;
    else if (port_num == 1) port = spi1;
    else return false;

    // Initialize SPI channel (channel, baud rate set to 20MHz)
    spi_init(port, baud);
    // Format (channel, data bits per transfer, polarity, phase, order)
    const spi_order_t order = SPI_MSB_FIRST; // this can ONLY be MSB first
    spi_set_format(port, 16, (spi_cpol_t)0, (spi_cpha_t )0, order);
    spi_set_slave(port, false); // set to Master (default)

    // Map SPI signals to GPIO ports
    gpio_set_function(miso, GPIO_FUNC_SPI);
    gpio_set_function(mosi, GPIO_FUNC_SPI);
    gpio_set_function(sck, GPIO_FUNC_SPI);
    gpio_set_function(cs, GPIO_FUNC_SPI);

    return true;
  }

  inline // value? Do we need to change this?
  uint32_t set_baudrate(const uint32_t baud) { return spi_set_baudrate(port, baud); }

  // uint16_t read(const uint16_t data){
  //   uint16_t buffer{0};
  //   if (spi_is_writable(port)) {
  //     int num = spi_read16_blocking(port, data, &buffer, 2);
  //   }
  //   return buffer;
  // }

  int transfer(const uint16_t* out, uint16_t* in, size_t len) {
    int num{0};
    if (spi_is_writable(port)) {
      num = spi_write16_read16_blocking(port, out, in, len);
    }
    return num;
  }

  int transfer(const uint8_t* out, uint8_t* in, size_t len) {
    int num{0};
    if (spi_is_writable(port)) {
      num = spi_write_read_blocking(port, out, in, len);
    }
    return num;
  }

  protected:
  spi_inst_t* port{nullptr};
  // pin_t miso, mosi, sck, cs;
};