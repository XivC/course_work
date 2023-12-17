from django.db import models


class Weapon(models.Model):
    name = models.CharField(max_length=255)
    power = models.IntegerField()
    icon = models.URLField(blank=True, null=True)


class Effect(models.Model):
    name = models.CharField(max_length=255)
    power_affect = models.IntegerField()

    def __str__(self):
        return f'{self.name} ({self.power_affect})'


class CreatureEffectRule(models.Model):
    creature_from = models.ForeignKey('creatures.Creature', related_name='+', on_delete=models.CASCADE)
    creature_to = models.ForeignKey('creatures.Creature', related_name='+', on_delete=models.CASCADE)
    effect = models.ForeignKey('affects.Effect', related_name='creatures_rules', on_delete=models.CASCADE)
    is_to_ally = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['effect', 'creature_from', 'creature_to', 'is_to_ally'],
                name='creature_effect_rule_unique',
            )
        ]


class PlanetEffectRule(models.Model):
    planet = models.ForeignKey('planets.Planet', related_name='+', on_delete=models.CASCADE)
    creature_to = models.ForeignKey('creatures.Creature', related_name='+', on_delete=models.CASCADE)
    effect = models.ForeignKey('affects.Effect', related_name='planets_rules', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['planet', 'effect', 'creature_to'],
                name='planet_effect_rule_unique',
            )
        ]
