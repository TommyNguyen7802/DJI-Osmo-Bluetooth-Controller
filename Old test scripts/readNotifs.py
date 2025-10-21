import asyncio
from bleak import BleakClient, BleakScanner

CHAR_UUID = "0000fff4-0000-1000-8000-00805f9b34fb"
last_payload = None

def parse_dji_notification(data: bytes):
    if len(data) != 47:
        return {"error": "Invalid payload length"}

    return {
        "header": data[0:6].hex(),
        "sequence": data[6],
        "mode_flags": data[7:11].hex(),
        "camera_mode": data[11],
        "sub_mode": data[12],
        "status_code": data[13:15].hex(),
        "battery_raw": int.from_bytes(data[15:17], "little"),
        "temp_raw": int.from_bytes(data[17:19], "little"),
        "flags": data[19:23].hex(),
        "reserved_1": data[23:33].hex(),
        "session_id": data[33:37].hex(),
        "reserved_2": data[37:47].hex(),
    }

def notification_handler(sender, data):
    global last_payload
    parsed = parse_dji_notification(data)
    if "error" in parsed:
        print(f"❌ {parsed['error']}")
        return

    print(f"\n🔔 Notification from {sender} (len={len(data)}):")
    for k, v in parsed.items():
        print(f"{k:15}: {v}")

    # Optional: compare with last payload
    if last_payload:
        diffs = {k: (last_payload[k], v) for k, v in parsed.items() if last_payload[k] != v}
        if diffs:
            print("🧪 Changes since last:")
            for k, (old, new) in diffs.items():
                print(f"  {k}: {old} → {new}")
    last_payload = parsed

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

        await client.start_notify(CHAR_UUID, notification_handler)
        print("📨 Live logging started — press Ctrl+C to stop")

        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping logger...")
            await client.stop_notify(CHAR_UUID)

asyncio.run(main())
