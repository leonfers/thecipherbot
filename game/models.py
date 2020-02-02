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
        print("New event to te world!")
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
            cipher = CesarCipher()
            cipher.shift = randrange(1, 5, 1)
            cipher.save()
            player.cipher = cipher
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
        unit.category = 'spy'
        unit.current_action = ACTIONS[randrange(0, 3, 1)]
        unit.field = None
        unit.save()

        unit = Unit()
        unit.player = player
        unit.category = 'warrior'
        unit.current_action = ACTIONS[randrange(0, 3, 1)]
        unit.field = None
        unit.save()

        unit = Unit()
        unit.player = player
        unit.category = 'warrior'
        unit.current_action = ACTIONS[randrange(0, 3, 1)]
        unit.field = None
        unit.save()

        print('Units created')

        units = player.units.all()
        for u in units:
            u.field = territory.fields.all()[randrange(0, 9, 1)]
            u.save()
            print('Unidade posicionada')


        player.territory = territory
        player.save()

        return player


class Territory(models.Model):
    name = models.CharField(max_length=255, null=False)
    world = models.ForeignKey(TheWorld, related_name='territories', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


CITIES = ['Dadon', 'Tila', 'Ekasa', 'Oreford', 'Mudale', 'Hale', 'Jumond', 'Lore', 'Erysa']


class Field(models.Model):
    name = models.CharField(max_length=255, null=False)
    territory = models.ForeignKey(Territory, related_name='fields', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CesarCipher(models.Model):
    shift = models.IntegerField(null=False)

    def encrypt(self, text):
        result = ''
        for i in range(len(text)):
            char = text[i]
            if (char != ' '):
                if (char.isupper()):
                    result += chr((ord(char) + self.shift - 65) % 26 + 65)
                else:
                    result += chr((ord(char) + self.shift - 97) % 26 + 97)
            else:
                result += ' '
        return result


class Player(models.Model):
    name = models.CharField(max_length=255, null=False)
    identifier = models.IntegerField(null=False)
    cipher = models.OneToOneField(CesarCipher, related_name='player', on_delete=models.CASCADE)
    territory = models.ForeignKey(Territory, related_name='players', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


UNIT_TYPES = ['warrior', 'spy']


class Unit(models.Model):
    name = models.CharField(max_length=255, null=False)
    category = models.CharField(max_length=255, null=False)
    field = models.ForeignKey(Field, related_name='units', on_delete=models.CASCADE, null=True)
    player = models.ForeignKey(Player, related_name='units', on_delete=models.CASCADE)
    current_action = models.CharField(max_length=255, null=False)

    def battle(self, enemy_unit):
        print(enemy_unit.current_action)
        print(self.current_action)
        if enemy_unit.current_action == self.current_action:
            if (self.category == 'spy'):
                TelegramApi.getService().sendMessage(
                    "S.O.S enemy spoted at " + self.field.name + "at position of " + enemy_unit.current_action + " send backup!",
                    self.player.identifier, TelegramApi.buildReplyMarkup())
            else:
                TelegramApi.getService().sendMessage("S.O.S enemy spoted at " + self.field.name + " send backup!",
                                                     self.player.identifier, TelegramApi.buildReplyMarkup())
                TelegramApi.getService().sendMessage(
                    "S.O.S i am under siege at " + enemy_unit.field.name + " send backup!",
                    enemy_unit.player.identifier, TelegramApi.buildReplyMarkup())
        elif Util.winning_action(self.current_action, enemy_unit.current_action):
            if (self.category == 'spy'):
                TelegramApi.getService().sendMessage(
                    "S.O.S enemy spoted at " + self.field.name + "at position of " + enemy_unit.current_action + " send backup,!",
                    self.player.identifier, TelegramApi.buildReplyMarkup())
            else:
                if len(enemy_unit.player.units.all()) < 2:
                    enemy_unit.delete()
                    TelegramApi.getService().sendMessage(
                        "You lost the war useless CIO, go back to where you came from!",
                        enemy_unit.player.identifier, TelegramApi.buildReplyMarkup())
                    TelegramApi.getService().sendMessage("Enemy eliminated at " + self.field.name + ", job done!",
                                                         self.player.identifier, TelegramApi.buildReplyMarkup())
                else:
                    enemy_unit.delete()
                    TelegramApi.getService().sendMessage("Enemy eliminated at " + self.field.name + ", job done!",
                                                         self.player.identifier, TelegramApi.buildReplyMarkup())


        else:
            print("Ganhou quem defende!")

            if (enemy_unit.category == 'spy'):
                TelegramApi.getService().sendMessage(
                    "S.O.S enemy spoted at " + self.field.name + "at position of " + self.current_action + " send backup,!",
                    enemy_unit.player.identifier, TelegramApi.buildReplyMarkup())
            else:
                TelegramApi.getService().sendMessage(
                    "Invader eliminated at " + enemy_unit.field.name + ", I hope they keep sending more!",
                    enemy_unit.player.identifier, TelegramApi.buildReplyMarkup())
                self.delete()

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
        return str(self.action) + " " + str(self.target) + " " + str(self.unit) + " " + str(self.origin)

    @staticmethod
    def execute(event):
        player = Player.objects.filter(identifier=event.player.identifier).first()
        for p in player.territory.players.all():
            if (p != player):
                message = str(event).split(' ')
                TelegramApi.getService().sendMessage('Interceptamos uma mensagem, CIO \n' +
                                                     player.cipher.encrypt(str(player.name)) + ': '
                                                     + player.cipher.encrypt(message[0]) +
                                                     ' '
                                                     + player.cipher.encrypt(message[1]) +
                                                     ' with '
                                                     + player.cipher.encrypt(message[2]) +
                                                     ' from '
                                                     + player.cipher.encrypt(message[3]),
                                                     p.identifier, TelegramApi.buildReplyMarkup())

        if event.action == 'attack':
            time.sleep(5)
        elif event.action == 'ambush':
            time.sleep(10)
        elif event.action == 'defend':
            time.sleep(15)

        player = Player.objects.filter(identifier=event.player.identifier).first()
        origin = player.territory.fields.all().filter(name=event.origin).first()
        unit = origin.units.all().filter(category=event.unit).first()
        if unit:
            target = player.territory.fields.filter(name=event.target).first()
            enemies = Util.filter_enemies(player, target.units.all())
            unit.field = target
            unit.current_action = event.action
            unit.save()
            if (len(enemies) > 0):
                unit.battle(enemies.__getitem__(randrange(0, len(enemies), 1)))
            else:
                TelegramApi.getService().sendMessage(
                    "I " + str(unit.category) + " moved to new location at " + str(event.target) + " with no problems",
                    event.player.identifier, TelegramApi.buildReplyMarkup())
        else:
            TelegramApi.getService().sendMessage(
                "There is no one to carry on the orders here at " + str(event.origin) + " , did something happen?",
                event.player.identifier, TelegramApi.buildReplyMarkup())

    @staticmethod
    def command_builder(player, message):
        print("Entrou comando builder")
        elements = message.split(' ')
        print(elements)
        command = Command()
        command.origin = player.territory.fields.filter(name=elements[5]).get()
        command.target = player.territory.fields.filter(name=elements[1]).get()
        command.player = player
        command.unit = elements[3]
        command.action = elements[0]
        command.save()
        return command


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
                return "Our hero, may your journey to other realms be amazing, thank you for saving us!"
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
            overview = "Mr(s). " + player.name + ", in the realm of " + str(player.territory) + " you have : \n\n"
            units = player.units.all()
            for unit in units:
                overview += 'an allied ' + str(
                    unit) + ' at ' + unit.field.name + ' on ' + unit.current_action + ' position \n'

            enemy_units = Unit.objects.all();
            enemy_units_same_territory = []
            for unit in enemy_units:
                if (unit.player.territory == player.territory):
                    enemy_units_same_territory.append(unit)
            overview += '\nYou are up against ' + str(
                len(Player.objects.filter(territory=player.territory).all()) - 1) + ' rivals.\n' \
                                                                                    'There are ' + str(
                len(enemy_units_same_territory) - len(player.units.all())) + ' enemy units left in the war.' \
                                                                             '\nCities: ' + (str(CITIES)).replace("\'",
                                                                                                                  "")
            return overview
        else:
            overview = "Mr(s). " + player.name + ", in the realm of " + str(
                player.territory) + " you have no one to help you, you should flee!"
            enemy_units = Unit.objects.all();
            enemy_units_same_territory = []
            for unit in enemy_units:
                if (unit.player.territory == player.territory):
                    enemy_units_same_territory.append(unit)
            overview += '\nYou are up against ' + str(
                len(Player.objects.filter(territory=player.territory).all()) - 1) + ' rivals.\n' \
                                                                                    'There are ' + str(
                len(enemy_units_same_territory)) + ' enemy units left in the war.' \
                                                   '\nCities: ' + (str(CITIES)).replace("\'",
                                                                                        "")
            return overview

    @staticmethod
    def command(identifier, message):
        player = Player.objects.filter(identifier=identifier).first()
        if (player and player.territory):
            if (len(player.territory.players.all()) > 1):
                if message.split(' ')[5] not in CITIES:
                    return 'Master, i do not know the city: ' + str(message.split(' ')[5])
                elif message.split(' ')[1] not in CITIES:
                    return 'Master, i do not know the city: ' + str(message.split(' ')[1])
                else:
                    command = Command.command_builder(player, message)
                    TheWorld.getTheWorld().addEvent(command)

                return 'Your command has being sent, master, we shall hope it reaches the right hands!'
            else:
                return 'The land of ' + str(player.territory) + ' is in peace, there is no need to worry about enemies.'
        else:
            return 'Command who and where? ( enter world_name )'

    @staticmethod
    def history(identifier):
        player = Player.objects.filter(identifier=identifier).first()
        if (player and player.territory):
            if (len(player.territory.players.all()) > 1):
                return 'The realm of ' + str(player.territory) + ' has ' + str(
                    len(player.territory.players.all())) + ' rulers. \n' \
                                                           'We trust you ' + player.name + ' to protect our good leader from their rivals and repair the damage ' \
                                                                                           'caused by this war. \n\n' \
                                                                                           'We believe your cunning tactics and masterful manipulation of information can turn the tides of this war and end it ' \
                                                                                           'once and for all.\n\n' \
                                                                                           'Uncover the plot of the vilains, by intercepting their commands, repair the information if needed and counter atack their evil plans!'
            else:
                return 'The land of ' + str(player.territory) + ' is in peace.'
        else:
            return 'History of where? ( enter world_name )'

    @staticmethod
    def start():
        return "In this game, each player enters a realm with a certain number of units (warriors and spies). When more than one player " \
               "enters the same kingdom, they battle each other over the kingdom.\nThe objective of the game is to defeat all enemy troops.\nTroops can be moved with three " \
               "actions:\n\n attack, ambush and defend \n\nAttacking wins ambushing.\nAmbushing wins defending.\nDefending wins attacking.\n\n" \
               "You can intercept enemy messages and repair it\'s contents to launch counter attacks!" \
               "\nBy defeating all enemies, you will " \
               "repair the kingdom\'s peace."

    @staticmethod
    def enter_help():
        return "To enter a world type: enter world_name" \
               "\n like: \n" \
               "enter Narnia "

    @staticmethod
    def command_interface():
        return "To command your units use the following structure:\n\n" \
               "<action> <target> with <unit> from <unit\'s origin>\n\n" \
               "An example would be:" \
               "\ndefend Jumond with warrior from Jumond"


class Util():

    @staticmethod
    def filter_enemies(player, units):
        enemy = []
        for unit in units:
            if (unit.player != player):
                enemy.append(unit)
        return enemy

    @staticmethod
    def winning_action(action, action_enemy):
        if (action == 'attack' and action_enemy == 'ambush'):
            return True
        elif (action == 'attack' and action_enemy == 'defend'):
            return False
        elif (action == 'ambush' and action_enemy == 'attack'):
            return False
        elif (action == 'ambush' and action_enemy == 'defend'):
            return True
        elif (action == 'defend' and action_enemy == 'attack'):
            return True
        elif (action == 'defend' and action_enemy == 'ambush'):
            return False
