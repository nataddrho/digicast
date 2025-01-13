import asyncio
from bleak import BleakScanner

async def main():
    stop_event = asyncio.Event()

    def callback(device, advertising_data):
        print(device, advertising_data)

    while(True):
        async with BleakScanner(callback) as scanner:           
            await asyncio.sleep(3)

asyncio.run(main())