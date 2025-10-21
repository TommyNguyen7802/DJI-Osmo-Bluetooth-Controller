import asyncio
from bleak import BleakClient, BleakScanner

# BLE UUIDs confirmed from your scan
CHAR_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"

# Pairing initiation payload
PAIRING_INIT = bytes.fromhex("0a080000000000000000000000000000")

# Follow-up pairing payload builder
def pairing_response(token: bytes):
    return bytes.fromhex("0a080001") + token

# Store token received from notification
received_token = None

def notification_handler(sender, data):
    global received_token
    print(f"🔔 Notification from {sender}: {data.hex()} (len={len(data)})")
    if len(data) == 16:
        received_token = data

async def main():
    print("🔍 Scanning for OsmoAction5Pro...")
    devices = await BleakScanner.discover()
    target = next((d for d in devices if "OsmoAction5Pro" in d.name), None)

    if not target:
        print("❌ Camera not found.")
        return

    print(f"📡 Connecting to {target.name} ({target.address})...")
    async with BleakClient(target.address) as client:
        print("✅ Connected!")

        # Start notifications
        await client.start_notify(CHAR_UUID, notification_handler)

        # Send pairing initiation
        await client.write_gatt_char(CHAR_UUID, PAIRING_INIT)
        print("📨 Sent pairing initiation")

        # Wait for token response
        for _ in range(10):
            await asyncio.sleep(1)
            if received_token:
                break

        if not received_token:
            print("⚠️ No token received — pairing may have failed.")
            await client.stop_notify(CHAR_UUID)
            return

        print(f"🔑 Received token: {received_token.hex()}")

        # Send pairing response
        response_payload = pairing_response(received_token)
        await client.write_gatt_char(CHAR_UUID, response_payload)
        print("📨 Sent pairing response")

        await asyncio.sleep(2)
        await client.stop_notify(CHAR_UUID)
        print("✅ Pairing sequence complete")

asyncio.run(main())
