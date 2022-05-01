from datetime import timedelta
from django.utils import timezone
from order.models import Order
from passenger.models import Passenger
from passenger.testcases.utils import *


class PassengerEstimatePriceTest(TestCase):
    def setUp(self):
        Passenger.objects.create(
            id=1,
            username='username1',
            age=30,
            identification_no='012345678987654321',
            phone='0123456789'
        )

    def test_valid_est_price(self):
        # valid request
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

        payload = {
            'start': {
                'name': '清华大学',
                'address': '北京市海淀区双清路30号',
                'latitude': '39.99970025463166',
                'longitude': '116.32636879642432',
            },
            'end': {
                'name': '故宫博物院',
                'address': '中国北京市东城区景山前街4号',
                'latitude': '39.9136172322172',
                'longitude': '116.39729231302886'
            }
        }
        response = self.client.post(
            '/api/passenger/order/est-price',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_valid_est_price_reverse_geocoding(self):
        # valid request
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

        payload = {
            'start': {
                'name': '',
                'address': '',
                'latitude': '39.99970025463166',
                'longitude': '116.32636879642432',
            },
            'end': {
                'name': '',
                'address': '',
                'latitude': '39.9136172322172',
                'longitude': '116.39729231302886'
            }
        }
        response = self.client.post(
            '/api/passenger/order/est-price',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_est_price(self):
        # not authenticated
        payload = {
            'start': {
                'name': '清华大学',
                'address': '北京市海淀区双清路30号',
                'latitude': '39.99970025463166',
                'longitude': '116.32636879642432',
            },
            'end': {
                'name': '故宫博物院',
                'address': '中国北京市东城区景山前街4号',
                'latitude': '39.9136172322172',
                'longitude': '116.39729231302886'
            }
        }
        response = self.client.post(
            '/api/passenger/order/est-price',
            data=payload,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)

        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

        # invalid method
        response = self.client.get(
            '/api/passenger/order/est-price',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 405)


class PassengerOrderTests(TestCase):
    def setUp(self):
        Passenger.objects.create(
            id=1,
            username='username1',
            age=30,
            identification_no='012345678987654321',
            phone='0123456789'
        )
        for x in range(0, 100):
            Order.objects.create(
                passenger=Passenger.objects.get(id=1),
                start_POI_name=f"清华大学{x}",
                start_POI_address="北京市海淀区双清路30号",
                start_POI_lat=39.99970025463166,
                start_POI_long=116.32636879642432,
                end_POI_name="故宫博物院",
                end_POI_address="中国北京市东城区景山前街4号",
                end_POI_lat=39.9136172322172,
                end_POI_long=116.39729231302886,
                est_price=100,
                status=6,
                updated_at=timezone.now() - timedelta(minutes=5)
            )

    def test_create_order(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

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

    def test_create_order_reverse_geocoding(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

        payload = {
            "start": {
                "name": "",
                "address": "",
                "latitude": "39.99970025463166",
                "longitude": "116.32636879642432"
            },
            "end": {
                "name": "",
                "address": "",
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

    def test_active_order_exists(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

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

        # Adds another order when an order exists
        response = self.client.post(
            '/api/passenger/order/new',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 400)

    def test_get_order(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

        # No active order
        response = self.client.get(
            '/api/passenger/order/get',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, None)

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

        # Add a new order
        response = self.client.post(
            '/api/passenger/order/new',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

        # Check for the current order
        response = self.client.get(
            '/api/passenger/order/get',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_current_order(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

        response = self.client.get(
            '/api/passenger/order/current',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], -1)

        # Add a new order
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

        response = self.client.get(
            '/api/passenger/order/current',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.data['status'], 0)

    def test_cancel_order(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

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

        # Add a new order
        response = self.client.post(
            '/api/passenger/order/new',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

        # Cancel the order
        response = self.client.post(
            '/api/passenger/order/cancel',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {})

        # Check for the current order
        response = self.client.get(
            '/api/passenger/order/current',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_cancel_order(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

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
        Order.objects.create(
            passenger=Passenger.objects.get(id=1),
            start_POI_name=payload['start']['name'],
            start_POI_address=payload['start']['address'],
            start_POI_lat=float(payload['start']['latitude']),
            start_POI_long=float(payload['start']['longitude']),
            end_POI_name=payload['end']['name'],
            end_POI_address=payload['end']['address'],
            end_POI_lat=float(payload['end']['latitude']),
            end_POI_long=float(payload['end']['longitude']),
            est_price=100,
            updated_at=timezone.now(),
            status=2
        )
        response = self.client.post(
            '/api/passenger/order/cancel',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['errMsg'], '当前阶段不允许取消订单。')

    def test_pay_order(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

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
        Order.objects.create(
            passenger=Passenger.objects.get(id=1),
            start_POI_name=payload['start']['name'],
            start_POI_address=payload['start']['address'],
            start_POI_lat=float(payload['start']['latitude']),
            start_POI_long=float(payload['start']['longitude']),
            end_POI_name=payload['end']['name'],
            end_POI_address=payload['end']['address'],
            end_POI_lat=float(payload['end']['latitude']),
            end_POI_long=float(payload['end']['longitude']),
            est_price=100,
            updated_at=timezone.now(),
            status=5
        )
        response = self.client.post(
            '/api/passenger/order/paid',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            '/api/passenger/order/current',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.data['status'], -1)

    def test_invalid_pay_order(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

        response = self.client.post(
            '/api/passenger/order/paid',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {})

    def test_update_location(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

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

        # Add a new order
        response = self.client.post(
            '/api/passenger/order/new',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

        # Update location
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

    def test_list_orders(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

        response = self.client.get(
            '/api/passenger/order/list?offset=10&limit=20',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

        for x in range(0, 10):
            self.assertEqual(
                response.data[x]['start']['name'],
                f'清华大学{89 - x}'
            )


class PassengerUnauthenticatedTests(TestCase):
    def setUp(self):
        pass

    def test_est_price(self):
        payload = {
            'start': {
                'name': '清华大学',
                'address': '北京市海淀区双清路30号',
                'latitude': '39.99970025463166',
                'longitude': '116.32636879642432',
            },
            'end': {
                'name': '故宫博物院',
                'address': '中国北京市东城区景山前街4号',
                'latitude': '39.9136172322172',
                'longitude': '116.39729231302886'
            }
        }
        response = self.client.post(
            '/api/passenger/order/est-price',
            data=payload,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)

    def test_create_order(self):
        payload = {
            'start': {
                'name': '清华大学',
                'address': '北京市海淀区双清路30号',
                'latitude': '39.99970025463166',
                'longitude': '116.32636879642432',
            },
            'end': {
                'name': '故宫博物院',
                'address': '中国北京市东城区景山前街4号',
                'latitude': '39.9136172322172',
                'longitude': '116.39729231302886'
            }
        }
        response = self.client.post(
            '/api/passenger/order/new',
            data=payload,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)

    def test_get_order(self):
        response = self.client.get(
            '/api/passenger/order/get',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)

    def test_current_order(self):
        response = self.client.get(
            '/api/passenger/order/current',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)

    def test_cancel_order(self):
        response = self.client.post(
            '/api/passenger/order/cancel',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)

    def test_pay_order(self):
        response = self.client.post(
            '/api/passenger/order/paid',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)

    def test_update_location(self):
        response = self.client.post(
            '/api/passenger/order/update-location',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)

    def test_list_orders(self):
        response = self.client.get(
            '/api/passenger/order/list',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)


class PassengerUnregisteredTests(TestCase):
    def setUp(self):
        Passenger.objects.create(id=1)
        access_token, refresh_token, status_code = auth_driver(self,
                                                               'superuser1')

    def test_est_price(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

        payload = {
            'start': {
                'name': '清华大学',
                'address': '北京市海淀区双清路30号',
                'latitude': '39.99970025463166',
                'longitude': '116.32636879642432',
            },
            'end': {
                'name': '故宫博物院',
                'address': '中国北京市东城区景山前街4号',
                'latitude': '39.9136172322172',
                'longitude': '116.39729231302886'
            }
        }
        response = self.client.post(
            '/api/passenger/order/est-price',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.data['errMsg'], '请填写个人资料。')

    def test_create_order(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

        payload = {
            'start': {
                'name': '清华大学',
                'address': '北京市海淀区双清路30号',
                'latitude': '39.99970025463166',
                'longitude': '116.32636879642432',
            },
            'end': {
                'name': '故宫博物院',
                'address': '中国北京市东城区景山前街4号',
                'latitude': '39.9136172322172',
                'longitude': '116.39729231302886'
            }
        }
        response = self.client.post(
            '/api/passenger/order/new',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.data['errMsg'], '请填写个人资料。')

    def test_get_order(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

        response = self.client.get(
            '/api/passenger/order/get',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.data['errMsg'], '请填写个人资料。')

    def test_current_order(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

        response = self.client.get(
            '/api/passenger/order/current',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.data['errMsg'], '请填写个人资料。')

    def test_cancel_order(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

        response = self.client.post(
            '/api/passenger/order/cancel',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.data['errMsg'], '请填写个人资料。')

    def test_pay_order(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

        response = self.client.post(
            '/api/passenger/order/paid',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.data['errMsg'], '请填写个人资料。')

    def test_update_location(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

        payload = {
            "latitude": 39.99970025463180,
            "longitude": 116.32636879642432
        }
        response = self.client.post(
            '/api/passenger/order/paid',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.data['errMsg'], '请填写个人资料。')

    def test_list_orders(self):
        access_token, refresh_token, status_code = auth_passenger(self,
                                                                  'superuser0')
        self.assertEqual(status_code, 200)

        response = self.client.get(
            '/api/passenger/order/list',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 402)
        self.assertEqual(response.data['errMsg'], '请填写个人资料。')
