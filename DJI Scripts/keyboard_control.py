#!/usr/bin/env python3

"""
Contains functions that allow for camera control by standard input (console).
An entry point is also provided.
"""
"""
    TODO:
    - [ ] make actions trigger on key press
        - [ ] Actions:
            - [X] take_photo
            - [X] start_record (same as take_photo)
            - [X] stop record
            - [ ] sleep switch
            - [X] switch_camera_mode
                - **Do any other modes need to be implemented?**
                - [X] video mode
                - [X] photo mode
        - [ ] Tidy and organize program for later flexibility
            - [X] move camera actions to separate file
            - [ ] misc.
    - [ ] implement fix for sleep/wake modes
    - [ ] implement camera status/state
    - [X] Make SSH friendly
    - [ ] update docs
"""

import asyncio
from sys import stdin
import termios
from tty import setraw

from dji_ble import DJIBLE
from dji_commands import build_connection_request
from dji_protocol import build_frame, next_seq
from dji_actions import (
    start_recording,
    stop_recording,
    switch_mode_video,
    switch_mode_photo,
)


def get_key():
    """Read a single keypress from stdin"""
    fd = stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        setraw(fd)
        charput = stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return charput

async def keyboard_control():
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

    while True:
        key = get_key()

        if key == "c":
            print("start recording/capture")
            await start_recording(ble, device_id)
        elif key == "s":
            print("stop recording")
            await stop_recording(ble, device_id)
        elif key == "1":
            print("switch to video mode")
            await switch_mode_video(ble, device_id)
        elif key == "2":
            print("switch to camera/capture mode")
            await switch_mode_photo(ble, device_id)
        elif key == "q":
            print("Disconnecting!")
            await asyncio.sleep(0.5)
            break

    await asyncio.sleep(0.5)

    await ble.disconnect()

def main():
    asyncio.run(keyboard_control())

if __name__ == "__main__":
    main()
