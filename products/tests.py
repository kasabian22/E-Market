from django.test import TestCase


class ErrorHandlersTests(TestCase):
    def test_404_returns_json_error(self):
        with self.settings(ALLOWED_HOSTS=['testserver']):
            response = self.client.get('/does-not-exist/')

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'error': 'Path not found'})
