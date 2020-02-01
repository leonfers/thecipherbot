from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response

from game.theworld import TheWorld
from telegramapi.models import TelegramApi


class TelegramUpdate(viewsets.ViewSet):
    telegram = TelegramApi.getService()
    the_world = TheWorld()

    def create(self, request):
        print("------New update from telegram-----")

        self.telegram.sendMessage(request.data['message']['text'], request.data['message']['chat']['id'])
        return Response(status=status.HTTP_200_OK)

