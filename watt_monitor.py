"""
WS2812B LED Strip Watt Monitor for RasPi

https://github.com/sadaoikebe/ws2812-ant-monitor

usage: sudo python3 watt_monitor.py

LED arrangement:

    First connected LED from Pi is a right center of ones digit, then going up,
    drawing an S letter from top, left-top, center, right-bottom, bottom, left-bottom
    then wire to the tens digit.

                    <------- ^
                  |          |
    +------+      | +------+ |
    |      |      | |      | |
    |      |      v | ---> |  <---
    +------+        +------+
    |      | <---   |      | |
    |      |      ^ |      | |
    +------+      | +------+ |
                  |          v
                  | <------+

    Please note your LED strip should withstand splash of your sweat.

"""

# %%
import sys
import time
import board
import neopixel
from powermeter import PowerMeter

# number of LEDs in each horizontal/vertical segment
H_LEDS = 5
V_LEDS = 4

# GPIO Pin connected to the first LED
pixel_pin = board.D18

# FTP in watts in order to determine color
FTP = 315

# 7 segment LED counts
LED_COUNT_DIGIT = V_LEDS * 4 + H_LEDS * 3
LED_COUNT_THOUSAND = V_LEDS * 2

# 3.1 digits
# thousands contain only two vertical segments
LED_COUNT_ALL = LED_COUNT_THOUSAND + LED_COUNT_DIGIT * 3

# %%
# determine onoff for ones, tens, hundreds
def onoff_single_digit(x):
    a = []
    vtrue = [True] * V_LEDS
    vfalse = [False] * V_LEDS
    htrue = [True] * H_LEDS
    hfalse = [False] * H_LEDS

    if x == '0' or x == '1' or x == '2' or x == '3' or x == '4' or x == '7' or x == '8' or x == '9':
        a.extend(vtrue)
    else:
        a.extend(vfalse)

    if x == '0' or x == '2' or x == '3' or x == '5' or x == '6' or x == '7' or x == '8' or x == '9':
        a.extend(htrue)
    else:
        a.extend(hfalse)

    # remove x == 7 if you like seven without hook
    if x == '0' or x == '4' or x == '5' or x == '6' or x == '7' or x == '8' or x == '9':
        a.extend(vtrue)
    else:
        a.extend(vfalse)

    if x == '2' or x == '3' or x == '4' or x == '5' or x == '6' or x == '8' or x == '9':
        a.extend(htrue)
    else:
        a.extend(hfalse)

    if x == '0' or x == '1' or x == '3' or x == '4' or x == '5' or x == '6' or x == '7' or x == '8' or x == '9':
        a.extend(vtrue)
    else:
        a.extend(vfalse)

    if x == '0' or x == '2' or x == '3' or x == '5' or x == '6' or x == '8' or x == '9':
        a.extend(htrue)
    else:
        a.extend(hfalse)

    if x == '0' or x == '2' or x == '6' or x == '8':
        a.extend(vtrue)
    else:
        a.extend(vfalse)

    return a

# determine onoff for thousands
def onoff_thousand_digit(x):
    return ([x == '1'] * LED_COUNT_THOUSAND)

# %%
# determine onoff for entire 3.1 digits
def generate_onoff(w):
    s = "{:4d}".format(w)
    # [ ones tens hundreds thousands ]
    return onoff_single_digit(s[3]) + onoff_single_digit(s[2]) + onoff_single_digit(s[1]) + onoff_thousand_digit(s[0]) 

# %%
# gradually change color, determine by FTP ratio
def ftpp_color2(x):
    r = g = b = 0
    if 0 <= x < 0.4:
        # gray with decaying luminance
        r = g = b = 0.566 * x
    elif 0.4 <= x < 0.52:
        # gray to blue
        r = g = -3.3 * x + 2.72 * x * x + 1.11
        b = 13 * x - 8.6 * x * x - 3.59
    elif 0.52 <= x < 0.62:
        # blue to cyan
        r = -7.23 * x + 5.24 * x * x + 2.47
        g = 5.56 * x - 1.897 * x * x - 2.25
        b = -4.3 * x + 3.08
    elif 0.62 <= x < 0.85:
        # cyan to green
        g = 3.34 * x - 1.67 * x * x - 0.96
        b = -5.852 * x + 2.893 * x * x + 2.93
    elif 0.85 <= x < 0.91:
        # green to yellow (1)
        r = 64.13 * x - 33.87 * x * x - 30.03
        g = -38.65 * x + 20.42 * x * x + 18.77
        b = -5.852 * x + 2.893 * x * x + 2.93
    elif 0.91 <= x < 1.05:
        # green to yellow (2)
        r = 14.887 * x - 6.923 * x * x - 7.53
        g = -10.634 * x + 4.946 * x * x + 6.09
    elif 1.05 <= x < 1.5:
        # yellow to red
        r = 1.17 * x - 0.76
        g = -0.82 * x + 1.24
    elif 1.5 <= x:
        # 100% red
        r = 1
    return r,g,b

# initialize neopixel
pixels = neopixel.NeoPixel(pixel_pin, LED_COUNT_ALL, brightness=0.2, auto_write=False, pixel_order=neopixel.GRB)

# called when the power is updated
def show_led(pwr):
    global pixels
    onoff = generate_onoff(pwr)
    rgb = ftpp_color2(pwr / FTP)
    for i in range(LED_COUNT_ALL):
        if onoff[i]:
            pixels[i] = (int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))
        else:
            pixels[i] = (0,0,0)
    pixels.show()

with PowerMeter(serial='/dev/ttyUSB0', netkey=[0xb9, 0xa5, 0x21, 0xfb, 0xbd, 0x72, 0xc3, 0x45], report=show_led) as pwr:
    pwr.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)
