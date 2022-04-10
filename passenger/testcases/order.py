from .utils import *
from order.models import Order


class PassengerEstimatePriceTest(TestCase):
    def setUp(self):
        pass

    def test_valid_est_price(self):
        # valid request
        access_token, refresh_token, status_code = authenticate(self)
        self.assertEqual(status_code, 200)

        payload = {
            'start_POI_lat': '39.99970025463166',
            'start_POI_long': '116.32636879642432',
            'end_POI_lat': '39.9136172322172',
            'end_POI_long': '116.39729231302886'
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
            'start_POI_lat': '39.99970025463166',
            'start_POI_long': '116.32636879642432',
            'end_POI_lat': '39.9136172322172',
            'end_POI_long': '116.39729231302886'
        }
        response = self.client.post(
            '/api/passenger/order/est-price',
            data=payload,
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)

        access_token, refresh_token, status_code = authenticate(self)
        self.assertEqual(status_code, 200)

        # invalid method
        response = self.client.get(
            '/api/passenger/order/est-price',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 405)

        # invalid payload
        payload = {
            'start_POI_lat': '39.99970025463166',
            'star_POI_long': '116.32636879642432',
        }
        response = self.client.post(
            '/api/passenger/order/est-price',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 400)


class PassengerCreateOrderTest(TestCase):
    def setUp(self):
        pass

    def test_create_order(self):
        access_token, refresh_token, status_code = authenticate(self)
        self.assertEqual(status_code, 200)

        payload = {
            "start_POI_name": "清华大学",
            "start_POI_address": "北京市海淀区双清路30号",
            "start_POI_lat": "39.99970025463166",
            "start_POI_long": "116.32636879642432",
            "end_POI_name": "故宫博物院",
            "end_POI_address": "中国北京市东城区景山前街4号",
            "end_POI_lat": "39.9136172322172",
            "end_POI_long": "116.39729231302886",
            "passenger_lat": "39.99970025463166",
            "passenger_long": "116.32636879642432"
        }
        response = self.client.post(
            '/api/passenger/order/new',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_current_order_exists(self):
        access_token, refresh_token, status_code = authenticate(self)
        self.assertEqual(status_code, 200)

        payload = {
            "start_POI_name": "清华大学",
            "start_POI_address": "北京市海淀区双清路30号",
            "start_POI_lat": "39.99970025463166",
            "start_POI_long": "116.32636879642432",
            "end_POI_name": "故宫博物院",
            "end_POI_address": "中国北京市东城区景山前街4号",
            "end_POI_lat": "39.9136172322172",
            "end_POI_long": "116.39729231302886",
            "passenger_lat": "39.99970025463166",
            "passenger_long": "116.32636879642432"
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
