import unittest

from main import app

class TestMain(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
 
    def test_get_index_url(self):
        response = self.app.get('/')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.get_json(), {'API': 'Heroes'})

    def test_get_not_found_url(self):
        response = self.app.get('/teste/teste/teste')

        self.assertEqual(response.status_code, 404)

        self.assertEqual(response.get_data(), b'Sorry, Nothing at this URL.')

if __name__ == '__main__':
    unittest.main()