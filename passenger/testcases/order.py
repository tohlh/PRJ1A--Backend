from .utils import *


class PassengerOrderTest(TestCase):
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
