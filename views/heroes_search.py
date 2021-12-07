from modules.hero import Hero
from flask import request
from flask_restful import Resource

class HeroesSearchHandler(Resource):
    def get(self):
        """Get heroes"""
        try:
            param = request.args.get('name')
            if  param: 
                heroes = Hero.search_heroes(request.args.get('name'))
                response = {
                    'heroes': [],
                }
                
                # Vamos percorer os herois e transformar em json
                for hero in heroes:
                    response['heroes'].append(hero.to_dict())
                if heroes:
                    return response['heroes']
                return {'message': 'Hero not found'}, 404
            else:
                return {
                    'message': 'Bad request, param name is required'
                }, 400
        except Exception as error:
            return {
                    'message': 'Bad request, param name is required'
                }, 400