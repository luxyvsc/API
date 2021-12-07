from models.hero import Hero

class HeroModule(object):
    @staticmethod
    def create(params):
        hero = Hero()
        hero.name = params['name']
        hero.description = params['description']
        hero.imageUrl = params['imageUrl']
        hero.universe = params['universe']
        HeroModule.valid_hero_params(hero)
        hero.save()
        return hero
    
    @staticmethod
    def update(hero, params):
        hero.name = params['name']
        hero.description = params['description']
        hero.imageUrl = params['imageUrl']
        hero.universe = params['universe']
        HeroModule.valid_hero_params(hero)
        hero.save()

    @staticmethod
    def valid_hero_params(hero):
        if not hero.name:
            raise Exception('Bad request, name is required')
        elif not hero.universe == 'DC' and not hero.universe == 'MARVEL':
            raise Exception("Bad request, invalid universe")

    
    