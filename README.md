# Python Script to Remotely Control DJI Osmo Action 5 (WIP: Updated January 27, 2025)
This script will allow you to control an DJI Osmo Action 5 via bluetooth over the BLE communication protocol.
DJI uses a proprietary protocol for connecting over bluetooth, so this script allows you to pair a regular computer
that is equipped with bluetooth LE capabilities (BT 4.0 and newer) and control the camera.

The DJI control scripts are universally compatible but our main script is tailored specifically for a Raspberry Pi 5 running 64-Bit Raspberry Pi OS. Instructions should mostly be the same on debian based distros.

### Dependencies
- Python 3
- Bleak
- Bluez
- Bluetooth
- uhubctl
- paramiko
- git

## Setting up the Environment
Assuming you have a Raspberry Pi 5 running 64-bit Pi OS, first thing you'll want to do is install the dependencies required to run the script.
```
sudo apt install python3 python3-bleak bluetooth bluez uhubctl paramiko git
```
Next you will want to setup the udev rules for uhubctl, which allows for the usb controller to be disabled without sudo. To do this you will want to create a new rule by creating `/etc/udev/rules.d/52-usb.rules` and adding:
```
SUBSYSTEM=="usb", DRIVER=="hub|usb", MODE="0664", GROUP="dialout"
# Linux 6.0 or later (its ok to have this block present for older Linux kernels):
SUBSYSTEM=="usb", DRIVER=="hub|usb", \
  RUN+="/bin/sh -c \"chown -f root:dialout $sys$devpath/*port*/disable || true\"" \
  RUN+="/bin/sh -c \"chmod -f 660 $sys$devpath/*port*/disable || true\""
```
and then add permitted users to `dialout` group:
```
sudo usermod -a -G dialout $USER
```
For your `udev` rule changes to take effect, reboot or run:
```
sudo udevadm trigger --attr-match=subsystem=usb
```
Referenced from: https://github.com/mvp/uhubctl

### Configuring Camera Permissions
Next you'll want to plug in the camera to the Pi. In our case, we used a DJI Osmo Action 5 Pro. Make sure the camera is in File Transfer mode or MTP. You will want to navigate to `/media/$USER`. Here you should be able to see the camera's folders mounted as Osmo_Action (internal memory) and SD_Card (external expansion). By default these are normally owned by the root user. You will want to change this so the script has read/write permissions. To do this, type in:
```
sudo chown -R $USER:$USER /media/$USER/Osmo_Action
```
or
```
sudo chown -R $USER:$USER /media/$USER/SD_Card
```
## Getting Started
You should now be ready to try out the script! Clone this repository:
```
git clone https://github.com/TommyNguyen7802/DJI-Osmo-Bluetooth-Controller.git
```
Then navigate to "`~/DJI-Osmo-Bluetooth-Controller/DJI\ Scripts`". You will want to configure the `sample_config.json` and rename it to `config.json`. It houses all the information needed to do the file transfer over SFTP via SSH. You then shoule be able to run the script by typing in:
```
python3 compiled-main.py
```
