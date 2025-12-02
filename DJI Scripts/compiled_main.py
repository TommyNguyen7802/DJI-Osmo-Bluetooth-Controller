#!/usr/bin/env python3

import asyncio
from uhubctl import disable_hub, enable_hub
from keyboard_control import keyboard_control
from transfer_video import transfer_new_videos
from time import sleep

async def main():
    # Disable all usb ports on Raspberry Pi 5
    disable_hub(2)
    disable_hub(4)

    sleep(0.5)

    # Camera logic
    asyncio.run(keyboard_control())

    sleep(0.5)

    # Enable all usb ports on Raspberry Pi 5
    enable_hub(2)
    enable_hub(4)

    # Transfer new videos via sftp
    transfer_new_videos()

if __name__ == "__main__":
    asyncio.run(main())
