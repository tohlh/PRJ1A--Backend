from datetime import timedelta
from django.utils import timezone
from order.models import Order
from passenger.models import Passenger
from passenger.testcases.utils import *


class PassengerEstimatePriceTest(TestCase):
    def setUp(self):
        pass

    def test_add_message(self):
        access_token, refresh_token, status_code = auth_driver(self,
                                                               'superuser0')
        self.assertEqual(status_code, 200)

        payload = {
            'title': "Test message title",
            'description': 'This is a description of this test message',
            'value': 'some value',
            'color': 'purple'
        }

        response = self.client.post(
            '/api/driver/msg',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
