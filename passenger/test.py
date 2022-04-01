from django.test import TestCase


class PassengerTokenTest(TestCase):
    def setUp(self):
        pass

    def test_obtain_passenger_token_pair(self):
        payload = {
            'code': 'superuser0'
        }
        response = self.client.post('/api/passenger/token',
                                    data=payload,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_refresh_passenger_token(self):
        payload = {
            'code': 'superuser0'
        }
        response = self.client.post('/api/passenger/token',
                                    data=payload,
                                    content_type='application/json')

        access_token = response.data['access']
        refresh_token = response.data['refresh']

        self.assertEqual(response.status_code, 200)

        payload = {
            'refresh': refresh_token
        }

        response = self.client.post('/api/passenger/token/refresh',
                                    data=payload,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)

        # refreshing with a wrong token
        payload = {
            'refresh': access_token
        }

        response = self.client.post('/api/passenger/token/refresh',
                                    data=payload,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_verify_passenger_token(self):
        payload = {
            'code': 'superuser0'
        }
        response = self.client.post('/api/passenger/token',
                                    data=payload,
                                    content_type='application/json')

        access_token = response.data['access']
        refresh_token = response.data['refresh']

        self.assertEqual(response.status_code, 200)

        payload = {
            'token': refresh_token
        }

        response = self.client.post('/api/passenger/token/verify',
                                    data=payload,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)

        payload = {
            'token': access_token
        }

        response = self.client.post('/api/passenger/token/verify',
                                    data=payload,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)

        payload = {
            'refresh': access_token
        }

        response = self.client.post('/api/passenger/token/refresh',
                                    data=payload,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 401)

    def test_invalid_passenger_code(self):
        payload = {
            'code': 'invalidusercode'
        }
        response = self.client.post('/api/passenger/token',
                                    data=payload,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_invalid_passenger_token_verify(self):
        payload = {
            'token': 'invalidtoken11223344'
        }
        response = self.client.post('/api/passenger/token',
                                    data=payload,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
