#!/usr/bin/env python3

"""
This entry point allows toggling between file transfer mode and record/capture mode.
"""
"""
TODO:
- [X] Testing w/ file transfer
"""
from sys import stdin
import termios
from tty import setraw
from time import sleep

from uhubctl import disable_hub, enable_hub
from transfer_video import transfer_new_videos

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


async def remote_control_camera(ble, device_id):
    """Performs camera actions and shows menu options"""
    while True:
        print(
            "Make a selection:\n"
            "c. start recording/capture\n"
            "s. stop recording\n"
            "1. switch to video mode\n"
            "2. switch to camera/capture mode\n"
            "3. Return"
        )

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
        elif key == "3" or key == "q":
            await asyncio.sleep(0.5)
            break


async def main():
    disable_hub(2)
    disable_hub(4)

    ble = DJIBLE()
    try:
        await ble.connect()
    except Exception as e:
        if str(e) == "Camera not found":
            print("The camera was not found.")
            print("exiting...")
            return 1
        else:
            raise

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
        print(
            "Make a selection:\n"
            "1. Record/capture mode\n"
            "2. File transfer mode\n"
            "3. Disconnect"
        )

        key = get_key()
        if key == "1":
            await asyncio.sleep(0.5)
            await remote_control_camera(ble, device_id)
            await asyncio.sleep(0.5)

        elif key == "2":
            await asyncio.sleep(0.5)
            enable_hub(2)
            enable_hub(4)

            transfer_attempts = 3
            transfer_delay_time = 4
            transfer_buffer = 1
            for i in range(transfer_attempts):
                try:
                    print("\nAttempting file transfer...")
                    await asyncio.sleep(transfer_delay_time)
                    transfer_new_videos()
                    await asyncio.sleep(transfer_buffer)
                    break
                except FileNotFoundError as e:
                    if i == transfer_attempts:
                        print("Path does not exist. Returning to main menu...")
                    pass

            await asyncio.sleep(0.5)
            disable_hub(2)
            disable_hub(4)
            await asyncio.sleep(2)

        elif key == "3" or key == "q":
            await asyncio.sleep(0.25)
            break

    await asyncio.sleep(1)
    try:
        await ble.disconnect()
    except EOFError:
        # already disconnected
        pass
    await asyncio.sleep(1)
    enable_hub(2)
    enable_hub(4)
    sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
