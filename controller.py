import asyncio
import keyboard

async def scankey(chargepoint):
    while True:
        print('clock')
        if keyboard.is_pressed('q'):
            await chargepoint.reset_send()
        await asyncio.sleep(1)