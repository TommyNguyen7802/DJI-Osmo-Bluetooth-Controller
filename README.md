# Python Script to Remotely Control DJI Osmo Action 5 (WIP: Updated December 1, 2025)
This script will allow you to control an DJI Osmo Action 5 via bluetooth over the BLE communication protocol.
DJI uses a proprietary protocol for connecting over bluetooth, so this script allows you to pair a regular computer
that is equipped with bluetooth LE capabilities (BT 4.0 and newer) and control the camera.

## Dependencies
- Python 3
- Bleak
- Bluez
- Bluetooth
- uhubctl
- paramiko

  
Quick install for Linux

sudo apt install python3 python3-bleak bluetooth bluez uhubctl paramiko


## Getting Started
Navigate to the DJI Scripts folder and open a termainal. To run the base script, type in the following:

python3 main.py
