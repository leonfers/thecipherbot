from multiprocessing import Pool
from random import randrange

from . import models
from .models import Territory, Field, Player, Unit, UNIT_TYPES


class TheWorld(models.Model):
    world = None
    pool = Pool()

    def addEvent(self, event):
        self.pool.map(event.execute)

    @staticmethod
    def getTheWorld():
        if (TheWorld.world == None):
            TheWorld.world = TheWorld()
        return TheWorld.world

    def createTerritory(self, name, identifier, player_name):
        territory = Territory.objects.get(name='name')
        if (territory is None):
            territory = Territory()
            territory.name = name
            territory.world = TheWorld.getTheWorld()
            territory.save()
            print('Territorio criado')

        player = TheWorld.getTheWorld().createPlayer(identifier, player_name, territory);

        for i in range(9):
            field = Field()
            field.name = str(i) + str(i) + str(i) + str(i)
            field.territory = territory
            field.save()
            print('Field created')

        unit = player.units.first()
        unit.field = territory.fields.all()[randrange(0, 10, 1)]
        unit.save()
        print('Unidade posicionada')

    def createPlayer(self, identifier, player_name, territory):
        player = Player.objects.get(identifier=identifier)
        if (player is None):
            player = Player()
            player.name = player_name
            player.territory = territory
            player.save()
            print('Player '+player_name+'created')
        else:
            print('Player '+player_name+'loaded')

        unit = Unit()
        unit.player = player
        unit.category = UNIT_TYPES.__getitem__(1)
        unit.field = None
        unit.save()
        print('Unit created')
