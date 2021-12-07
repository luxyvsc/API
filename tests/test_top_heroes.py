import unittest

from mock import patch
from mockfirestore import MockFirestore

from main import app
from models.hero import Hero


class TopHeroesHandlerTestCase(unittest.TestCase):

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

    @staticmethod
    def create_hero(hero_name, universe):
        hero = Hero()
        hero.name = hero_name
        hero.description = '{0} description'.format(hero_name)
        hero.universe = universe
        hero.save()
        return hero

    def test_get_top_heroes(self):
        for index in range(1, 21):
            self.create_hero('Hero {0}'.format(index), 'marvel')
        
        response = self.app.get(path='/top-heroes')
        first_hero_list = response.get_json()['heroes']
        self.assertEqual(len(first_hero_list), 4)
        self.assertEqual(response.status_code, 200)
        

        response = self.app.get(path='/top-heroes')
        self.assertEqual(response.status_code, 200)
        second_hero_list = response.get_json()['heroes']
        self.assertEqual(len(second_hero_list), 4)

        self.assertNotEqual(first_hero_list, second_hero_list)

if __name__ == '__main__':
    unittest.main()