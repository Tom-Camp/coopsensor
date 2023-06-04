import json
import time

import adafruit_ahtx0
import alarm
import board
import busio
import digitalio
from adafruit_epd.epd import Adafruit_EPD
from adafruit_epd.uc8151d import Adafruit_UC8151D
from adafruit_sgp30 import Adafruit_SGP30

i2c = board.STEMMA_I2C()
aht_sensor = adafruit_ahtx0.AHTx0(i2c)
aht_sensor.calibrate()

temperature_celsius = aht_sensor.temperature
temperature = round(temperature_celsius * (9 / 5) + 32)
relative_humidity = aht_sensor.relative_humidity
humidity = round(relative_humidity)


def check_mox(baseline: list) -> tuple:
    """Do moxy stuff here"""


error: str = ""
try:
    with open("log.json", "r") as logfile:
        log_data = json.load(logfile)
except OSError as e:
    error = f"ERROR: {e}"

sgp30 = Adafruit_SGP30(i2c)
sgp30.set_iaq_baseline(0x8973, 0x8AAE)
sgp30.set_iaq_relative_humidity(temperature_celsius, relative_humidity)
for x in range(0, 19):
    eco2, tvoc = sgp30.baseline_eCO2, sgp30.baseline_TVOC

results: tuple = (temperature, humidity, eco2, tvoc)

last_six = log_data.get("last_six")
if len(last_six) >= 5:
    last_six = last_six[-4:]
last_six.append(results)

try:
    with open("log.json", "w+") as outfile:
        json.dump(last_six, outfile)
except OSError as e:
    error = f"ERROR: {e}"

spi = busio.SPI(board.EPD_SCK, MOSI=board.EPD_MOSI)
ecs = digitalio.DigitalInOut(board.EPD_CS)
dc = digitalio.DigitalInOut(board.EPD_DC)
srcs = None
rst = digitalio.DigitalInOut(board.EPD_RESET)
busy = digitalio.DigitalInOut(board.EPD_BUSY)

display = Adafruit_UC8151D(
    128,
    296,
    spi,
    cs_pin=ecs,
    dc_pin=dc,
    sramcs_pin=srcs,
    rst_pin=rst,
    busy_pin=busy,
)

display.set_black_buffer(1, True)
display.set_color_buffer(1, True)
display.rotation = 1

display.fill(Adafruit_EPD.WHITE)
display.pixel(10, 100, Adafruit_EPD.BLACK)

column_width = int(round(display.width, 0) / 3)

display.text(f"Temp: {results[0]}F", 2, 5, Adafruit_EPD.BLACK)
display.vline(column_width, 2, display.height - 12, Adafruit_EPD.BLACK)
display.text(f"Humidity: {results[1]}%", column_width + 5, 5, Adafruit_EPD.BLACK)
display.vline(column_width * 2, 2, display.height - 12, Adafruit_EPD.BLACK)
display.text(f"vCO2: {results[2]} ppm", column_width * 2 + 5, 5, Adafruit_EPD.BLACK)
display.text("Last hour", 2, 20, Adafruit_EPD.BLACK)
display.text("Last hour", column_width + 5, 20, Adafruit_EPD.BLACK)
display.text(f"TVOC: {results[3]} ppb", column_width * 2 + 5, 20, Adafruit_EPD.BLACK)

t_bar_x: int = 25
h_bar_x: int = column_width + 5
bar_y: int = 35
for data in last_six:
    t_length = (data[0] - 25) if data[0] > 32 else data[0]
    display.fill_rect(2, bar_y, t_length, 10, Adafruit_EPD.BLACK)
    display.text(f"{data[0]}F: ", t_length + 5, bar_y, Adafruit_EPD.BLACK)

    h_length = data[1] - 25 if data[1] > 32 else data[1]
    display.fill_rect(h_bar_x, bar_y, h_length, 10, Adafruit_EPD.BLACK)
    display.text(f"{data[1]}%: ", h_bar_x + h_length + 5, bar_y, Adafruit_EPD.BLACK)
    bar_y += 15

if error:
    display.text(error, 5, display.height - 10, Adafruit_EPD.BLACK)
display.display()

time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 30)
# time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 720)
alarm.exit_and_deep_sleep_until_alarms(time_alarm)
