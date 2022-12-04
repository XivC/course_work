from django.db import models


class Battler(models.Model):
    creature = models.ForeignKey('creatures.Creature', related_name='+', on_delete=models.CASCADE)
    adventure = models.ForeignKey('adventures.Adventure', related_name='battlers', on_delete=models.CASCADE)
    weapon = models.ForeignKey('affects.Weapon', related_name='+', on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['creature', 'adventure'],
                name='creature_to_adv_unique',
            )
        ]


class Battle(models.Model):
    adventure = models.ForeignKey('adventures.Adventure', related_name='battles', on_delete=models.CASCADE)
    planet = models.ForeignKey('planets.Planet', related_name='+', on_delete=models.CASCADE)
    created_at = models.DateTimeField()


class BattleMember(models.Model):
    battle = models.ForeignKey('battles.Battle', related_name='members', on_delete=models.CASCADE)
    battler = models.ForeignKey('battles.Battler', related_name='+', on_delete=models.CASCADE)
    is_opponent = models.BooleanField()


class BattleReport(models.Model):
    battle = models.OneToOneField('battles.Battle', on_delete=models.CASCADE, related_name='report')
    allies_power = models.PositiveIntegerField()
    opponents_power = models.PositiveIntegerField()


class BattlerEffect(models.Model):
    battle = models.ForeignKey('battles.Battle', related_name='+', on_delete=models.CASCADE)
    battler = models.ForeignKey('battles.Battler', related_name='effects', on_delete=models.CASCADE)
    effect = models.ForeignKey('affects.Effect', related_name='+', on_delete=models.CASCADE)
