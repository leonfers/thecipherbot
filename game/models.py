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

            for i in range(9):
                field = Field()
                field.name = CITIES[i]
                field.territory = territory
                field.save()
                print('Field created')

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

            print('Player ' + player_name + 'created')
        else:
            print('Player ' + player_name + 'loaded')

        for unit in player.units.all():
            unit.delete()

        unit = Unit()
        unit.player = player
        unit.category = UNIT_TYPES[randrange(0, 2, 1)]
        unit.field = None
        unit.save()
        print('Unit created')

        unit = player.units.first()
        unit.field = territory.fields.all()[randrange(0, 10, 1)]
        unit.save()
        print('Unidade posicionada')

        player.territory = territory
        player.save()

        return player


class Territory(models.Model):
    name = models.CharField(max_length=255, null=False)
    world = models.ForeignKey(TheWorld, related_name='territories', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


CITIES = ['sparta', 'atenas', 'teresina', 'rio', 'cairo', 'persia', 'nilo', 'japao', 'londres']


class Field(models.Model):
    name = models.CharField(max_length=255, null=False)
    territory = models.ForeignKey(Territory, related_name='fields', on_delete=models.CASCADE)


class Player(models.Model):
    name = models.CharField(max_length=255, null=False)
    identifier = models.IntegerField(null=False)
    territory = models.ForeignKey(Territory, related_name='players', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


UNIT_TYPES = ['Peon', 'Spy']


class Unit(models.Model):
    name = models.CharField(max_length=255, null=False)
    category = models.CharField(max_length=255, null=False)
    field = models.ForeignKey(Field, related_name='units', on_delete=models.CASCADE, null=True)
    player = models.ForeignKey(Player, related_name='units', on_delete=models.CASCADE)

    def action(self):
        pass

    def __str__(self):
        return self.category


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
    def enter(world, identifier, player_name):
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
                for unit in player.units.all():
                    unit.delete()
                return "Our hero, may your journey to other counties be amazing, thank you for saving us!"
            else:
                for unit in player.units.all():
                    unit.delete()
                return "Coward, we trusted you, know that you will be not missed, we will win this war by ourselves!"
        else:
            return "What exactly are you trying to leave?"

    @staticmethod
    def overview(identifier):
        player = Player.objects.filter(identifier=identifier).first()
        if player and len(player.units.all()) > 0:
            overview = "Mr(s). " + player.name + " you have : "
            units = player.units.all()
            for unit in units:
                overview += '\n an allied ' + str(unit) + ' at ' + unit.field.name

            enemy_units = Unit.objects.all();
            enemy_units_same_territory = []
            for unit in enemy_units:
                if (unit.player.territory == player.territory):
                    enemy_units_same_territory.append(unit)
            overview += '\n\nYou are up against ' + str(
                len(Player.objects.filter(territory=player.territory).all()) - 1) + ' rivals.\n' \
                                                                                    'There are ' + str(
                len(enemy_units_same_territory) - len(player.units.all())) + ' enemy units left in the war.'
            return overview
        else:
            return 'What units? ( /enter name_world)'


    @staticmethod
    def opponents(self, player):
        print("dentro")


    @staticmethod
    def history(identifier):
        player = Player.objects.filter(identifier=identifier).first()
        if (player and player.territory):
            if (len(player.territory.players.all()) > 1):
                return 'The land of ' + str(player.territory) + ' has ' + str(
                    len(player.territory.players.all())) + ' rulers. \n' \
                                                           'We trust you ' + player.name + ' to protect our good leader from their rivals and repair the damage ' \
                                                                                           'caused by this war. \n\n' \
                                                                                           'We believe your cunning tactics and masterful manipulation of information can turn the tides of this war and end it ' \
                                                                                           'once and for all.\n\n' \
                                                                                           'Uncover the plot of the vilains, by intercepting their commands, repair the information if needed and counter atack their evil plans!'
            else:
                return 'The land of ' + str(player.territory) + ' is in peace.'
        else:
            return 'History of where? ( /enter world_name )'
