# Ambient Light Sensor Emulator for [wluma](https://github.com/maximbaz/wluma)

This is a fake ambient light sensor for those who don't get one built into in their laptop.

Mainly done for [wluma](https://github.com/maximbaz/wluma) and based on [@maximbaz](https://github.com/maximbaz)'s work.
'
`wluma` is a great project that sets screen brighness based on screen contents and ambient light around you.

The following modes are available:

- `webcam`: takes a webcam capture with ffmpeg and approximates ambient light value out of image brightness.
- `time`: approximates ambient light value based on the current time.

## Dependencies

See `requirements.txt`:

- `ffmpeg` (needed for webcam mode)
- `python-pillow` (needed for webcam mode)
- `python-requests` (needed for requests api)

## Installation

On Arch Linux, use AUR packages `wluma-als-emulator` or `wluma-als-emulator-git`.
Releases are signed with my PGP key: [FC9B1319726657D3](https://levis.name/pgp_keys.asc) .

## Usage

```bash
wluma-als-emulator [-h|--help]
```

# Developement

## Run

To make a quick test from a virtualenv

```bash
make ARGS="--help" run
make ARGS="-t noon -s 3" run
```

## Tests

```bash
tox
```
