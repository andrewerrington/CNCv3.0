#!/usr/bin/env bash

# A short bash script to start the CNC program
# It kills the PiGPIO server when the CNC program exits,
# so that all servos will stop.
sudo pigpiod
python3 cncv30.py
sudo killall pigpiod
