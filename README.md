# Ambient Light Sensor Emulator for [wluma](https://github.com/maximbaz/wluma)

This is a fake ambient light sensor for those who don't get one built into in their laptop.

Mainly done for [wluma](https://github.com/maximbaz/wluma) and based on [@maximbaz](https://github.com/maximbaz)'s work.
'
`wluma` is a great project that sets screen brighness based on screen contents and ambient light around you.

The following modes are available:

- `webcam`: takes a webcam capture with ffmpeg and approximates ambient light value out of image brightness.
- `time`: approximates ambient light value based on the current time.

## Dependencies

- `ffmpeg` (needed for webcam mode)
- `python-pillow` (needed for webcam mode)

## Installation

On Arch Linux, use AUR packages `wluma-als-emulator` or `wluma-als-emulator-git`.

## Usage

```bash
wluma-als-emulator [--help]
```
