#!/usr/bin/env python3

"""
An entry point that allows functions to be controlled by keyboard entry

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
            - [ ] move camera actions to separate file
            - [ ] misc.
    - [ ] implement fix for sleep/wake modes
    - [ ] implement camera status/state
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


async def start_recording(ble, device_id):
    payload = build_record_command(device_id, start=True)
    frame = build_frame(0x1D, 0x03, 0x00, payload, next_seq())
    await ble.write(frame)


async def stop_recording(ble, device_id):
    payload = build_record_command(device_id, start=False)
    frame = build_frame(0x1D, 0x03, 0x00, payload, next_seq())
    await ble.write(frame)


async def take_photo(ble, device_id):
    payload = build_record_command(device_id, start=True)
    frame = build_frame(0x1D, 0x03, 0x00, payload, next_seq())
    await ble.write(frame)


async def switch_mode_video(ble, device_id):
    payload = build_camera_mode_switch(device_id, 0x01)
    frame = build_frame(0x1D, 0x04, 0x00, payload, next_seq())
    await ble.write(frame)


async def switch_mode_photo(ble, device_id):
    payload = build_camera_mode_switch(device_id, 0x05)
    frame = build_frame(0x1D, 0x04, 0x00, payload, next_seq())
    await ble.write(frame)


def on_press_wrapper(ble, device_id, asyncio_running_loop):
    """Creates an on_press wrapper for `ble`, `device_id`, asyncio_running_loop params"""

    def on_press(key):
        """Handles key press events"""

        async def take_photo_caller():
            await asyncio.sleep(2)
            await take_photo(ble, device_id)
            print("you took a photo")
            await asyncio.sleep(2)

        async def start_recording_caller():
            await asyncio.sleep(2)
            await start_recording(ble, device_id)
            print("you started recording")
            await asyncio.sleep(2)

        async def stop_recording_caller():
            await asyncio.sleep(2)
            await stop_recording(ble, device_id)
            print("you stopped recording")
            await asyncio.sleep(2)

        async def switch_mode_video_caller():
            await asyncio.sleep(2)
            await switch_mode_video(ble, device_id)
            print("you switched to video mode")
            await asyncio.sleep(2)

        async def switch_mode_photo_caller():
            await asyncio.sleep(2)
            await switch_mode_photo(ble, device_id)
            print("you switched to photo mode")
            await asyncio.sleep(2)

        try:
            if key.char == "p":
                asyncio.run_coroutine_threadsafe(
                    take_photo_caller(), asyncio_running_loop
                )
            elif key.char == "v":
                asyncio.run_coroutine_threadsafe(
                    start_recording_caller(), asyncio_running_loop
                )
            elif key.char == "s":
                asyncio.run_coroutine_threadsafe(
                    stop_recording_caller(), asyncio_running_loop
                )
            elif key.char == "1":
                asyncio.run_coroutine_threadsafe(
                    switch_mode_video_caller(), asyncio_running_loop
                )
            elif key.char == "2":
                asyncio.run_coroutine_threadsafe(
                    switch_mode_photo_caller(), asyncio_running_loop
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
