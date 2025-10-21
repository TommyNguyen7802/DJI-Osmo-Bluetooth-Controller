import asyncio
from dji_ble import DJIBLE
from dji_commands import build_connection_request, build_record_command
from dji_protocol import build_frame, next_seq

async def main():
    ble = DJIBLE()
    await ble.connect()

    # Send connection request
    device_id = 0x12345678
    mac = [0x04, 0xA8, 0x5A, 0x67, 0x90, 0x7B]
    fw_version = 0x01020304
    verify_mode = 0
    verify_data = 0x0000

    payload = build_connection_request(device_id, mac, fw_version, verify_mode, verify_data)
    frame = build_frame(0x00, 0x19, 0x00, payload, next_seq())
    await ble.write(frame)

    await asyncio.sleep(2)

    # Start recording
    payload = build_record_command(device_id, start=True)
    frame = build_frame(0x1D, 0x03, 0x00, payload, next_seq())
    await ble.write(frame)

    await asyncio.sleep(5)
    await ble.disconnect()

asyncio.run(main())
