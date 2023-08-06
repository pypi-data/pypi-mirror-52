# Raspberry-Pi-based Mopidy controller prototype

**Note**: This project assumes your Mopidy installation uses
          [MQTT control backend](https://github.com/odiroot/mopidy-mqtt).

## Schematics

[![Fritzing model](./docs/sketch_rpi_bb.png "Fritzing model")](./docs/sketch_rpi.fzz)

## Built prototype

![Prototype in case](./docs/prototype.jpg "Built prototype")

## Components

* Raspberry Pi Zero W board.
* SSD1306 OLED, I²C-based 128×64 display.
* EVE-PDBRL408B rotary encoder with switch.

## Software stack

* Python 3.6.
* `luma.oled` (display driving).
  - `luma.emulator` (emulating display in development).
* `RPi.GPIO` (interfacing with hardware inputs).
  - `raspberry-gpio-emulator` (emulating GPIO inputs in development).
* `paho.mqtt` (MQTT communication).


