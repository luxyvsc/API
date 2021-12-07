from sys import path
import unittest

from mock import patch
from mockfirestore import MockFirestore
from modules.hero import Hero
from views.heroes import HeroHandler

from main import app

class HeroesHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_db = MockFirestore()
        self.patcher = patch(
            'modules.main.MainModule.get_firestore_db', return_value=self.mock_db
        )
        self.patcher.start()
        self.app = app.test_client()

    def tearDown(self):
        self.patcher.stop()
        self.mock_db.reset()

    def test_create_a_new_hero(self):
        params = {
            'hero': {
                'name': ' Superman ',
                'description': 'Superman description',
                'universe': 'DC',
                'imageUrl': 'https://image.com.br/image.jpg'
            }
        }
        response = self.app.post(path='/heroes', json=params)
        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(response.get_json())
        self.assertIsNotNone(response.get_json()['id'])

    def test_get_heroes(self):
        for index in range(1, 21):
            
            self.create_hero('Hero {0}'.format(index), 'marvel')
        response = self.app.get(path='/heroes')
        self.assertEqual(response.status_code, 200)
        self.assertIn('cursor', response.get_json())
        self.assertEqual(len(response.get_json()['heroes']), 16)

        cursor = response.get_json()['cursor']
        response = self.app.get(path='/heroes?cursor=' + cursor)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()['heroes']), 4)
             
    @staticmethod
    def create_hero(hero_name, universe):
        hero = Hero()
        hero.name = hero_name
        hero.description = '{0} description'.format(hero_name)
        hero.universe = universe
        hero.save()
        return hero
    
    def test_get_hero(self):
        
        hero_id = self.create_hero('Hero', 'DC')
        response = self.app.get('/hero/{0}'.format(hero_id.to_dict()['id']))
        self.assertEqual(response.status_code, 200)

        hero_dict = response.get_json()
        self.assertEqual(hero_dict['name'], 'Hero')
        self.assertEqual(hero_dict['id'], hero_id.to_dict()['id'])

    def test_get_hero_not_found(self):
        response = self.app.get('/hero/id_aleatorio')
    
        self.assertEqual(response.status_code, 404)

        self.assertDictEqual(
            response.get_json(),
            {
            'message': 'Hero not found',
            }
        )
    
    def test_update_hero(self):

        hero = self.create_hero('Hero', 'dc')

        params = {
            'hero': {
                'name': 'Hawkwoman',
                'description': hero.description,
                'universe': hero.universe,
                'imageUrl': 'https://exitoina.uol.com.br/media/_versions/mulher_gaviao_3_widexl.jpg'
            }
        }
        response = self.app.post(path='/hero/{0}'.format(hero.id), json=params)

        self.assertEqual(response.status_code, 500)

        hero_updated = Hero.get_hero(hero.id)
        self.assertEqual(hero_updated.name, 'Hero')

    def test_delete_hero(self):

        hero = self.create_hero('Hero', 'dc')

        response = self.app.delete(path='/hero/{0}'.format(hero.id))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.get_json(), {'message': 'Hero deleted'})

        self.assertIsNone(Hero.get_hero(hero.id))
    
    def test_create_hero_without_name(self):
        params = {
            'hero': {
                'name': '',
                'description': '',
                'universe': 'dc',
                'imageUrl': 'https://image.com.br/image.jpg'
            }
        }
        response = self.app.post(path='/heroes', json=params)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['details'],
                        'Bad request, name is required')
    
    def test_create_hero_with_invalid_universe(self):
        params = {
            'hero': {
                'name': ' SUPERMAN ',
                'description': 'Hero description',
                'universe': 'x-men',
                'imageUrl': 'https://image.com.br/image.jpg'
            }
        }
        response = self.app.post(path='/heroes', json=params)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['details'],
                        'Bad request, invalid universe')

if __name__ == '__main__':
    unittest.main()