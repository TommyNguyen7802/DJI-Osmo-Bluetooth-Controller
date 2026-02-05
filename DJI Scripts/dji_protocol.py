import struct
from dji_crc import crc16, crc32
from dji_handlers import dispatch_handler

seq_counter = 0

def next_seq():
    global seq_counter
    seq_counter += 1
    return seq_counter & 0xFFFF

def build_frame(cmd_set, cmd_id, cmd_type, payload: bytes, seq: int):
    header = bytearray()
    header += b'\xAA'  # SOF
    ver_len = (0 << 10) | (12 + 2 + len(payload) + 4)
    header += struct.pack("<H", ver_len)
    header += bytes([cmd_type, 0x00])  # cmd_type, enc
    header += b'\x00\x00\x00'  # reserved
    header += struct.pack("<H", seq)
    header += struct.pack("<H", crc16(header))  # CRC16
    header += bytes([cmd_set, cmd_id])
    frame = header + payload
    frame += struct.pack("<I", crc32(frame))  # CRC32
    return frame

def handle_notification(data: bytes):
    if data[0] != 0xAA:
        print("Non-protocol notification")
        return
    # print(f"Notification: {data.hex()}")
    # TODO: parse frame, extract cmd_set/cmd_id, dispatch to handler

def parse_frame(frame: bytes):
    if len(frame) < 16 or frame[0] != 0xAA:
        # Hide when invalid frames are printed
        # print("❌ Invalid frame")
        return

    # Parse header
    ver_len = struct.unpack_from("<H", frame, 1)[0]
    version = ver_len >> 10
    expected_len = ver_len & 0x03FF
    if expected_len != len(frame):
        print(f"❌ Length mismatch: expected {expected_len}, got {len(frame)}")
        return

    crc16_recv = struct.unpack_from("<H", frame, 10)[0]
    crc16_calc = crc16(frame[:10])
    if crc16_recv != crc16_calc:
        print(f"❌ CRC16 mismatch: {crc16_recv:04X} vs {crc16_calc:04X}")
        return

    crc32_recv = struct.unpack_from("<I", frame, len(frame) - 4)[0]
    crc32_calc = crc32(frame[:-4])
    if crc32_recv != crc32_calc:
        print(f"❌ CRC32 mismatch: {crc32_recv:08X} vs {crc32_calc:08X}")
        return

    # Extract command set and ID
    cmd_set = frame[12]
    cmd_id = frame[13]
    payload = frame[14:-4]

    # print(f"📦 Frame parsed: cmd_set=0x{cmd_set:02X}, cmd_id=0x{cmd_id:02X}, payload={payload.hex()}")

    # Dispatch to handler
    dispatch_handler(cmd_set, cmd_id, payload)
