import asyncio
from dji_ble import DJIBLE
from dji_commands import build_connection_request, build_record_command
from dji_protocol import build_frame, next_seq
from dji_structs import (
    build_camera_mode_switch,
    build_power_mode_switch,
    build_key_report_qs
)
#remove
import struct

# debugging
def parse_ret_code(payload: bytes) -> int | None:
    return payload[0] if payload else None



async def main():


    ble = DJIBLE()
    await ble.connect()



    # # debugging
    # async def wait_ret_code(cmd_set, cmd_id, timeout=2.0):
    #     # implement using your BLE read/queue; example skeleton:
    #     start = asyncio.get_event_loop().time()
    #     while asyncio.get_event_loop().time() - start < timeout:
    #         ref = await ble.read()  # your method that returns a parsed frame
    #         # make sure you parse SOF, CRCs, and extract cmd_set, cmd_id, payload
    #         if ref.cmd_set == cmd_set and ref.cmd_id == cmd_id:
    #             return ref.payload[0] if ref.payload else None
    #     return None


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

    await asyncio.sleep(1)

    #########################################################################
    # 1) stop recording
    payload = build_record_command(device_id, start=False)
    frame = build_frame(0x1D, 0x03, 0x02, payload, next_seq())  # mirror C: response-or-not
    await ble.write(frame)
    await asyncio.sleep(1.0)

    # 2) switch to plain video
    payload = build_camera_mode_switch(device_id, 0x01)
    frame = build_frame(0x1D, 0x04, 0x02, payload, next_seq())
    await ble.write(frame)
    await asyncio.sleep(1.0)

    # 3) send QS key report to 0x00/0x11 (not 0x02)
    payload = build_key_report_qs()              # (0x02, 0x01, 0x0000)
    frame = build_frame(0x00, 0x11, 0x02, payload, next_seq())
    await ble.write(frame)
    await asyncio.sleep(0.1)

    # 4) sleep (need-ack cmd_type)
    payload = struct.pack("<B 3x", 0x03)         # try padded; if no luck, try "<B" or "<H"
    frame = build_frame(0x00, 0x1A, 0x02, payload, next_seq())
    await ble.write(frame)

    #########################################################################

    # # make sure we are idle
    # payload = build_record_command(device_id, start=False)  # stop if recording
    # frame = build_frame(0x1D, 0x03, 0x00, payload, next_seq())
    # await ble.write(frame)

    # await asyncio.sleep(0.5)

    # # Switch to video mode
    # payload = build_camera_mode_switch(device_id, 0x01)
    # frame = build_frame(0x1D, 0x04, 0x00, payload, next_seq())
    # await ble.write(frame)

    # await asyncio.sleep(0.5)

    # # key report (QS)
    # payload = build_key_report_qs()  # 0x02, 0x01, 0x0000
    # frame = build_frame(0x00, 0x02, 0x00, payload, next_seq())
    # await ble.write(frame)

    # await asyncio.sleep(0.05)

    # Sleep Camera
    # # payload = build_power_mode_switch(device_id, sleep=True)
    # payload = struct.pack("<B 3x", 0x03)
    # frame = build_frame(0x00, 0x1A, 0x00, payload, next_seq())
    # ret = parse_ret_code(payload)
    # print(f"Power switch ret_code=0x{ret:02X}")
    # await ble.write(frame)

    # await asyncio.sleep(1)

    # payload = struct.pack("<B 3x", 0x03)
    # frame = build_frame(0x00, 0x1A, 0x00, payload, next_seq())
    # ret = parse_ret_code(payload)
    # print(f"Power switch ret_code=0x{ret:02X}")
    # await ble.write(frame)

    # Switch Camera to Photo Mode
    payload = build_camera_mode_switch(device_id, 0x05)
    frame = build_frame(0x1D, 0x04, 0x00, payload, next_seq())
    await ble.write(frame)

    await asyncio.sleep(2)

    # Take Photo
    payload = build_record_command(device_id, start=True)
    frame = build_frame(0x1D, 0x03, 0x00, payload, next_seq())
    await ble.write(frame)

    await asyncio.sleep(1)

    await ble.disconnect()


asyncio.run(main())
