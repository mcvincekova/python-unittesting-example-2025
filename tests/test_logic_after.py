from unittest import TestCase
from unittest.mock import MagicMock
from uuid import UUID

from parameterized import parameterized

from logic_after import Device, DeviceType, DeviceStatus, DeviceUserInfo


class TestDevice(TestCase):
    
    def setUp(self) -> None:
        pass

    def test_device_creation_status_set_to_initial(self):
        # Arrange
        mock_user_info = MagicMock()
        mock_uuid = MagicMock()
        expected_status = DeviceStatus.INITIAL.value
        # Act
        device = Device(
            device_id=mock_uuid,
            device_type=DeviceType.PC,
            user_info=mock_user_info()
        )
        # Assert
        self.assertEqual(expected_status, device.get_status())

    # ---
    # Notes:
    # Notice how we are using MagicMock to mock the DeviceUserInfo and UUID objects. We did it because in this test
    # we don't really care about the actual values/behaviour of the user_info and device_id,
    # we just want to test the Device status.
    # Creating these mocks was also very easy and saved a bit of time compared to creating the actual objects.
    # Using real object instances would be still OK though. This is the same for a few tests that follow.
    # ---

    @parameterized.expand([
        (DeviceStatus.INITIAL.value,),
        (DeviceStatus.ACTIVE.value,),
        (DeviceStatus.INACTIVE.value,),
        (DeviceStatus.UNKNOWN.value,)
    ])
    def test_set_status_valid_assigned(self, expected_status):
        # Arrange
        mock_user_info = MagicMock()
        mock_uuid = MagicMock()
        device = Device(
            device_id=mock_uuid,
            device_type=DeviceType.PC,
            user_info=mock_user_info
        )
        # Act
        device.set_status(expected_status)
        # Assert
        self.assertEqual(expected_status, device.get_status())

    # ---
    # Notes:
    # Notice two things:
    # 1. We found and fixed a BUG in the helper method `Device._is_device_status_valid()` used by the `Device.set_status()`.
    #    This was possible because we tested the specification of the `Device.set_status()` method, and used all possible
    #    valid DeviceStatus values in the test.
    # 2. We used the `parameterized` decorator to create a parametrized test - this is a more concise way to test multiple
    #    inputs for a single test method. Each parameterised test will be run as a separate unit test - thus the
    #    `test_set_status_valid_assigned` test method will run 4 times, once for each parameter.
    # ---


    def test_set_status_invalid_raises_error(self):
        # Arrange
        mock_user_info = MagicMock()
        mock_uuid = MagicMock()
        device = Device(
            device_id=mock_uuid,
            device_type=DeviceType.PC,
            user_info=mock_user_info
        )
        invalid_status = 'SOME INVALID STATUS'

        # Act & Assert
        with self.assertRaises(ValueError, msg=f'Invalid status: {invalid_status}'):
            device.set_status(invalid_status)


    def test_to_dict(self):
        # Arrange
        device_id = UUID('bcde2b57-1e4d-42cc-95bf-e674014b3426')
        user_id = UUID('acde2b57-1e4d-42cc-95bf-e674014b3426')
        expected_dict = {
            'id': device_id,
            'status': 'PENDING ACTIVATION',
            'type': 'IPHONE',
            'user_info': {
                'email': 'johndoe@gmail.com',
                'id': user_id,
                'name': 'John Doe'
            }
        }
        user_info = DeviceUserInfo(
            user_id=user_id,
            name='John Doe',
            email='johndoe@gmail.com'
        )

        device = Device(
            device_id=device_id,
            device_type=DeviceType.PHONE,
            user_info=user_info
        )

        # Act
        actual_dict = device.to_dict()

        # Assert
        self.assertDictEqual(expected_dict, actual_dict)

    # ---
    # Notes
    # Notice how we are testing the `Device.to_dict()` method, instead of the private methods suc has
    # `Device._get_device_user_id()`.
    # Moreover, once we have written a test for the `Device.to_dict()` method, we could have 'safely' refactored it
    # by directly accessing `Device` params instead of using private helper methods that only accessed the params
    # (and offered no extra logic)
    # ---