from .utils import *


class DriverOrderTests(TestCase):
    def setUp(self):
        pass

    def test_queue_order(self):
        access_token, refresh_token, status_code = authenticate(self)
        self.assertEqual(status_code, 200)
        response = self.client.get(
            '/api/driver/info',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_update_location(self):
        access_token, refresh_token, status_code = authenticate(self)
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
