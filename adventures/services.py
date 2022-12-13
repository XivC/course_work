from dataclasses import dataclass

from rest_framework.exceptions import ValidationError

from adventures.models import Adventure
from affects.models import Weapon
from battles.models import Battle
from course_work.storage import FunctionCaller
from creatures.models import Creature
from planets.models import Planet


@dataclass
class AdventureStarter:
    data: dict

    def validate_primary_key(self, clazz, keys):
        keys = list(filter(lambda x: x is not None, keys))
        if not keys:
            return
        qs = clazz.objects.filter(id__in=keys)
        if len(qs) != len(keys):
            raise ValidationError('Invalid data')

    def __call__(self):
        planets = self.data['planets']
        creatures = [row['creature'] for row in self.data['creatures_with_weapons']]
        weapons = [row['weapon'] for row in self.data['creatures_with_weapons']]

        self.validate_primary_key(Planet, planets)
        self.validate_primary_key(Creature, creatures)
        self.validate_primary_key(Weapon, weapons)

        adventure_id = FunctionCaller(
            function='create_adventure',
            args=[
                self.data['adventure_name'],
                self.data['team_name'],
                planets,
                creatures,
                weapons,
            ]
        )()[0]
        return Adventure.objects.get(id=adventure_id)


@dataclass
class AdventureStepper:
    adventure: Adventure

    def __call__(self):
        battle_id = FunctionCaller(
            function='adventure_step',
            args=[
                self.adventure.id,
            ]
        )()[0]
        return Battle.objects.get(id=battle_id)
