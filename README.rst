Ambient Light Sensor Emulator for `wluma <https://github.com/maximbaz/wluma>`__
===============================================================================

DEPRECATED
==========

* Main goal is this project was ported in wluma itself under the config `als.webcam`, See `wluma 3.0.0 <https://github.com/maximbaz/wluma/releases/tag/3.0.0>`__.


This is a fake ambient light sensor for those who don’t get one built
into in their laptop.

Mainly done for `wluma <https://github.com/maximbaz/wluma>`__ and based
on `@maximbaz <https://github.com/maximbaz>`__'s work. ``wluma`` is a
great project that sets screen brighness based on screen contents and
ambient light around you.

The following modes are available:

-  ``webcam``: takes a webcam capture with ffmpeg and approximates
   ambient light value out of image brightness.
-  ``time``: approximates ambient light value based on the current time, all the day.
-  ``noon``: approximates ambient light value based on the current time with the noon as reference.
-  ``daylight``: approximates ambient light value based on the solar phases, twilight.

See `readthedoc <https://wluma-als-emulator.readthedocs.io/en/latest/>`__ for more informations.

Dependencies
------------

See ``requirements.txt``:

-  ``ffmpeg`` (needed for webcam mode)
-  ``python-pillow`` (needed for webcam mode)
-  ``python-requests`` (needed for requests api)

Installation
------------

On Arch Linux, use AUR packages ``wluma-als-emulator`` or
``wluma-als-emulator-git``. Releases are signed with my PGP key:
`FC9B1319726657D3 <https://levis.name/pgp_keys.asc>`__ .

Usage
-----

.. code:: bash

   wluma-als-emulator [-h|--help]

Developement
============

Run
---

To make a quick test from a virtualenv

.. code:: bash

   make ARGS="--help" run
   make ARGS="-t noon -s 3" run

Tests
-----

.. code:: bash

   tox
