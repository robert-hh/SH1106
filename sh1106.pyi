"""
Type stub for the MicroPython SH1106 OLED driver.

This library provides a driver for controlling SH1106 OLED displays over 
I2C or SPI interfaces. It supports basic drawing operations, text rendering, 
and display configuration.

### Usage Examples:

#### SPI Interface:
```python
from machine import Pin, SPI
import sh1106

spi = SPI(1, baudrate=1000000)
display = sh1106.SH1106_SPI(128, 64, spi, dc=Pin(5), res=Pin(2), cs=Pin(4))
display.fill(0)  # Clear the display
display.text("Hello, World!", 0, 0, 1)  # Display text
display.show()
```

#### I2C Interface:
```python
from machine import Pin, I2C
import sh1106

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
display = sh1106.SH1106_I2C(128, 64, i2c, res=Pin(16))
display.fill(0)  # Clear the display
display.text("Hello, World!", 0, 0, 1)  # Display text
display.show()
```

### Features:
- Supports 128x64 SH1106 OLED displays.
- Drawing primitives (lines, rectangles, circles, etc.).
- Text rendering.
- Contrast adjustment and screen inversion.

For more details, visit the [SH1106 GitHub repository](https://github.com/robert-hh/SH1106).
"""

# sh1106.pyi - Stub file for SH1106 MicroPython library
from abc import abstractmethod
from typing import Optional, overload

from _typeshed import Incomplete
from framebuf import FrameBuffer
from machine import I2C, SPI, Pin

class SH1106(FrameBuffer):
    """
    Base class for SH1106 OLED display drivers.
    Handles common functionality such as rendering, power management, and drawing operations.
    """
    def __init__(self, width: int, height: int, external_vcc: bool, rotate: int = 0) -> None:
        """
        Initialize the SH1106 driver.
        
        :param width: Display width in pixels.
        :param height: Display height in pixels.
        :param external_vcc: Whether to use external VCC (True) or internal (False).
        :param rotate: Rotation angle (0, 90, 180, 270 degrees).
        """
        ...

    @abstractmethod
    def write_cmd(self, *args, **kwargs) -> Incomplete: ...

    @abstractmethod
    def write_data(self,  *args, **kwargs) -> Incomplete: ...

    def init_display(self) -> None:
        """Initialize and reset the display."""
        ...

    def poweroff(self) -> None:
        """Turn off the display."""
        ...

    def poweron(self) -> None:
        """Turn on the display."""
        ...

    def flip(self, flag: Optional[bool] = None, update: bool = True) -> None:
        """
        Flip the display horizontally or vertically.
        
        :param flag: If True, enable flipping; if False, disable.
        :param update: Whether to update the display immediately.
        """
        ...

    def sleep(self, value: bool) -> None:
        """
        Put the display into sleep mode or wake it up.
        
        :param value: True to sleep, False to wake up.
        """
        ...

    def contrast(self, contrast: int) -> None:
        """
        Set the display contrast level.
        
        :param contrast: Contrast value (0-255).
        """
        ...

    def invert(self, invert: bool) -> None:
        """
        Invert the display colors.
        
        :param invert: True to invert, False to reset to normal.
        """
        ...

    def show(self, full_update: bool = False) -> None:
        """
        Refresh the display with the current buffer content.
        
        :param full_update: If True, update all pages; otherwise, update only modified pages.
        """
        ...
    @overload
    def pixel(self, x: int, y: int, /) -> int:
        """
        Get or set the color of a specific pixel.
        
        :param x: X-coordinate.
        :param y: Y-coordinate.
        :param color: Pixel color (0 or 1). If None, return the current color.
        """
        ...    
    @overload
    def pixel(self, x: int, y: int, color: int) -> None:
        """
        Get or set the color of a specific pixel.
        
        :param x: X-coordinate.
        :param y: Y-coordinate.
        :param color: Pixel color (0 or 1). If None, return the current color.
        """
        ...

    def text(self, text: str, x: int, y: int, color: int = 1) -> None:
        """
        Draw text on the display.
        
        :param text: String to draw.
        :param x: X-coordinate of the top-left corner.
        :param y: Y-coordinate of the top-left corner.
        :param color: Text color (1 for white, 0 for black).
        """
        ...

    def line(self, x0: int, y0: int, x1: int, y1: int, color: int) -> None:
        """Draw a line between two points."""
        ...

    def hline(self, x: int, y: int, w: int, color: int) -> None:
        """Draw a horizontal line."""
        ...

    def vline(self, x: int, y: int, h: int, color: int) -> None:
        """Draw a vertical line."""
        ...

    def fill(self, color: int) -> None:
        """Fill the entire display with a single color."""
        ...

    def blit(self, fbuf: FrameBuffer, x: int, y: int, key: int = -1, palette: Optional[bytes] = None) -> None:
        """
        Copy a framebuffer onto the display.
        
        :param fbuf: Source framebuffer.
        :param x: X-coordinate for placement.
        :param y: Y-coordinate for placement.
        :param key: Transparent color key.
        :param palette: Optional color palette for translation.
        """
        ...

    def scroll(self, x: int, y: int) -> None:
        """Scroll the display content by a certain amount."""
        ...

    def fill_rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        """Draw a filled rectangle."""
        ...

    def rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        """Draw an outlined rectangle."""
        ...

    def ellipse(self, x: int, y: int, xr: int, yr: int, color: int) -> None:
        """Draw an outlined ellipse."""
        ...

    def reset(self, res: Optional[Pin]=None) -> None:
        """Reset the display using the reset pin."""
        ...

class SH1106_I2C(SH1106):
    """
    SH1106 driver for I2C communication.
    """
    def __init__(self, width: int, height: int, i2c: I2C, res: Optional[Pin] = None, 
                 addr: int = 0x3c, rotate: int = 0, external_vcc: bool = False, delay: int = 0) -> None:
        """
        Initialize the SH1106 I2C driver.
        """
        ...

    def write_cmd(self, cmd: int) -> None:
        """Write a command to the display via I2C."""
        ...

    def write_data(self, buf: bytes) -> None:
        """Write data to the display via I2C."""
        ...

    def reset(self, res: Optional[Pin]=None) -> None:
        """Reset the display via the reset pin (if available)."""
        ...

class SH1106_SPI(SH1106):
    """
    SH1106 driver for SPI communication.
    """
    def __init__(self, width: int, height: int, spi: SPI, dc: Pin, res: Optional[Pin] = None, 
                 cs: Optional[Pin] = None, rotate: int = 0, external_vcc: bool = False, delay: int = 0) -> None:
        """
        Initialize the SH1106 SPI driver.
        """
        ...

    def write_cmd(self, cmd: int) -> None:
        """Write a command to the display via SPI."""
        ...

    def write_data(self, buf: bytes) -> None:
        """Write data to the display via SPI."""
        ...

    def reset(self, res: Optional[Pin]=None) -> None:
        """Reset the display via the reset pin (if available)."""
        ...
