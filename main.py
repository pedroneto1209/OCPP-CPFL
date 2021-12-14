import asyncio
from asyncio.windows_events import NULL
import websockets

from chargepoint import ChargePoint
from controller import scankey

class Connector:    
    def __init__(self):
        self.chargepoint = NULL

    async def on_connect(self, websocket, path):
        self.chargepoint
        charge_point_id = path.strip('/')
        cp = ChargePoint(charge_point_id, websocket)
        self.chargepoint = cp
        print('cp assigned')
        await cp.start()


async def main():
    connector = Connector()
    server = await websockets.serve(
        connector.on_connect,
        '192.168.0.242',
        9000,
        subprotocols=['ocpp1.6']
    )

    tasks = [asyncio.ensure_future(server.wait_closed()), asyncio.ensure_future(scankey(connector.chargepoint))]
    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())