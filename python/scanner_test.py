import asyncio
from bleak import BleakScanner

async def main():
    stop_event = asyncio.Event()

    def callback(device, advertising_data):
        print(device, advertising_data)

    async with BleakScanner(callback) as scanner:
        # Important! Wait for an event to trigger stop, otherwise scanner
        # will stop immediately.
        await stop_event.wait()

asyncio.run(main())