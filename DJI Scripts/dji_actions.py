"""
Contains the camera actions used in 'entry_keyboard_control'
"""

from dji_commands import build_record_command
from dji_protocol import build_frame, next_seq
from dji_structs import build_camera_mode_switch


async def start_recording(ble, device_id):
    payload = build_record_command(device_id, start=True)
    frame = build_frame(0x1D, 0x03, 0x00, payload, next_seq())
    await ble.write(frame)


async def stop_recording(ble, device_id):
    payload = build_record_command(device_id, start=False)
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
