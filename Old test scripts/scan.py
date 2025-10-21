import asyncio
from bleak import BleakScanner, BleakClient

async def scan_osmo_services():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    osmo = next((d for d in devices if "Osmo" in d.name), None)

    if not osmo:
        print("DJI Osmo Action 5 not found.")
        return

    print(f"Found: {osmo.name} @ {osmo.address}")

    async with BleakClient(osmo.address) as client:
        print("Connected. Fetching services...")
        services = await client.get_services()
        for service in services:
            print(f"\nService: {service.uuid}")
            for char in service.characteristics:
                props = ", ".join(char.properties)
                print(f"  └─ Characteristic: {char.uuid} [{props}]")

asyncio.run(scan_osmo_services())
