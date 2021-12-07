import uuid

from firebase_admin import firestore
from modules.main import MainModule

class Hero(object):
    _collection_name = 'Hero'

    def __init__(self, **args):
        self.id = args.get('id', uuid.uuid4().hex)
        self.name = args.get('name')
        self.description = args.get('description')
        self.universe = args.get('universe')
        self.imageUrl = args.get('imageUrl')
        
    def save(self):
        MainModule.get_firestore_db().collection(
            self._collection_name).document(self.id).set(self.to_dict())
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'universe': self.universe,
            'imageUrl': self.imageUrl,
        }
    @classmethod
    def search_heroes(cls, hero_name):
        hero = MainModule.get_firestore_db().collection(
            cls._collection_name).where('name', '==', f'{hero_name.title()}').stream()
        if hero:
            return hero
        return None

    @classmethod
    def get_hero(cls, hero_id):
        hero = MainModule.get_firestore_db().collection(
            cls._collection_name).document(hero_id).get()
        if hero.exists:
            return Hero(**hero.to_dict())
        return None

    @classmethod
    def get_heroes(cls, cursor=None):
        query = MainModule.get_firestore_db().collection(
            cls._collection_name).order_by('id').limit(16)
        if cursor:
            query = query.start_after({
                'id': cursor
            })
        return query.stream()

    @classmethod
    def delete(cls, hero_id):
        return MainModule.get_firestore_db().collection(
            cls._collection_name).document(hero_id).delete()
    
    @classmethod
    def get_top_heroes(cls):
        return MainModule.get_firestore_db().collection(
            cls._collection_name).limit(20).stream()
        
    