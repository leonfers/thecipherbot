from rest_framework import viewsets, status
from rest_framework.response import Response

from game.serializers import CommandSerializer, Command, Profile, ProfileSerializer, SoldierSerializer, Soldier, \
    TransmissionSerializer, Transmission, Message, MessageSerializer


class CommandViewset(viewsets.ModelViewSet):
    queryset = Command.objects.all()
    serializer_class = CommandSerializer


class ProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class SoldierViewset(viewsets.ModelViewSet):
    queryset = Soldier.objects.all()
    serializer_class = SoldierSerializer


class TransmissionViewset(viewsets.ModelViewSet):
    queryset = Transmission.objects.all()
    serializer_class = TransmissionSerializer


class MessageViewset(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class TelegramUpdate(viewsets.ViewSet):
    def create(self, request, pk=None):
        print(request.data)
        return Response(status=status.HTTP_200_OK)
