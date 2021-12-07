import unittest
from mock import patch
from mockfirestore import MockFirestore

from models.hero import Hero

from main import app

class TestHeroModel(unittest.TestCase):
    def setUp(self):
        self.mock_db = MockFirestore()
        self.patcher = patch(
            'modules.main.MainModule.get_firestore_db', return_value=self.mock_db)
        self.patcher.start()
        self.app = app.test_client()

    def tearDown(self):
        self.patcher.stop()
        self.mock_db.reset()

    def test_save_and_get_hero(self):
        new_hero = Hero()
        new_hero.name = 'Superman'
        new_hero.description = 'Superman'
        new_hero.universe = 'dc'
        new_hero.save()

        hero = Hero.get_hero(new_hero.id)
        self.assertEqual(hero.name, 'Superman')
        self.assertEqual(hero.id, new_hero.id)
    
    def test_get_hero_not_found(self):
        hero = Hero.get_hero('ID_TEST')
        self.assertIsNone(hero)

    
    @staticmethod
    def create_hero(hero_name, universe):
        hero = Hero()
        hero.name = hero_name
        hero.description = '{0} description'.format(hero_name)
        hero.universe = universe
        hero.save()
        return hero

    def test_get_heroes(self):
        for index in range(1, 21):
            self.create_hero('Hero {0}'.format(index), 'marvel')

        heroes = Hero.get_heroes()
        heroes_dict = [hero.to_dict() for hero in heroes]

        self.assertEqual(len(heroes_dict), 16)
        for hero in heroes_dict:
            self.assertTrue(hero['name'].startswith('Hero'))
    
    def test_delete_hero(self):
        hero = self.create_hero('Joker', 'dc')
    
        Hero.delete(hero.id)

    
        self.assertIsNone(Hero.get_hero(hero.id))