from bleak import BleakClient, BleakScanner
from dji_protocol import parse_frame
class DJIBLE:
    def __init__(self, name="OsmoAction5Pro"):
        self.name = name
        self.client = None
        self.write_uuid = "0000fff3-0000-1000-8000-00805f9b34fb"
        self.notify_uuid = "0000fff4-0000-1000-8000-00805f9b34fb"

    async def connect(self):
        print("Scanning for OsmoAction5Pro camera...")
        devices = await BleakScanner.discover()
        target = next((d for d in devices if self.name in d.name), None)
        if not target:
            raise Exception("Camera not found")

        print(f"Connecting to {target.name} ({target.address})...")
        self.client = BleakClient(target.address)
        await self.client.connect()
        await self.client.start_notify(self.notify_uuid, self._notification_handler)
        print(f"Connected to {target.name}")

    async def disconnect(self):
        if self.client:
            await self.client.stop_notify(self.notify_uuid)
            await self.client.disconnect()
            print("Disconnected")

    async def write(self, data: bytes):
        await self.client.write_gatt_char(self.write_uuid, data)

    def _notification_handler(self, sender, data):
        from dji_protocol import handle_notification
        handle_notification(data)
        parse_frame(data)
