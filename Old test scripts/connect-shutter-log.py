import asyncio
from bleak import BleakClient, BleakScanner

# Candidate write characteristics
WRITE_CANDIDATES = [
    "0000fff3-0000-1000-8000-00805f9b34fb",
    "0000fff4-0000-1000-8000-00805f9b34fb",
    "0000fff5-0000-1000-8000-00805f9b34fb"
]

# Notification characteristic (confirmed active)
NOTIFY_CHAR_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"

# Shutter command payload
SHUTTER_CMD = bytes.fromhex("0a080100000000000000000000000000")

# Store notifications per write attempt
notifications_by_write = {}

def notification_handler(sender, data):
    hex_data = data.hex()
    print(f"🔔 Notification from {sender}: {hex_data} (len={len(data)})")
    notifications_by_write.setdefault(sender, []).append(hex_data)

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
        await client.start_notify(NOTIFY_CHAR_UUID, notification_handler)
        print("📨 Listening for notifications...")

        # Wait for baseline notifications
        await asyncio.sleep(3)

        # Try writing to each candidate characteristic
        for write_uuid in WRITE_CANDIDATES:
            print(f"\n🧪 Testing write to {write_uuid}...")
            try:
                await client.write_gatt_char(write_uuid, SHUTTER_CMD)
                print("📸 Shutter command sent")
            except Exception as e:
                print(f"❌ Write to {write_uuid} failed: {e}")

            # Wait for post-write notifications
            await asyncio.sleep(3)

        await client.stop_notify(NOTIFY_CHAR_UUID)
        print("\n✅ Test complete")

        # Summary
        print("\n🔍 Notification summary:")
        for sender, notes in notifications_by_write.items():
            print(f"\nFrom {sender}:")
            for i, note in enumerate(notes):
                print(f"  [{i}] {note}")

asyncio.run(main())