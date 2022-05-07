from datetime import timedelta
from django.utils import timezone
from driver.models import Driver
from driver.testcases.utils import *


class PassengerEstimatePriceTest(TestCase):
    def setUp(self):
        Driver.objects.create(
            id=1,
            username='driver1',
            age=30,
            identification_no='012345678987654321',
            phone='0123456789',
            carplate='京01234'
        )
        auth_driver(self, 'superuser0')

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

    def test_list_messages(self):
        access_token, refresh_token, status_code = auth_driver(self,
                                                               'superuser0')
        self.assertEqual(status_code, 200)

        payload = {
            'title': 'Test message title',
            'description': 'This is a description of this test message',
            'value': 'some value',
            'color': 'purple'
        }

        for i in range(0, 100):
            response = self.client.post(
                '/api/driver/msg',
                data=payload,
                content_type='application/json',
                **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
            )
            self.assertEqual(response.status_code, 200)

        response = self.client.get(
            '/api/driver/msg',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 100)

    def test_clear_messages(self):
        access_token, refresh_token, status_code = auth_driver(self,
                                                               'superuser0')
        self.assertEqual(status_code, 200)

        payload = {
            'title': 'Test message title',
            'description': 'This is a description of this test message',
            'value': 'some value',
            'color': 'purple'
        }

        for i in range(0, 100):
            response = self.client.post(
                '/api/driver/msg',
                data=payload,
                content_type='application/json',
                **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
            )
            self.assertEqual(response.status_code, 200)

        response = self.client.get(
            '/api/driver/msg',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 100)

        response = self.client.post(
            '/api/driver/msg/clear',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            '/api/driver/msg',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_unauthenticated(self):
        response = self.client.get(
            '/api/driver/msg',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)

    def test_unregistered(self):
        access_token, refresh_token, status_code = auth_driver(self,
                                                               'superuser1')
        self.assertEqual(status_code, 200)
        response = self.client.get(
            '/api/driver/msg',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 402)
