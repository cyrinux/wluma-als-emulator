# Fake ambiant light sensor

This is fake a ambiant light sensor for those who don't get one builtin in there laptop.

Mainly done for Wluma and based on @maximbaz work.

Wluma is a great project that set brighness based on luma from what you are watching, and ambiance light.
See more [here](https://github.com/maximbaz/wluma).

If you don't got a light sensor on your laptop, use your webcam as a fake light (lux) sensor.
This will take a webcam capture with ffmpeg then approximate a lux value from this one.

_Wluma_ will be able to read it by using the `-l /tmp/fake_light_sensor` parameter.

## Requirement

- ffmpeg
- python-pyllow

## Installation

Archlinux, from AUR use `fake-light-sensor-git`. (not publish yet)

## Usage

```bash
fake-light-sensor [--help]
```
