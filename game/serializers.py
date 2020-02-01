from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['url', 'name', 'identifier']


class SoldierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Soldier
        fields = ['url', 'name', 'category']


class CommandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Command
        fields = ['url', 'origin', 'target', 'action', 'soldier', 'type']


class TransmissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transmission
        fields = ['url', 'command', 'time', 'cost']


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ['url', 'text', 'identifier']

class TelegramUpdateSerializer(serializers.Serializer):
    def validate(self, attrs):
        text = self.initial_data.__str__()
        print(text)
        return True