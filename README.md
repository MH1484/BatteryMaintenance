# BatteryMaintenance

This repository contains different scripts to charge batteries and create statistics

## user_manual.md

This document guides a user to maintain batteries.

## battery_charging.py

To use this script, open it and adjust the IP adress of the used Shelly Plug S device.
Watch the used packages and install the required ones by using 'pip install ...'.

When starting this script, it switches the Shelly Plug S on.
Afterwards, it tracks the power consumption once per second until the user ends the script with Ctrl+C.
When stopping this script, it switches the Shelly Plug S off.

## battery_statistics.py

This script analyses all csv files inside the repository and prints a statistic.</br>
This allows cross-battery comparisms as well as historical comparisms for a single battery.

| File                        | First    | Latest   | Duration | MaxPower |
|-----------------------------|----------|----------|----------|----------|
| .\G-197791\2026-04-12.csv   | 06:18:19 | 09:50:19 | 3:32:00  | 6.7W     |
| .\G-174870\2026-04-11.csv   | 11:43:37 | 12:23:27 | 0:39:50  | 2.1W     |
| .\G-174873\2026-04-11.csv   | 13:47:03 | 15:00:07 | 1:13:04  | 2.9W     |
| .\G-174877\2026-04-11.csv   | 16:53:55 | 20:16:49 | 3:22:54  | 6.8W     |
| .\G-205927\2026-04-11.csv   | 20:42:39 | 23:25:59 | 2:43:20  | 6.2W     |
| .\G-493570\2026-04-11.csv   | 06:33:50 | 10:32:49 | 3:58:59  | 6.7W     |
