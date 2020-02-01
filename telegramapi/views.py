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
        try:
            print("------New update from telegram-----")
            command = request.data['message']['text']
            identifier = request.data['message']['chat']['id']
            if '/start' in command:
                world = request.data['message']['text'].split(" ")[1]
                player_name = request.data['message']['chat']['username']
                return Interface.start(world, identifier, player_name)
            elif '/leave' in command:
                return Interface.leave(identifier)

            print("------End update from telegram-----")
        except Exception as e:
            print('MORREU')
            print(e)
        self.telegram.sendMessage(request.data['message']['text'], request.data['message']['chat']['id'])
        return Response(status=status.HTTP_200_OK)
