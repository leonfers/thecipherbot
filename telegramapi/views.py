from logging import exception

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response

from game.models import Player, TheWorld, Interface
from telegramapi.models import TelegramApi
import re


class TelegramUpdate(viewsets.ViewSet):
    telegram = TelegramApi.getService()
    the_world = TheWorld()

    def create(self, request):
        message = None
        identifier = None
        try:
            print("------New update from telegram-----")
            command = request.data['message']['text']
            if 'enter' in command:
                identifier = request.data['message']['chat']['id']
                if len(request.data['message']['text'].split(" ")) == 1:
                    message = Interface.enter_help()
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
                message = Interface.command_interface()
                self.telegram.sendMessage(message, identifier, TelegramApi.buildReplyOverMarkup())
                return Response(status=status.HTTP_200_OK)
            elif re.match(
                    r'(\battack|defend|ambush\b) (\b([^\s]+)\b) (\bwith\b) (\bspy|warrior\b) (\bfrom\b) (\b([^\s]+)\b)',
                    command):
                identifier = request.data['message']['chat']['id']
                message = Interface.command(identifier, command)
            elif 'start' in command:
                identifier = request.data['message']['chat']['id']
                message = Interface.start()
                self.telegram.sendMessage(message, identifier, TelegramApi.buildReplyMarkup())
                return Response(status=status.HTTP_200_OK)
            else:
                identifier = request.data['message']['chat']['id']
                message = 'Sorry CIO, but  don\'t get what are you saying? (' + command + ')'

            print("------End update from telegram-----")
        except Exception as e:
            message = 'Sorry CIO, but something happends and i could do nothing about it!'
            print('MORREU de ', e)
        if (identifier):
            self.telegram.sendMessage(message, identifier, TelegramApi.buildReplyMarkup())
        return Response(status=status.HTTP_200_OK)
