from .utils import *


class PassengerInfoTest(TestCase):
    def setUp(self):
        pass

    def test_get_info(self):
        access_token, refresh_token, status_code = authenticate(self)
        self.assertEqual(status_code, 200)
        response = self.client.get(
            '/api/passenger/info',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_post_info(self):
        access_token, refresh_token, status_code = authenticate(self)
        self.assertEqual(status_code, 200)
        payload = {
            'username': 'updatedUsername',
        }
        response = self.client.post(
            '/api/passenger/info',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload, response.data)

        # Get the user info again
        response = self.client.get(
            '/api/passenger/info',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload, response.data)
