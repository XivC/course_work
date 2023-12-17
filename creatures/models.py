from django.db import models


class Creature(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    power = models.PositiveIntegerField()
    icon = models.URLField(blank=True, null=True)
    planet = models.ForeignKey('planets.Planet', on_delete=models.CASCADE, related_name='creatures')

    def __str__(self):
        return self.name
