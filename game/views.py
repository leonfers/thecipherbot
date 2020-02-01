from rest_framework import viewsets

from game.serializers import CommandSerializer, Command, Profile, ProfileSerializer, SoldierSerializer, Soldier, \
    TransmissionSerializer, Transmission, Message, MessageSerializer


class Commands(viewsets.ModelViewSet):
    queryset = Command.objects.all()
    serializer_class = CommandSerializer


class Profiles(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class Soldiers(viewsets.ModelViewSet):
    queryset = Soldier.objects.all()
    serializer_class = SoldierSerializer


class Transmissions(viewsets.ModelViewSet):
    queryset = Transmission.objects.all()
    serializer_class = TransmissionSerializer


class Messages(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
