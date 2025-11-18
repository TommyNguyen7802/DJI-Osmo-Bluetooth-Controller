#!/bin/bash
# usb_toggle.sh
# Demo USB bind/unbind script
# This script unbinds and rebinds a device connected to usb port 3.1.
# Note: Unbinding does not appear to make the DJI OSMO exit the file
# transfer mode.

# (Specific device appears to be 1-3.9)
PORT="1-3"
ACTION=$1

echo "Hello, Linux Mint!"

sleep 0.5

if [ "$ACTION" == "disable" ]; then
    echo "We will disable USB port $PORT."
    sleep 0.5
    echo "$PORT" | sudo tee /sys/bus/usb/drivers/usb/unbind
    sleep 0.5
    echo "Unbinded USB port $PORT"
    sleep 0.5

elif [ "$ACTION" == "enable" ]; then
    echo "We will enable USB port $PORT."
    sleep 0.5
    echo "$PORT" | sudo tee /sys/bus/usb/drivers/usb/bind
    sleep 0.5
    echo "Re-binded USB port $PORT."
    sleep 0.5

else
    echo "Usage: sudo ./usb_toggle.sh [enable|disable]"

fi

sleep 0.5

echo "Goodbye!"

sleep 0.5