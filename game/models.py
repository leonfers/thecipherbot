from multiprocessing.pool import Pool
from random import randrange

from django.db import models, transaction
from django.contrib.auth.models import User

from .models import *


class TheWorld(models.Model):
    world = None
    pool = Pool()

    def addEvent(self, event):
        self.pool.map(event.execute)

    @staticmethod
    def getTheWorld():
        if (TheWorld.world == None):
            world = TheWorld.objects.all().first()
            if (world):
                TheWorld.world = world
            else:
                TheWorld.world = TheWorld()
                TheWorld.world.save()
        return TheWorld.world

    def createTerritory(self, name, identifier, player_name):
        territory = Territory.objects.filter(name=name).first()
        print(territory)
        if (territory is None):
            territory = Territory()
            territory.name = name
            territory.world = TheWorld.getTheWorld()
            territory.save()
            print('Territorio criado')

        return TheWorld.getTheWorld().createPlayer(identifier, player_name, territory);

    def createPlayer(self, identifier, player_name, territory):
        player = Player.objects.filter(identifier=identifier).first()
        if (player is None):
            player = Player()
            player.identifier = identifier
            player.name = player_name
            player.territory = territory
            player.save()

            unit = Unit()
            unit.player = player
            unit.category = UNIT_TYPES.__getitem__(1)
            unit.field = None
            unit.save()
            print('Unit created')

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

            print('Player ' + player_name + 'created')
        else:
            print('Player ' + player_name + 'loaded')
        player.territory = territory
        player.save()

        return player


class Territory(models.Model):
    name = models.CharField(max_length=255, null=False)
    world = models.ForeignKey(TheWorld, related_name='territories', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Field(models.Model):
    name = models.CharField(max_length=255, null=False)
    territory = models.ForeignKey(Territory, related_name='fields', on_delete=models.CASCADE)


class Player(models.Model):
    name = models.CharField(max_length=255, null=False)
    identifier = models.IntegerField(null=False)
    territory = models.ForeignKey(Territory, related_name='players', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


UNIT_TYPES = (('P', 'Peon'), ('S', 'Spy'),)


class Unit(models.Model):
    name = models.CharField(max_length=255, null=False)
    category = models.CharField(max_length=255, choices=UNIT_TYPES, null=False)
    field = models.ForeignKey(Field, related_name='units', on_delete=models.CASCADE, null=True)
    player = models.ForeignKey(Player, related_name='units', on_delete=models.CASCADE)

    def action(self):
        pass

    def __str__(self):
        return self.name + self.category[1]


COMMAND_TYPE = (('F', 'FAKE'), ('R', 'REAL'))


class Command(models.Model):
    type = models.CharField(max_length=255, choices=COMMAND_TYPE, null=False)
    origin = models.CharField(max_length=255, null=False)
    target = models.CharField(max_length=255, null=False)
    action = models.CharField(max_length=255, null=False)
    unit = models.ForeignKey(Unit, related_name='units', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.origin + self.target + self.action + str(self.soldier)

    def execute(self):
        print("Teste " + self)


TRANSMISSION_STATUS = (('C', 'COMPLETED'), ('I', 'INTERCEPTED'), ('T', 'TRANSIT'), ('D', 'DAMAGED'))


class Transmission(models.Model):
    command = models.OneToOneField('Command', on_delete=models.DO_NOTHING)
    time_in_minutes = models.IntegerField(null=False)
    status = models.CharField(max_length=255, choices=TRANSMISSION_STATUS, null=False)
    cost = models.IntegerField(null=False)

    def __str__(self):
        return str(self.command) + str(self.time_in_minutes) + str(self.status) + str(self.cost)


class Interface():

    @staticmethod
    def start(world, identifier, player_name):
        player = Player.objects.filter(identifier=identifier).first()
        if player and player.territory is not None:
            return "You have a kingdom to defend, do not flee to another world!"
        else:
            TheWorld.getTheWorld().createTerritory(world, identifier, player_name)
            return "Might CIO " + player_name + " do your best to defeat our enemies in this " \
                                                "war of information, repair our kingdom " + world + " to prosperity " \
                                                                                                                    "with your Information Skills! "

    @staticmethod
    def leave(identifier):
        player = Player.objects.filter(identifier=identifier).first()
        if player and player.territory is not None:
            territory = player.territory
            player.territory = None
            player.save()
            if len(territory.players.all()) == 0:
                territory.delete()
                return "Our hero, may your journey to other counties be amazing, thank you for saving us!"
            else:
                return "Coward, we trusted you, know that you will be not missed, we will win this war by ourselves!"
        else:
            return "What exactly are you trying to leave?"

    @staticmethod
    def overview(self, player):
        print("dentro")

    @staticmethod
    def opponents(self, player):
        print("dentro")

    @staticmethod
    def history(self, player):
        print("dentro")
