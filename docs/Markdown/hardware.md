# Raspberry Pi

![RPI 3](https://www.raspberrypi.org/wp-content/uploads/2016/02/Pi_3_Model_B.png)

I am currently using a 1.2 GHz quad core [RPi 3](https://www.adafruit.com/products/3055) (ARMv8) as the main board running the lite version of Raspbian. It has on-board:

* 802.11n Wifi
* Bluetooth 4.1 BLE

## Camera Interface (CSI)

* [PiCamera](https://www.adafruit.com/products/3099) is used for video odometry (currently have version 1, 5 Mpixels but moving to 8 Mpixels)

## I2C

The following is on the I2C bus:

* [MCP23017 16b I/O Expander](https://www.adafruit.com/products/732): 0x20
* TBD - AHRS Compass ...need to get one

## GPIO

The RPi has both Pi pin numbers and BCM pin numbers assigned to its GPIO.

|BCM| Use  | Pi | Pi | Use |BCM|
|---|------|----|----|-----|---|
|   | 3v3  |  1 |  2 | 5v  |   |
| 2 | SDA  |  3 |  4 | 5v  |   |
| 3 | SCL  |  5 |  6 | GND |   |
| 4 | PWM0 |  7 |  8 | TX  | 14|
|   | GND  |  9 | 10 | RX  | 15|
| 17| PWM1 | 11 | 12 |     | 18|
| 27| PWM2 | 13 | 14 | GND |   |
| 22| PWM3 | 15 | 16 |     | 23|
|   | 3v3  | 17 | 18 |     | 24|
| 10| MOSI | 19 | 20 | GND |   |
|  9| MISO | 21 | 22 |     | 25|
| 11| SCLK | 23 | 24 | CE0 |  8|
|   | GND  | 25 | 26 | CE1 |  7|
|  0| A0   | 27 | 28 |     |  1|
|  5| B0   | 29 | 30 | GND |   |
|  6| A1   | 31 | 32 |     | 12|
| 13| B1   | 33 | 34 | GND |   |
| 19|      | 35 | 36 |     | 16|
| 26|      | 37 | 38 |     | 20|
|   | GND  | 39 | 40 |     | 21|


# Sensors

* [Sharp GP2Y0A21YK0F IR](https://www.adafruit.com/products/164) sensors give 10-80 cm (3.9-31.5 in)
* Pololu [ACS711LC Current sensor](https://www.pololu.com/product/2198) measures up to +/-25 A and up to 30 V

# Motion

* Pololu [TB6612FNG Dual Motor Driver](https://www.pololu.com/product/713) provides 4.5-13.5V at 1A continuous (3A peak) current.
* Motors currently are 12V 130 rpm gear motors

# Parts

Here is a parts list of **key components** that I am using. I am not listing wires, bread boards, cables, etc. Also note, I have rounded up the costs (i.e., $4.95 => $5).

| Part | Source | Number | Item Cost | Sum | Notes |
| ---  | ---    | ---    | ---       | --- | ---   |
| RPi v3    | [Adafruit](https://www.adafruit.com) | 1 | $40 | $40 | Main board, has wifi and bluetooth already |
| Pi Camera | [Adafruit](https://www.adafruit.com) | 1 | $30 | $30 | Currently have old 5 Mpixel, will upgrade to newer 8 Mpixel |
| PWM/Servo Driver, 16 Channels, 12 bit resolution (PCA9685) | [Adafruit](https://www.adafruit.com) | 1 | $15 | $15 | Controls motors and servos over I2C |
| MCP23017 (16 I/O port expander, I2C) | [Adafruit](https://www.adafruit.com) | 1 | $3 | $3 | Used to increase the digital I/O |
| TB6612FNG Dual Motor Driver | [Pololu](https://www.pololu.com/product/713) | 2 | $5 | $10 | Logic level 3.3V, motors 4.5-13V @ 1A continous (3A peak) per channel |
| 5V, 5A Buck Converter (D24V50F5)  | [Pololu](https://www.pololu.com) | 1 | $15 | $15 | For powering my electronics |
| 12V, 5A Boost Converter (U3V50F12) | [Pololu](https://www.pololu.com) | 1 | $14 | $14 | For powering my motors (future 12V motors) |
| Sharp IR | [Pololu](https://www.pololu.com) | 8 | $10 | $80 | Range 10-80 cm |
| PS4 Controller   | [Walmart](http://www.walmart.com) | 1 | $54 | $54 | |
| Micro SD (32 GB) | [Walmart](http://www.walmart.com) | 1 | $12 | $12 | |


---

<p align="center">
	<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
		<img alt="Creative Commons License"  src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" />
	</a>
	<br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.
</p>
