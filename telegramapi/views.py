from logging import exception

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response

from game.models import Player, TheWorld
from telegramapi.models import TelegramApi


class TelegramUpdate(viewsets.ViewSet):
    telegram = TelegramApi.getService()
    the_world = TheWorld()

    def create(self, request):
        try:
            print("------New update from telegram-----")
            player = Player.objects.filter(identifier=request.data['message']['chat']['id']).first()
            if player:
                print('jogador já existe')
            else:
                TheWorld.getTheWorld().createTerritory(request.data['message']['text'],
                                                       request.data['message']['chat']['id'],
                                                       request.data['message']['from']['username'])
            print("------End update from telegram-----")
        except Exception as e:
            print('MORREU')
            print(e)
        self.telegram.sendMessage(request.data['message']['text'], request.data['message']['chat']['id'])
        return Response(status=status.HTTP_200_OK)
