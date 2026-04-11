# BatteryMaintenance

This repository contains different scripts to charge batteries and create statistics

## battery_charging.py

To use this script, open it and adjust the IP adress of the used Shelly Plug S device.
Watch the used packages and install the required ones by using 'pip install ...'.

When starting this script, it switches the Shelly Plug S on.
Afterwards, it tracks the power consumption once per second until the user ends the script with Ctrl+C.
When stopping this script, it switches the Shelly Plug S off.

## battery_statistics.py

This script analyses all csv files inside the repository and prints a statistic.
This allows cross-battery comparisms as well as historical comparisms for a single battery.
