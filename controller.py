import asyncio
import keyboard

async def controller(chargepoint):
    while True:
        print('clock')
        if keyboard.is_pressed('q'):
            await chargepoint.reset_send()
        await asyncio.sleep(1)