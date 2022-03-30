from django.test import TestCase


class PassengerModelTests(TestCase):
    def setUp(self):
        pass

    # Tests for tokens
    def test_obtain_passenger_token(self):
        pass

    def test_invalid_passenger_code(self):
        payload = {
            'code': 'invalidusercode'
        }
        response = self.client.post('/api/passenger/token',
                                    data=payload,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_invalid_token_verify(self):
        payload = {
            'token': 'invalidtoken11223344'
        }
        response = self.client.post('/api/passenger/token',
                                    data=payload,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)