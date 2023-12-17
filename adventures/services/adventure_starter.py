from dataclasses import dataclass
from functools import cached_property
from typing import Callable

from rest_framework.exceptions import ValidationError

from adventures.models import Adventure
from affects.models import Weapon
from course_work.services import ServiceBase
from course_work.storage import FunctionCaller
from creatures.models import Creature
from planets.models import Planet


def validate_primary_key(clazz, keys):
    """
    A bit of optimization hack. Default PrimaryKeyRelatedField django validation will make a new DB request for every entity.
    Here we can check all PKs by 1 request.
    """
    keys = list(filter(lambda x: x is not None, keys))
    if not keys:
        return
    qs = clazz.objects.filter(id__in=keys)
    if len(qs) != len(keys):
        raise ValidationError(f'Objects ({keys}) of type {clazz.__name__} not found')


@dataclass
class AdventureStarter(ServiceBase):
    data: dict

    def action(self):
        adventure_id = FunctionCaller(
            function='create_adventure',
            args=[
                self.data['adventure_name'],
                self.data['team_name'],
                self.planets,
                self.creatures,
                self.weapons,
            ]
        )()[0]
        return Adventure.objects.get(id=adventure_id)

    @cached_property
    def planets(self) -> list[int]:
        return self.data['planets']

    @cached_property
    def creatures(self) -> list[int]:
        return [row['creature'] for row in self.data['creatures_with_weapons']]

    @cached_property
    def weapons(self) -> list[int]:
        return [row['weapon'] for row in self.data['creatures_with_weapons']]

    def get_validators(self) -> list[Callable]:
        return [
            lambda: validate_primary_key(Planet, self.planets),
            lambda: validate_primary_key(Creature, self.creatures),
            lambda: validate_primary_key(Weapon, self.weapons),
        ]
