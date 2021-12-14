from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call_result, call
from ocpp.v16.enums import Action, RegistrationStatus, ResetStatus, ResetType
from ocpp.routing import on

from datetime import datetime

hb = 0

class ChargePoint(cp):

###----------------------------Receive----------------------------###

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

###----------------------------Send----------------------------###

    async def reset_send(self):
        request = call.ResetPayload(
            type=ResetType.hard
        )
        response = await self.call(request)
        if response.status == ResetStatus.accepted:
            print("Reset Started!!!")