import time
from multiprocessing.pool import Pool
from random import randrange

from django.db import models, transaction
from django.contrib.auth.models import User
import threading

from telegramapi.models import TelegramApi
from .models import *


class TheWorld(models.Model):
    world = None

    def addEvent(self, event):
        t = threading.Thread(target=event.execute, args=[event])
        t.setDaemon(True)
        t.start()

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


ACTIONS = ['attack', 'ambush', 'defend']


class Command(models.Model):
    player = models.ForeignKey(Player, related_name='commands', on_delete=models.CASCADE)
    origin = models.CharField(max_length=255, null=False)
    target = models.CharField(max_length=255, null=False)
    action = models.CharField(max_length=255, null=False)
    unit = models.CharField(max_length=255, null=False)

    def __str__(self):
        return str(self.origin) + str(self.target) + str(self.action) + str(self.unit)

    @staticmethod
    def execute(event):
        if event.action == 'attack':
            time.sleep(30)
        elif event.action == 'ambush':
            time.sleep(50)
        elif event.action == 'defend':
            time.sleep(5)

        TelegramApi.getService().sendMessage("relatório de execução", event.player.identifier)
        print("Teste " + str(event))

    @staticmethod
    def command_builder(player, message):
        elements = message.split(' ')
        print(elements)
        command = Command()
        command.origin = player.territory.fields.filter(name=elements[0]).get()
        command.target = player.territory.fields.filter(name=elements[1]).get()
        command.player = player
        command.unit = elements[2]
        command.action = elements[3]
        command.save()
        return command


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
    def command(identifier, message):
        player = Player.objects.filter(identifier=identifier).first()
        if (player and player.territory):
            if (len(player.territory.players.all()) > 1):
                command = Command.command_builder(player, message)
                TheWorld.getTheWorld().addEvent(command)
                return 'Your command has being sent, master, we shall hope it reaches the right hands!'
            else:
                return 'The land of ' + str(player.territory) + ' is in peace, there is no need to worry about enemies.'
        else:
            return 'Command who and where? ( /enter world_name )'

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
