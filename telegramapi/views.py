from logging import exception

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response

from game.models import Player, TheWorld, Interface
from telegramapi.models import TelegramApi


class TelegramUpdate(viewsets.ViewSet):
    telegram = TelegramApi.getService()
    the_world = TheWorld()

    def create(self, request):
        message = None
        identifier = None
        try:
            print("------New update from telegram-----")
            command = request.data['message']['text']
            if 'enter' == command:
                identifier = request.data['message']['chat']['id']
                if len(request.data['message']['text'].split(" ")) == 1:
                    message = 'Which world do you wish to fight for?( /enter world_name )'
                else:
                    world = request.data['message']['text'].split(" ")[1]
                    player_name = request.data['message']['chat']['username']
                    message = Interface.enter(world, identifier, player_name)

            elif 'leave' == command:
                identifier = request.data['message']['chat']['id']
                message = Interface.leave(identifier)

            elif 'history' == command:
                identifier = request.data['message']['chat']['id']
                message = Interface.history(identifier)

            elif 'overview' == command:
                identifier = request.data['message']['chat']['id']
                message = Interface.overview(identifier)

            elif 'command' == command:
                identifier = request.data['message']['chat']['id']
                message = Interface.command_interface(identifier, message)

            elif command.match(
                    r'(\battack|defend|ambush\b) (\b([^\s]+)\b) (\bwith\b) (\bspy|peon\b) (\bfrom\b) (\b([^\s]+)\b)'):
                message = Interface.command(identifier, command)
            else:
                message = 'Sorry general, but  don\'t get what are you saying? (' + command + ')'
            print("------End update from telegram-----")
        except Exception as e:
            print('MORREU')
            print(e)
        if (identifier):
            self.telegram.sendMessage(message, identifier, TelegramApi.buildReplyMarkup())
        return Response(status=status.HTTP_200_OK)
