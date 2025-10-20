import asyncio
from bleak import BleakClient, BleakScanner

# BLE UUIDs for DJI Osmo Action 5
SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
WRITE_CHAR_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"
NOTIFY_CHAR_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"

# Step 1: Pairing initiation payload
PAIRING_INIT = bytes.fromhex("0a080000000000000000000000000000")

# Step 2: Follow-up payload template (will be filled with token)
def pairing_response(token: bytes):
    # Replace the last 16 bytes with the token
    return bytes.fromhex("0a080001") + token

# Store token received from notification
received_token = None

def notification_handler(sender, data):
    global received_token
    print(f"Notification from {sender}: {data.hex()}")
    if len(data) == 16:
        received_token = data

async def main():
    print("Scanning for OsmoAction5Pro...")
    devices = await BleakScanner.discover()
    target = next((d for d in devices if "OsmoAction5Pro" in d.name), None)

    if not target:
        print("Camera not found.")
        return

    print(f"Connecting to {target.name} ({target.address})...")
    async with BleakClient(target.address) as client:
        print("Connected!")

        # Step 1: Start notifications
        await client.start_notify(NOTIFY_CHAR_UUID, notification_handler)

        # Step 2: Send pairing initiation
        await client.write_gatt_char(WRITE_CHAR_UUID, PAIRING_INIT)
        print("Sent pairing initiation")

        # Step 3: Wait for token
        for _ in range(10):
            await asyncio.sleep(1)
            if received_token:
                break

        if not received_token:
            print("No token received — pairing failed.")
            await client.stop_notify(NOTIFY_CHAR_UUID)
            return

        print(f"Received token: {received_token.hex()}")

        # Step 4: Send pairing response with token
        response_payload = pairing_response(received_token)
        await client.write_gatt_char(WRITE_CHAR_UUID, response_payload)
        print("Sent pairing response")

        await asyncio.sleep(2)
        await client.stop_notify(NOTIFY_CHAR_UUID)

asyncio.run(main())
