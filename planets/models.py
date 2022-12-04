from django.db import models


class Universe(models.Model):
    name = models.CharField(max_length=255)


class Planet(models.Model):
    name = models.CharField(max_length=255)
    universe = models.ForeignKey('planets.Universe', related_name='planets', on_delete=models.CASCADE)
