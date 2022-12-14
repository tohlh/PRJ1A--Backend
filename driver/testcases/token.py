from .utils import *


class DriverTokenTest(TestCase):
    def setUp(self):
        pass

    def test_obtain_driver_token_pair(self):
        _, _, status_code = auth_driver(self,
                                        'superuser1')

        self.assertEqual(status_code, 200)

    def test_refresh_token(self):
        access_token, refresh_token, status_code = auth_driver(self,
                                                               'superuser1')
        self.assertEqual(status_code, 200)

        payload = {
            'refresh': refresh_token
        }
        response = self.client.post('/api/driver/token/refresh',
                                    data=payload,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # refreshing with a wrong token
        payload = {
            'refresh': access_token
        }
        response = self.client.post('/api/driver/token/refresh',
                                    data=payload,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_verify_token(self):
        access_token, refresh_token, status_code = auth_driver(self,
                                                               'superuser1')
        self.assertEqual(status_code, 200)

        payload = {
            'token': refresh_token
        }
        response = self.client.post('/api/driver/token/verify',
                                    data=payload,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

        payload = {
            'token': access_token
        }
        response = self.client.post('/api/driver/token/verify',
                                    data=payload,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

        payload = {
            'refresh': access_token
        }
        response = self.client.post('/api/driver/token/refresh',
                                    data=payload,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_invalid_code(self):
        payload = {
            'code': 'invalidusercode'
        }
        response = self.client.post('/api/driver/token',
                                    data=payload,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_invalid_token_verify(self):
        payload = {
            'token': 'invalidtoken11223344'
        }
        response = self.client.post('/api/driver/token',
                                    data=payload,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
