# WS2812B LED Strip Watt Monitor controller for RasPi
2019/12/19 Sadao Ikebe

This is for Python 3.x, not compatible with Python 2.x

## What you need
* Raspberry Pi
* USB-ANT+ dongle (or nRF24AP2 serial device would work, though I haven't tested)
* NeoPixel LED strip (or any cheap WS2812B / SK6812 LED strips would work)
* DC5V power adapter
* Some lead wire
* Solder

## Wiring
https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring

The section Using External Power Source Without Level Shifting is most helpful, the wiring is:

* Pi GND to NeoPixel GND
* Pi GPIO18 to NeoPixel DIN
* Power Supply GND to NeoPixel GND
* Power Supply 5V to NeoPixel 5V

just 4 wire would perfectly work.
I don't think level shifter is necessary.

## Power supply rating
The LED might draw 60mA per chip on 5V line when it's max brightness white, however that max draw is unthinkable using this watt monitor.

If you use ~100 LEDs on this project, consider using 5V 2A power supply, it should perfectly work.

1A adapter would also work but less margin.

## LED counts and arrangement
Need to set up 3.1 digits with 7 segments so we need at least 23 segments.

If you are monster who is able to go beyond 1999 watts you need 28 segments :) If you won't go beyond 999 watts you just need 21.

If you show bare LEDs I recommend at least four LEDs per segment for readability, so 92 LEDs are necessary.

Because the WS2812B LEDs are so bright, once you are able to build a fixture like frosted acrylic plate, one LED per segment would be okay.

First connected LED from Pi is a right center of ones digit, and going up,
drawing an S letter like top, left-top, center, right-bottom, bottom, left-bottom
then go to the tens letter.

# USB port setup
add this line to /etc/udev/rules.d/garmin-ant2.rules

    SUBSYSTEM=="usb", ATTRS{idVendor}=="0fcf", ATTRS{idProduct}=="1008", RUN+="/sbin/modprobe usbserial vendor=0x0fcf product=0x1008", MODE="0666", OWNER="pi", GROUP="root"
product ID of your ANT+ stick might not be 1008, check with **lsusb** or **dmesg | tail**

# Prerequisite
https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage

    sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel

https://github.com/mch/python-ant

    git clone https://github.com/mch/python-ant
    cd python-ant
    sudo python3 setup.py install
