from multiprocessing import Pool
from random import randrange

from django.db import models

from game.models import Territory, Field, Player, Unit, UNIT_TYPES


