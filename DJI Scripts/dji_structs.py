# dji_structs.py

import struct

def pad_mac(mac: bytes) -> bytes:
    return mac.ljust(16, b'\x00')

def build_connection_request(device_id, mac, fw_version, verify_mode, verify_data):
    return struct.pack(
        "<I B 16s I B H 4s",
        device_id,
        len(mac),
        pad_mac(mac),
        fw_version,
        verify_mode,
        verify_data,
        b'\x00\x00\x00\x00'
    )

def build_connection_response(device_id, ret_code=0, camera_reserved=0x01):
    reserved = bytearray(4)
    reserved[0] = camera_reserved
    return struct.pack("<I B 4s", device_id, ret_code, reserved)

def build_record_control(device_id, start=True):
    ctrl = 0x00 if start else 0x01
    return struct.pack("<I B 4s", device_id, ctrl, b'\x00\x00\x00\x00')
# Expected build_camera_mode_switch Payload Structure:
#   payload = build_record_command(device_id, start=True)
#   frame = build_frame(0x1D, 0x03, 0x00, payload, next_seq())
#   await ble.write(frame)
# Where start=True to start recording, False to stop recording.

def build_camera_mode_switch(device_id, mode):
    return struct.pack("<I B 4s", device_id, mode, b'\x01\x47\x39\x36')
# Expected build_camera_mode_switch Payload Structure:
#   payload = build_camera_mode_switch(device_id, 0x00)
#   frame = build_frame(0x1D, 0x04, 0x00, payload, next_seq())
#   await ble.write(frame)
# Where mode can be:
#   0x01: Video
#   0x05: Photo
#   0x02: Timelapse Video (Untested)
#   0x0A: Hyperlapse Video (Untested)
#   0x00: Slow Motion Video
#   0x28: Low Light Video (Untested)
#   0x34: Subject Follow Video (Untested)
#   0x1A: Live Stream via RTMP (Untested)
#   0x23: UVC Live Stream via USB (Untested)



def build_key_report_qs():
    return struct.pack("<B B H", 0x02, 0x01, 0x0000)

def build_power_mode_switch(sleep=True):
    mode = 0x03 if sleep else 0x00
    return struct.pack("<B", mode)

def build_status_subscription(push_mode=3, push_freq=20):
    return struct.pack("<B B 4s", push_mode, push_freq, b'\x00\x00\x00\x00')
