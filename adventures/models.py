from django.db import models


class Adventure(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)
    is_successful = models.BooleanField(null=True)


class AdventurePlanet(models.Model):
    adventure = models.ForeignKey('adventures.Adventure', related_name='adventure_planets', on_delete=models.CASCADE)
    planet = models.ForeignKey('planets.Planet', related_name='+', on_delete=models.CASCADE)
    is_visited = models.BooleanField(default=False)


class Team(models.Model):
    name = models.CharField(max_length=255)
    adventure = models.OneToOneField('adventures.Adventure', on_delete=models.CASCADE)


class Teammate(models.Model):
    team = models.ForeignKey('adventures.Team', on_delete=models.CASCADE, related_name='teammates')
    battler = models.ForeignKey('battles.Battler', on_delete=models.CASCADE, related_name='+')
