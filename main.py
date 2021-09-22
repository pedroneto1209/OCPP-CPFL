import asyncio
import websockets
from datetime import datetime

from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import Action, RegistrationStatus
from ocpp.v16 import call_result

class ChargePoint(cp):
    @on(Action.BootNotification)
    def on_boot_notitication(self, charge_point_vendor, charge_point_model, **kwargs):
        print(charge_point_vendor)
        print('bn')
        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )

    @on(Action.StatusNotification)
    def on_status_notitication(self, status, connector_id, **params):
        print(status)
        print(connector_id)
        return call_result.StatusNotificationPayload(
        )

    @on(Action.Heartbeat)
    def on_heart_beat(self):
        print('heartbeat')
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().isoformat(),
        )


async def on_connect(websocket, path):
    charge_point_id = path.strip('/')
    cp = ChargePoint(charge_point_id, websocket)

    await cp.start()


async def main():
    server = await websockets.serve(
        on_connect,
        '192.168.0.242',
        9000,
        subprotocols=['ocpp1.6']
    )

    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())