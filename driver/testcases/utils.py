from django.test import TestCase


def authenticate(self):
    payload = {
        'code': 'superuser0'
    }
    response = self.client.post('/api/driver/token',
                                data=payload,
                                content_type='application/json')
    access_token = response.data['access']
    refresh_token = response.data['refresh']
    return access_token, refresh_token, response.status_code
