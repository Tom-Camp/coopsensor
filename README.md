# Coop Sensor

A [CircuitPython](https://circuitpython.org/) application measuring temperature, humidity, and metal-oxide (MOX) gas in
a chicken coop. The `coop sensor` displays data on a [2.9" flexible E-Ink display](https://www.adafruit.com/product/4262).

## Getting Started

### Prerequisites

#### Hardware

* [RP2040](https://www.raspberrypi.com/documentation/microcontrollers/rp2040.html) MCU
* [E-Ink](https://www.adafruit.com/search?q=e-ink+display) display
* [Temperture and humidity sensor](https://www.adafruit.com/product/4566)
* [Air Quality Sensor](https://www.adafruit.com/product/3709)

The choices of components that I made were made for simplicity. I chose to use the
[RP2040 Feather ThinkInk](https://www.adafruit.com/product/5727) board and the
[2.9" flexible E-Ink display](https://www.adafruit.com/product/4262) because I didn't need to wire up the display. I
chose the [AHT20](https://www.adafruit.com/product/4566) temp and humidity sensor and the
[SGP30 Air Quality Sensor](https://www.adafruit.com/product/3709) because they use
[STEMMA QT](https://learn.adafruit.com/introducing-adafruit-stemma-qt) connectors.

#### Software

I did not include libraries needed for this project. If you are doing any CircuitPython programming on MCUs you are
going to want the Adafruit Circuit Python library bundle, so you might as well download/clone it now.

* [CircuitPython](https://circuitpython.org/downloads) specific to your board
* The [Adafruit Circuit Python library bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle)

### Installation

Once you have flashed the MCU with the CircuitPython u2f file, it will show on your computer as a drive;
(`/media/[YOUR USER]/CircuitPy/` on Linux) and will include a `lib/` directory and a `code.py` file. Copy the following
files from the Adafruit Circuit Python library bundle to the `lib/` directory.

* [adafruit_epd](https://github.com/adafruit/Adafruit_EPD)
* [adafruit_sgp](https://docs.circuitpython.org/projects/sgp30/en/latest/)
* [adafruit_aht0](https://docs.circuitpython.org/projects/ahtx0/en/latest/)

Copy the `code.py`, `boot.py`, and the `logging.json` file from this repo root directory on your MCU.

## Authors

* Tom Camp - _Initial work_ - [Tom-Camp](https://github.com/Tom-Camp)

## License

This project is licensed under the [GNU General Public License version 3](LICENSE).

## Acknowledgments

* [Adafruit tutorials](https://learn.adafruit.com) are an invaluable resource learning.
* [Adafruit shop](https://adafruit.com) because learning inevitably means buying.
* [Digikey](https://digikey.com) another great resource for hardware.
