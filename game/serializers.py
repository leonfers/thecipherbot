from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *


class PerfilSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Perfil
        fields = ['url', 'nome']
    

class SoldadoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Soldado
        fields = ['url', 'quantidade']


class ComandoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comando
        fields = ['url', 'origem', 'destino', 'acao', 'sujeito' ]


class TransporteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transporte
        fields = ['url', 'comando', 'tempo']