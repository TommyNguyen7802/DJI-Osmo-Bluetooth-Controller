from dji_protocol import build_frame, next_seq
import struct

def build_connection_request(device_id, mac, fw_version, verify_mode, verify_data):
    payload = struct.pack("<I", device_id)
    payload += bytes([len(mac)]) + bytes(mac)
    payload += struct.pack("<I", fw_version)
    payload += bytes([verify_mode])
    payload += struct.pack("<H", verify_data)
    return payload

def build_record_command(device_id, start=True):
    ctrl = 0x00 if start else 0x01
    payload = struct.pack("<IB4s", device_id, ctrl, b'\x00\x00\x00\x00')
    return payload
