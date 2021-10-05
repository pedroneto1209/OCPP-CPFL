import asyncio
from asyncio.runners import run
from asyncio.windows_events import NULL
import keyboard
import websockets
from datetime import datetime

from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus, ResetStatus, ResetType
from ocpp.v16 import call_result, call

hb = 0
class ChargePoint(cp):
    @on(Action.BootNotification)
    def on_boot_notitication(self, **kwargs):
        print('\n\n')
        print('BOOT NOTIFICATION')
        print('charge_point_vendor = '+kwargs.get('charge_point_vendor'))
        print('charge_point_model = '+kwargs.get('charge_point_model'))
        print('\n\n')
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )

    @on(Action.StatusNotification)
    def on_status_notitication(self, **kwargs):
        print('\n\n')
        print('STATUS NOTIFICATION')
        print('status = '+kwargs.get('status'))
        print('connector_id = '+str(kwargs.get('connector_id')))
        print('error_code = '+str(kwargs.get('error_code')))
        print('\n\n')
        return call_result.StatusNotificationPayload(
        )

    @on(Action.Heartbeat)
    def on_heart_beat(self):
        global hb
        print('heartbeat ' + str(hb))
        hb += 1
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().isoformat(),
        )

    async def reset_send(self):
        request = call.ResetPayload(
            type=ResetType.hard
        )
        response = await self.call(request)
        if response.status == ResetStatus.accepted:
            print("Reset Started!!!")

chargepoint = NULL

async def on_connect(websocket, path):
    global chargepoint
    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)
    chargepoint = cp
    print('cp assigned')
    await cp.start()

async def scankey():
    global chargepoint
    while True:
        print('clock')
        if keyboard.is_pressed('q'):
            await chargepoint.reset_send()
        await asyncio.sleep(1)


async def main():
    server = await websockets.serve(
        on_connect,
        '192.168.0.242',
        9000,
        subprotocols=['ocpp1.6']
    )

    tasks = [asyncio.ensure_future(server.wait_closed()), asyncio.ensure_future(scankey())]
    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())