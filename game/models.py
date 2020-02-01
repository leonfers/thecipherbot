from django.db import models
from django.contrib.auth.models import User

from .theworld import TheWorld


class Territory(models.Model):
    name = models.CharField(max_length=255, null=False)
    world = models.ForeignKey(TheWorld, related_name='territories', on_delete=models.CASCADE)


class Field(models.Model):
    name = models.CharField(max_length=255, null=False)
    territory = models.ForeignKey(Territory, related_name='fields', on_delete=models.CASCADE)


class Player(models.Model):
    name = models.CharField(max_length=255, null=False)
    identifier = models.CharField(max_length=255, null=False)
    territory = models.ForeignKey(Territory, related_name='players', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


UNIT_TYPES = (('P', 'Peon'), ('S', 'Spy'),)


class Unit(models.Model):
    name = models.CharField(max_length=255, null=False)
    category = models.CharField(max_length=255, choices=UNIT_TYPES, null=False)
    field = models.ForeignKey(Field, related_name='units', on_delete=models.CASCADE)
    player = models.ForeignKey(Player,related_name='units',on_delete=models.CASCADE)

    def action(self):
        pass

    def __str__(self):
        return self.name + self.category[1]


COMMAND_TYPE = (('F', 'FAKE'), ('R', 'REAL'))


class Command(models.Model):
    type = models.CharField(max_length=255, choices=COMMAND_TYPE, null=False)
    origin = models.CharField(max_length=255, null=False)
    target = models.CharField(max_length=255, null=False)
    action = models.CharField(max_length=255, null=False)
    soldier = models.ForeignKey(Unit, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.origin + self.target + self.action + str(self.soldier)

    def execute(self):
        print("Teste " + self)


TRANSMISSION_STATUS = (('C', 'COMPLETED'), ('I', 'INTERCEPTED'), ('T', 'TRANSIT'), ('D', 'DAMAGED'))


class Transmission(models.Model):
    command = models.OneToOneField('Command', on_delete=models.DO_NOTHING)
    time_in_minutes = models.IntegerField(null=False)
    status = models.CharField(max_length=255, choices=TRANSMISSION_STATUS, null=False)
    cost = models.IntegerField(null=False)

    def __str__(self):
        return str(self.command) + str(self.time_in_minutes) + str(self.status) + str(self.cost)


class Message(models.Model):
    text = models.CharField(max_length=400, null=False)
    identifier = models.IntegerField(null=False)
    date = models.DateTimeField()
