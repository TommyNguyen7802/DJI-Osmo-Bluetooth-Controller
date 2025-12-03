#!/usr/bin/env python3

"""
This entry point allows toggling between file transfer mode and record/capture mode.
"""
from uhubctl import disable_hub, enable_hub
import asyncio
from dji_ble import DJIBLE
from dji_commands import build_connection_request
from dji_protocol import build_frame, next_seq
from dji_actions import (
    start_recording,
    stop_recording,
    switch_mode_video,
    switch_mode_photo,
)


async def main():
    # Disable USB Ports
    # disable_hub(2)
    # disable_hub(4)

    # Connect to camera
    ble = DJIBLE()
    await ble.connect()

    # Send connection request
    device_id = 0x12345678
    mac = [0x04, 0xA8, 0x5A, 0x67, 0x90, 0x7B]
    fw_version = 0x01020304
    verify_mode = 0
    verify_data = 0x0000

    payload = build_connection_request(
        device_id, mac, fw_version, verify_mode, verify_data
    )
    frame = build_frame(0x00, 0x19, 0x00, payload, next_seq())
    await ble.write(frame)

    await asyncio.sleep(0.5)

    await asyncio.sleep(2)

    await ble.disconnect()

    await asyncio.sleep(1)

    # Once connection is established, offer recording mode or file transfer mode
    #   In recording mode, call `keyboard_control`
    #   In file transfer mode, enable usb ports and call the file transfer function
    #       When exiting file transfer mode, re-disable usb ports
    # On exit, disconnect camera and re-enable usb ports
    return


if __name__ == "__main__":
    main()
