from unittest import TestCase
from uuid import UUID
from unittest.mock import MagicMock

from logic_before import Device, DeviceType, DeviceStatus, DeviceUserInfo


class TestDevice(TestCase):
    
    def setUp(self) -> None:
        pass

    def test_device_creation_status(self):
        # Arrange
        user_info = DeviceUserInfo(
            user_id=UUID('acde2b57-1e4d-42cc-95bf-e674014b3426'),
            name='John Doe',
            email='johndoe@gmail.com'
        )
        expected_status = DeviceStatus.INITIAL.value
        # Act
        device = Device(
            device_id=UUID('bcde2b57-1e4d-42cc-95bf-e674014b3426'),
            device_type=DeviceType.PC,
            user_info=user_info
        )
        # Assert
        self.assertEqual(expected_status, device.get_status())


    def test_set_status_valid_assigned(self):
        # Arrange
        user_info = DeviceUserInfo(
            user_id=UUID('acde2b57-1e4d-42cc-95bf-e674014b3426'),
            name='John Doe',
            email='johndoe@gmail.com'
        )
        device = Device(
            device_id=UUID('bcde2b57-1e4d-42cc-95bf-e674014b3426'),
            device_type=DeviceType.PC,
            user_info=user_info
        )
        expected_statuses = ['PENDING ACTIVATION', 'ACTIVE', 'INACTIVE']

        for expected_status in expected_statuses:
            # Act
            device.set_status(expected_status)
            # Assert
            self.assertEqual(expected_status, device.get_status())

    # ---
    # Notes:
    # Notice how in this test we are mirroring the implementation of the `Device._is_device_status_valid()` method - by
    # using only the expected_statuses accepted by that method as valid;
    # instead of testing the specification of the `Device.set_status()` method.
    # This caused us to miss a BUG, since the `UNKNOWN` device status is now not recognized as a valid status,
    # but based on the docstring/specification of the `Device.set_status()` method, any DeviceStatus is valid.
    # ---

    def test_set_status_invalid_assigned(self):
        # Arrange
        user_info = DeviceUserInfo(
            user_id=UUID('acde2b57-1e4d-42cc-95bf-e674014b3426'),
            name='John Doe',
            email='johndoe@gmail.com'
        )
        device = Device(
            device_id=UUID('bcde2b57-1e4d-42cc-95bf-e674014b3426'),
            device_type=DeviceType.PC,
            user_info=user_info
        )
        invalid_status = 'SOME INVALID STATUS'

        # Act & Assert
        with self.assertRaises(ValueError, msg=f'Invalid status: {invalid_status}'):
            device.set_status(invalid_status)

    def test_user_device_info(self):
        # Arrange
        mock_user_info = MagicMock()
        mock_user_info.user_id = UUID('acde2b57-1e4d-42cc-95bf-e674014b3426')
        mock_user_info.name = 'John Doe'
        mock_user_info.email = 'john.doe@email.com'

        device = Device(
            device_id=UUID('bcde2b57-1e4d-42cc-95bf-e674014b3426'),
            device_type=DeviceType.PC,
            user_info=mock_user_info
        )

        # Act
        user_name = device._get_device_user_name()
        user_id = device._get_device_user_id()
        user_email = device._get_device_user_email()

        # Assert
        self.assertEqual(user_name, mock_user_info.name)
        self.assertEqual(user_id, mock_user_info.user_id)
        self.assertEqual(user_email, mock_user_info.email)

    # ---
    # Notes:
    # Notice how we are doing two unnecessary things here:
    # 1. We are testing three private methods that are not part of the public API of the `Device` class.
    #    We should never be testing private methods directly, but rather test the public methods that use them.
    # 2. We are mocking the `DeviceUserInfo` object, and while it's OK to mock it here
    #    it's not necessary, since it's a simple dataclass; and a real instance might be easier to work with.
    # ---
