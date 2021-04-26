# Driver for the SH1106 display

This driver consists mostly of the work of Radomir Dopieralski (@deshipu).
I added a few functions and changed the existing ones so it matches better
my needs for a project.

## Features

Use OLED display with the SH1106 driver with SPI or I2C. It is based on the MicroPython
framebuffer class and consists wrappers for this class as well as special methods
for controlling the display.

## Connection

The SH1106 supports next to thers the I2C or SPI interface. The connection depends on the interface used
and the number of devices in the system. Especially the ESP8266 with their small
number of GPIO ports may require optimization.

### I2C
SCL and SDA have to be connected as minimum. The driver also resets the device by the reset PIN.
If your are low on GPIO ports, reset can be applied by a dedicated circuit, like the MCP100-300.

### SPI
SCLK, MOSI, D/C are always required. If the display is the only SPI device in the set-up,
CS may be tied to GND. Reset has also to be connected, unless it is driven
by an external circuit.


## Class

The driver contains the SH1106 class and the derived SH1106_I2C and SH1106_SPI classes.
Besides the constructors, the methods are the same.

### I2C
```
display = sh1106.SH1106_I2C(width, height, i2c, reset, address)
```
- width and height define the size of the display
- i2c is an I2C object, which has to be created beforehand and tells the ports for SDA and SCL.
- res is the GPIO Pin object for the reset connection. It will be initialized by the driver.
If it is not needed, `None` has to be supplied.
- adr is the I2C address of the display. Default 0x3c or 60


### SPI
```
display = sh1106.SH1106_SPI(width, height, spi, dc, res, cs)
```
- width and height define the size of the display
- spi is an SPI object, which has to be created beforehand and tells the ports for SCLJ and MOSI.
MISO is not used.
- dc is the GPIO Pin object for the Data/Command selection. It will be initialized by the driver.
- res is the GPIO Pin object for the reset connection. It will be initialized by the driver.
If it is not needed, it can be set to `None` or omitted. In this case the default value
of `None` applies.
- cs is the GPIO Pin object for the CS connection. It will be initialized by the driver.
If it is not needed, it can be set to `None` or omitted. In this case the default value
of `None` applies.


## Methods

### display.init_display()
```
display.init_display()
```
Initializes the display, fills it with the color 0 and displays the empty screen. It also tries
to apply the reset signal, if it is connected ( = not `None`).

### display.power_on() and display.power_off()

```
display.poweron()
display.poweroff()
display.sleep(state)
```
Enable and disable the display. `display.sleep(True)` is identical to `display.poweroff()`,
`display.sleep(False)` is equivalent to `display.poweron()`.
Other than the literal meaning could tell, it does not switch the power line(Vcc)
of the display.

###  display.contrast()

```
display.contrast(level)
```
Set the display's contrast to the given level. The range is 0..255. For a single color
display like the SH1106, this is actually the brightness.

###  display.invert()
```
display.invert(flag)
```
Invert the content of the display, depending on the value of Flag. This is immediately
effective for the whole display.
- flag = True  Invert
- flag = False Normal mode

###  display.rotate()
```
display.rotate(flag[, update=True])
```
Rotate the content of the display, depending on the value of Flag.
To become fully effective, you have to run display.show(). If the parameter update is True, show() is called by the function itself.
- flag = True: Rotate by 180 degree
- flag = False: Normal mode  

###  display.show()

Display the content of the frame buffer on the display.
```
display.show()
```
The usual program flow would set-up/update the frame buffer content with a sequence of calls
an the call display.show() for the content to be shown (see examples below).

## Framebuffer Methods

The below listed display methods of the framebuffer class are mirrored in this
class. For a documentation, please look into the MicroPython documentation at http://docs.micropython.org/en/latest/pyboard/library/framebuf.html?highlight=framebuf#module-framebuf:

- fill
- fill_rect
- line
- vline
- hline
- rect
- pixel
- scroll
- text
- blit


The text is displayed with the built-in
8x8 pixel font, which support the ASCII character set values 32..127. The text overlays
the previous content; 'on' pixels in a character will not overwrite existing 'off' pixels.
If you want to rewrite an area of the screen, you have to clear it beforehand,
e.g. with the `fill_rect()` method.

Remark: If you want to use other font styles and sizes, have a look at
the work of Peter Hinch (@pythoncoder) at https://github.com/peterhinch/micropython-font-to-py

### display.reset()
```
display.reset()
```
Attempt to reset the display by toggling the reset line. This is obviously only effective
is reset is connected. Otherwise it's a No-Op.


# Sample Code

## SPI
```
# MicroPython SH1106 OLED driver
#
# Pin Map SPI for ESP8266
#   - 3v - xxxxxx   - Vcc
#   - G  - xxxxxx   - Gnd
#   - D7 - GPIO 13  - Din / MOSI fixed
#   - D5 - GPIO 14  - Clk / SCLK fixed
#   - D8 - GPIO 4   - CS (optional, if the only connected device)
#   - D2 - GPIO 5   - D/C
#   - D1 - GPIO 2   - Res (required, unless a Hardware reset circuit is connected)
#
# for CS, D/C and Res other ports may be chosen.
#
from machine import Pin, SPI
import sh1106

spi = SPI(1, baudrate=1000000)
display = sh1106.SH1106_SPI(128, 64, spi, Pin(5), Pin(2), Pin(4))
display.sleep(False)
display.fill(0)
display.text('Testing 1', 0, 0, 1)
display.show()
```
## I2C

```
# MicroPython SH1106 OLED driver
#
# Pin Map I2C for ESP8266
#   - 3v - xxxxxx   - Vcc
#   - G  - xxxxxx   - Gnd
#   - D2 - GPIO 5   - SCK / SCL
#   - D1 - GPIO 4   - DIN / SDA
#   - D0 - GPIO 16  - Res (required, unless a Hardware reset circuit is connected)
#   - G  - xxxxxx     CS
#   - G  - xxxxxx     D/C
#
# Pin's for I2C can be set almost arbitrary
#
from machine import Pin, I2C
import sh1106

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
display = sh1106.SH1106_I2C(128, 64, i2c, Pin(16), 0x3c)
display.sleep(False)
display.fill(0)
display.text('Testing 1', 0, 0, 1)
display.show()
```
