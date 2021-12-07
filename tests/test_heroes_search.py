import unittest

from mock import patch
from mockfirestore import MockFirestore

from main import app
from models.hero import Hero


class HeroesSearchHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.mock_db = MockFirestore()
        self.patcher = patch(
            'modules.main.MainModule.get_firestore_db',
            return_value=self.mock_db)
        self.patcher.start()
        self.app = app.test_client()

    def tearDown(self):
        self.patcher.stop()
        self.mock_db.reset()

    def test_search_hero(self):
        self.create_hero('Superman', 'dc')
        self.create_hero('Batman', 'dc')

        response = self.app.get(path='/search?name=Batman')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.get_json()), 1)
        self.assertEqual(response.get_json()[0]['name'], 'Batman')

    def test_search_hero_with_lowercase_param_name(self):
        self.create_hero('Superman', 'dc')
        self.create_hero('Batman', 'dc')

        response = self.app.get(path='/search?name=' + 'superman')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.get_json()), 1)
        self.assertEqual(response.get_json()[0]['name'], 'Superman')

    def test_search_hero_max_returned_items(self):
        for _ in range(10):
            self.create_hero('Superman', 'dc')

        response = self.app.get(path='/search?name=' + 'Superman')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.get_json()), 10)

    def test_search_hero_without_param_name(self):

        response = self.app.get(path='/search?name=')

        self.assertEqual(response.status_code, 400)

        self.assertDictEqual(
            response.get_json(),
            {'message': 'Bad request, param name is required'}
        )

    @staticmethod
    def create_hero(hero_name, universe):
        hero = Hero()
        hero.name = hero_name
        hero.description = '{0} description'.format(hero_name)
        hero.universe = universe
        hero.save()
        return hero


if __name__ == '__main__':
    unittest.main()