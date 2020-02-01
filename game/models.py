from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    nome = models.CharField(max_length=255, null=False)
    

    
class Soldado(models.Model):
    quantidade = models.IntegerField(max_length=4, null=False)
    
    def atacar(self, body):
        if body.instanceOff(Soldado):
            pass

class Comando(models.Model):
    origem = models.CharField(max_length=255, null=False)
    destino = models.CharField(max_length=255, null=False)
    acao = models.CharField(max_length=255, null=False)
    sujeito = models.CharField(max_length=255, null=False)

class Transporte(models.Model):
    comando = models.OneToOneField('Comando', related_name="transporte-comando", on_delete = models.CASCADE)
    tempo = models.CharField(max_length=255, null=False)
    
