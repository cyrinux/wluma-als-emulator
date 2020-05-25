"""
wluma-als-emulator
"""

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages
import fastentrypoints  # noqa f401


with open("README.rst") as f:
    description = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="wluma-als-emulator",
    version="1.2.0",
    description="Ambient light sensor emulator for wluma",
    long_description=description,
    long_description_content_type="text/x-rst",
    author="Cyril Levis",
    author_email="alse@levis.name",
    url="https://github.com/cyrinux/wluma-als-emulator",
    download_url="https://github.com/cyrinux/wluma-als-emulator/tags",
    license=license,
    include_package_data=True,
    packages=find_packages(exclude=("tests", "docs")),
    install_requires=[],
    entry_points={"console_scripts": ["wluma-als-emulator = wluma_als_emulator:main"]},
    python_requires=">=3.8",
)
