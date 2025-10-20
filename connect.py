# Dependencies:
# pip install bleak
# sudo apt install bluetooth bluez


import asyncio
from bleak import BleakClient, BleakScanner

# UUIDs from your ESP32 code
SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID2 = "0000fff4-0000-1000-8000-00805f9b34fb" # Write characteristic
NOTIFY_CHAR_UUID = "0000fff4-0000-1000-8000-00805f9b34fb" # Notify characteristic

# Command payloads
def shutter_button():
    return bytes.fromhex("0a080100000000000000000000000000")



def screen_toggle(on=True):
    return bytes.fromhex("0a080200000000000000000000000000") if on else bytes.fromhex("0a080201000000000000000000000000")

def power_off():
    return bytes.fromhex("0a080300000000000000000000000000")

async def main():
    print("Scanning for OsmoAction5Pro camera...")
    devices = await BleakScanner.discover()
    target = None
    for d in devices:
        if "OsmoAction5Pro" in d.name:
            target = d
            break

    if not target:
        print("Camera not found.")
        return

    print(f"Connecting to {target.name} ({target.address})...")
    async with BleakClient(target.address) as client:
        print("Connected!")

        # Send shutter command
        await client.write_gatt_char(CHARACTERISTIC_UUID2, shutter_button())
        print("Shutter triggered")

        await asyncio.sleep(5)

        # Turn screen off
        await client.write_gatt_char(CHARACTERISTIC_UUID2, screen_toggle(on=False))
        print("Screen off")

        await asyncio.sleep(5)

        # Turn screen on
        await client.write_gatt_char(CHARACTERISTIC_UUID2, screen_toggle(on=True))
        print("Screen on")

        await asyncio.sleep(5)

        # Power off
        await client.write_gatt_char(CHARACTERISTIC_UUID2, power_off())
        print("Power off")

asyncio.run(main())
