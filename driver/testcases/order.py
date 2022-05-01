from .utils import *
from datetime import timedelta
from django.utils import timezone
from driver.models import Driver
from passenger.models import Passenger
from order.models import Order


class DriverOrderTests(TestCase):
    def setUp(self):
        Driver.objects.create(
            id=1,
            username='driver1',
            age=30,
            identification_no='012345678987654321',
            phone='0123456789',
            carplate='京01234'
        )
        access_token, refresh_token, status_code = auth_driver(self,
                                                               'superuser1')
        Passenger.objects.create(
            id=2,
            username='passenger1',
            age=30,
            identification_no='012345678987654321',
            phone='0123456743'
        )
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

    def test_queue_order(self):
        access_token, refresh_token, status_code = auth_driver(self,
                                                               'superuser1')
        self.assertEqual(status_code, 200)
        response = self.client.get(
            '/api/driver/info',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_update_location_no_order(self):
        access_token, refresh_token, status_code = auth_driver(self,
                                                               'superuser1')
        self.assertEqual(status_code, 200)
        response = self.client.get(
            '/api/driver/info',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

        payload = {
            "latitude": 39.99970025463180,
            "longitude": 116.32636879642432
        }
        response = self.client.post(
            '/api/driver/order/update-location',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {})

    def test_update_location_with_order(self):
        # Driver being online
        access_token, refresh_token, status_code = auth_driver(self,
                                                               'superuser1')
        self.assertEqual(status_code, 200)

        payload = {
            "latitude": '39.9136172322172',
            "longitude": '116.39729231302886'
        }
        response = self.client.post(
            '/api/driver/order/update-location',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

        # Passenger creates a new order
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

        payload = {
            "latitude": 39.99970025463180,
            "longitude": 116.32636879642432
        }
        response = self.client.post(
            '/api/passenger/order/update-location',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

        payload = {
            "start": {
                "name": "清华大学",
                "address": "北京市海淀区双清路30号",
                "latitude": "39.99970025463166",
                "longitude": "116.32636879642432"
            },
            "end": {
                "name": "故宫博物院",
                "address": "中国北京市东城区景山前街4号",
                "latitude": "39.9136172322172",
                "longitude": "116.39729231302886",
            }
        }
        response = self.client.post(
            '/api/passenger/order/new',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

        # Driver updates location again
        access_token, refresh_token, status_code = auth_driver(self,
                                                               'superuser1')
        self.assertEqual(status_code, 200)

        payload = {
            "latitude": '39.9136172322172',
            "longitude": '116.39729231302886'
        }
        response = self.client.post(
            '/api/driver/order/update-location',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            "latitude": 39.99970025463180,
            "longitude": 116.32636879642432
        })
