from .utils import *


class DriverInfoTest(TestCase):
    def setUp(self):
        pass

    def test_get_info(self):
        access_token, refresh_token, status_code = auth_driver(self,
                                                               'superuser1')
        self.assertEqual(status_code, 200)
        response = self.client.get(
            '/api/driver/info',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_post_info(self):
        access_token, refresh_token, status_code = auth_driver(self,
                                                               'superuser1')
        self.assertEqual(status_code, 200)
        payload = {
            'username': 'updatedUsername',
            'carplate': '京123123',
            'phone': '01234567890',
            'age': 30,
            'identification_no': '012345678901233457'
        }
        response = self.client.post(
            '/api/driver/info',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload, response.data)

        # Get the user info again
        response = self.client.get(
            '/api/driver/info',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload, response.data)

    def test_invalid_post_info(self):
        access_token, refresh_token, status_code = auth_driver(self,
                                                               'superuser1')
        self.assertEqual(status_code, 200)
        payload = {
            'username': 'updatedUsername',
            'carplate': '京123123',
            'phone': '01234567890',
            'age': 30,
        }

        response = self.client.post(
            '/api/driver/info',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual({
            'errMsg': 'identification_no is required'
            }, response.data)

    def test_reset_info(self):
        access_token, refresh_token, status_code = auth_driver(self,
                                                               'superuser0')
        self.assertEqual(status_code, 200)

        payload = {
            'username': 'updatedUsername',
            'phone': '01234567890',
            'carplate': '京1234',
            'age': 30,
            'identification_no': '012345678901233457'
        }
        response = self.client.post(
            '/api/driver/info',
            data=payload,
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload, response.data)

        response = self.client.post(
            '/api/driver/info/reset',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual({}, response.data)

        response = self.client.get(
            '/api/driver/info',
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual({
            'username': '',
            'phone': '',
            'carplate': '',
            'age': None,
            'identification_no': ''
        }, response.data)
