from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response

from game.models import Player
from game.theworld import TheWorld
from telegramapi.models import TelegramApi


class TelegramUpdate(viewsets.ViewSet):
    telegram = TelegramApi.getService()
    the_world = TheWorld()

    def create(self, request):
        try:
            print("------New update from telegram-----")
            if (Player.objects.get(identifer=request.data['message']['chat']['id'])):
                print('jogador já existe')
            else:
                TheWorld.getTheWorld().createTerritory(self, request.data['message']['text'],
                                                       request.data['message']['chat']['id'],
                                                       request.data['message']['from']['username'])
                print("------End update from telegram-----")
        except:
            print('MORREU')
        self.telegram.sendMessage(request.data['message']['text'], request.data['message']['chat']['id'])
        return Response(status=status.HTTP_200_OK)
