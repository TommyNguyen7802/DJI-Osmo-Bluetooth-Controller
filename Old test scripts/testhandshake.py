import asyncio
from bleak import BleakClient, BleakScanner
from enum import Enum

# BLE UUIDs (adjust if needed)
WRITE_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"
NOTIFY_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"

# Wake payload
wake_payload = bytes([0xFC, 0xEF, 0xFE, 0x86, 0x00, 0x00])


# Connection states
class ConnectState(Enum):
    BLE_NOT_INIT = 0
    BLE_INIT_COMPLETE = 1
    BLE_SEARCHING = 2
    BLE_CONNECTED = 3
    PROTOCOL_CONNECTED = 4
    BLE_DISCONNECTING = 5

connect_state = ConnectState.BLE_NOT_INIT
camera_response = None

# Notification handler
def notification_handler(sender, data):
    global camera_response
    print(f"🔔 Notification from {sender}: {data.hex()} (len={len(data)})")
    camera_response = data

# Build connection request frame
def build_dji_framed_connection_request(device_id, mac_addr, fw_version, verify_mode, verify_data):
    # DJI-style header
    header = bytes([0xFC, 0xEF, 0xFE, 0x86])

    # Original payload
    payload = bytearray()
    payload += device_id.to_bytes(4, "little")
    payload += len(mac_addr).to_bytes(1, "little")
    payload += bytes(mac_addr)
    payload += fw_version.to_bytes(4, "little")
    payload += verify_mode.to_bytes(1, "little")
    payload += verify_data.to_bytes(2, "little")

    return header + payload

def build_dji_command_frame(cmd_id, payload):
    header = bytes([0xFC, 0xEF, 0xFE, 0x86])
    length = len(payload).to_bytes(2, "little")
    return header + bytes([cmd_id]) + length + payload

# Parse camera command frame
def parse_camera_command(data):
    verify_mode = data[9]
    verify_data = int.from_bytes(data[10:12], "little")
    return verify_mode, verify_data

# Build connection response frame
def build_connection_response(device_id, camera_reserved):
    payload = bytearray()
    payload += device_id.to_bytes(4, "little")
    payload += (0).to_bytes(2, "little")  # ret_code = 0
    payload += bytes([camera_reserved]) + bytes(15)
    return payload

# Main connection flow
async def connect_to_dji_camera():
    global connect_state, camera_response
    connect_state = ConnectState.BLE_SEARCHING

    print("🔍 Scanning for OsmoAction5Pro...")
    devices = await BleakScanner.discover()
    target = next((d for d in devices if "OsmoAction5Pro" in d.name), None)
    if not target:
        print("❌ Camera not found.")
        return
    print(f"Connecting to {target.name} ({target.address})...")
    async with BleakClient(target.address) as client:
        print("✅ BLE connected")
        connect_state = ConnectState.BLE_CONNECTED
        

        await client.start_notify(NOTIFY_UUID, notification_handler)

        # Build and send connection request
        device_id = 0x12345678
        mac_addr = [0x04, 0xA8, 0x5A, 0x67, 0x90, 0x7B]  # Example MAC
        fw_version = 0x01020304
        #verify_mode = 1  # Pairing
        #verify_data = 0xABCD
        verify_mode = 1  # Pairing
        verify_data = 0x0000

        await client.write_gatt_char("0000fff4-0000-1000-8000-00805f9b34fb", wake_payload)
        print("📡 Wake payload sent")
        for _ in range(30):
            await asyncio.sleep(1)
            if camera_response:
                break


        raw_payload = build_dji_framed_connection_request(device_id, mac_addr, fw_version, verify_mode, verify_data)
        framed_payload = build_dji_command_frame(cmd_id=0x19, payload=raw_payload)
        await client.write_gatt_char("0000fff4-0000-1000-8000-00805f9b34fb", framed_payload)

        print("📨 Sent DJI-framed connection request")

        # Wait for camera response
        for _ in range(30):
            await asyncio.sleep(1)
            if camera_response:
                break

        if not camera_response:
            print("⚠️ No response from camera")
            return

        # Parse and respond
        verify_mode, verify_data = parse_camera_command(camera_response)
        if verify_mode == 2 and verify_data == 0:
            response_payload = build_connection_response(device_id, camera_reserved=0x01)
            await client.write_gatt_char(WRITE_UUID, response_payload)
            connect_state = ConnectState.PROTOCOL_CONNECTED
            print("✅ Protocol handshake complete")
        else:
            print(f"❌ Unexpected verify_mode={verify_mode}, verify_data={verify_data}")

        await client.stop_notify(NOTIFY_UUID)

asyncio.run(connect_to_dji_camera())
