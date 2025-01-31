import pprint
from dataclasses import dataclass
from enum import Enum
from uuid import uuid4, UUID


class DeviceType(Enum):
    PC = 'MACBOOK'
    PHONE = 'IPHONE'
    TABLET = 'IPAD'
    WATCH = 'APPLE_WATCH'


class DeviceStatus(Enum):
    INITIAL = 'PENDING ACTIVATION'
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    UNKNOWN = 'UNKNOWN'


@dataclass
class DeviceUserInfo:
    user_id: UUID
    name: str
    email: str


class Device:
    
    def __init__(self, device_id: UUID, device_type: DeviceType, user_info: DeviceUserInfo) -> None:
        self.device_id = device_id
        self.device_type = device_type
        self.user_info = user_info
        self._status = DeviceStatus.INITIAL.value

    def get_status(self) -> str:
        """ Returns the current status of the device """
        return self._status

    def set_status(self, status: str) -> None:
        """ Sets one of the DeviceStatus values, otherwise raises ValueError """
        if not self._is_device_status_valid(status):
            raise ValueError(f'Invalid status: {status}')

        self._status = status

    def to_dict(self) -> dict:
        """ Returns a dictionary representation of the Device object """
        return {
            'id': self.device_id,
            'type': self.device_type.value,
            'status': self.get_status(),
            'user_info': {
                'id': self.user_info.user_id,
                'name': self.user_info.name,
                'email': self.user_info.email
            }
        }
    
    @staticmethod
    def _is_device_status_valid(status: str) -> bool:
        return status in [e.value for e in DeviceStatus]


def main():
    device_id = uuid4()
    user_id = uuid4()
    user_info = DeviceUserInfo(user_id=user_id, name='Kent Beck', email='kent.beck@email.com')
    device = Device(device_id=device_id, device_type=DeviceType.PC, user_info=user_info)

    pprint.pprint(device.to_dict())


if __name__ == '__main__':
    main()