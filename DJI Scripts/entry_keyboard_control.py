#!/usr/bin/env python3

"""
An entry point that allows functions to be controlled by keyboard entry

    TODO:
    - [ ] make actions trigger on key press
        - [X] take_photo
        - [ ] start_record
        - [ ] stop record
        - [ ] sleep switch
        - [ ] switch_camera_mode
    - [ ] move camera actions to separate file
    - [ ] update docs
"""

import asyncio
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from pynput import keyboard
from dji_ble import DJIBLE
from dji_commands import build_connection_request, build_record_command
from dji_protocol import build_frame, next_seq
from dji_structs import build_status_subscription, build_camera_mode_switch


async def take_photo(ble, device_id):
    payload = build_record_command(device_id, start=True)
    frame = build_frame(0x1D, 0x03, 0x00, payload, next_seq())
    await ble.write(frame)


def on_press_wrapper(ble, device_id, asyncio_running_loop):
    """Creates an on_press wrapper for `ble`, `device_id`, asyncio_running_loop params"""

    def on_press(key):
        """Handles key press events"""

        async def take_photo_caller():
            await asyncio.sleep(2)
            await take_photo(ble, device_id)
            print("you pressed 'c'!")
            await asyncio.sleep(2)

        try:
            if key.char == "p":
                asyncio.run_coroutine_threadsafe(
                    take_photo_caller(), asyncio_running_loop
                )
            elif key.char == "q":
                print("quitting...")
                return False
        except AttributeError:
            pass

    return on_press


async def main():
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

    await asyncio.sleep(2)

    asyncio_running_loop = asyncio.get_running_loop()
    with keyboard.Listener(
        on_press=on_press_wrapper(ble, device_id, asyncio_running_loop)
    ) as listener:
        await asyncio.to_thread(listener.join)

    # await take_photo(ble, device_id)

    # await asyncio.sleep(2)

    # await take_photo(ble, device_id)

    # await asyncio.sleep(2)

    # await asyncio.sleep(2)
    # print("Press ... or 'q' to quit")

    # Take Photo
    # payload = build_record_command(device_id, start=True)
    # frame = build_frame(0x1D, 0x03, 0x00, payload, next_seq())
    # await ble.write(frame)

    # await asyncio.sleep(2)

    await ble.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
