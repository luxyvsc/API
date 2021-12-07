import firebase_admin
from flask import Flask
from flask_restful import Resource, Api
from flask import request
from flask_cors import CORS
from firebase_admin import firestore
from views.heroes import HeroesHandler, HeroHandler
from views.heroes_search import HeroesSearchHandler
from views.top_heroes import TopHeroesHandler

app = Flask(__name__)
CORS(app)
API = Api(app)
API.add_resource(HeroesHandler, '/heroes', endpoint='heroes')
API.add_resource(HeroHandler, '/hero/<hero_id>', endpoint='hero')
API.add_resource(TopHeroesHandler, '/top-heroes', endpoint='top-heroes')
API.add_resource(HeroesSearchHandler, '/search', endpoint='search')


cred = firebase_admin.credentials.Certificate(
    './tour-of-heroes-7f78f-firebase-adminsdk-exyc5-f4ea51991d.json'
)

firebase_admin.initialize_app(credential=cred)

@app.before_request
def start_request():
    if request.method == 'OPTIONS':
        return '', 200
    if not request.endpoint:
        return 'Sorry, Nothing at this URL.', 404

class Index(Resource):
    def get(self):
        return {"API": "Heroes"}

API.add_resource(Index, '/', endpoint='index')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)