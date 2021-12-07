from flask_restful import Resource
from modules.hero import HeroModule
from modules.hero import Hero
from modules.main import MainModule
from flask import request

class HeroesHandler(Resource):
    def get(self):
        try:
            heroes = Hero.get_heroes(request.args.get('cursor'))
            response = {
                'cursor': None,
                'heroes': []
            }

            for hero in heroes:
                response['heroes'].append(hero.to_dict())
            
            if len(response['heroes']) == 16:
                response['cursor'] = response['heroes'][-1]['id']
            
            return response

        except Exception as error:
            return {
                'message': 'Error on get heroes',
                'details': str(error)
            }, 500

    def post(self):
        try:
            if not request.is_json or 'hero' not in request.json:
                return {'message': 'Bad request'}, 400
            #print(f'\n  \n{request.json} \n')
            hero = HeroModule.create(request.json['hero'])
            return hero.to_dict()
        except Exception as error:
            return {
                'message': 'Error on create a new hero',
                'details': str(error)
            },500

class HeroHandler(Resource):
    def get(self, hero_id):
        try:
            hero = Hero.get_hero(hero_id)
            if hero:
                return hero.to_dict(),200
                    
                
            return {'message': 'Hero not found'},404
        except Exception as error:
            return {
                'message': 'Hero not found',
                'details': str(error)
            },500

    def post(self,hero_id):
        try:
            hero = Hero.get_hero(hero_id)
            if not hero:
                return {
                    'message': 'Hero not found'
                },404
            HeroModule.update(hero, request.json['hero'])
            return hero.to_dict()
        except Exception as error:
            return {
                'message': 'Error on update hero',
                'details': str(error)
            }, 500

    def delete(self, hero_id):
        try:
            hero = Hero.delete(hero_id)
            if not hero:
                return {
                    'message': 'Hero deleted'
                },200
            return {'message':'hero not found'}, 404
        except Exception as error:
            return {
                'message': 'Error on delete hero',
                'details': str(error)
            }, 500