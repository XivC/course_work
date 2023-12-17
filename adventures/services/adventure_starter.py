from dataclasses import dataclass
from functools import cached_property
from typing import Callable

from django.db.models import QuerySet
from django.db.transaction import atomic
from rest_framework.exceptions import ValidationError

from adventures.models import Adventure, Team, AdventurePlanet, Teammate
from affects.models import Weapon
from battles.models import Battler
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

    @atomic
    def action(self) -> Adventure:
        adventure = self.create_adventure()
        team = self.create_team(adventure=adventure)
        battlers = self.create_battlers(adventure=adventure)
        self.create_teammates(team, battlers)

        return adventure

    def create_adventure(self) -> Adventure:
        adventure = Adventure.objects.create(
            name=self.data['adventure_name']
        )

        adventure_planets = [
            AdventurePlanet(
                adventure=adventure,
                planet=planet,
                is_visited=False,
            ) for planet in self.planets
        ]
        AdventurePlanet.objects.bulk_create(adventure_planets)

        return adventure

    def create_team(self, adventure: Adventure) -> Team:
        return Team.objects.create(
            name=self.data['team_name'],
            adventure=adventure,
        )

    def create_battlers(self, adventure: Adventure) -> list[Battler]:
        battlers = []
        for creature_id, weapon_id in zip(self.creatures_ids, self.weapons_ids):
            battlers.append(
                Battler(
                    creature_id=creature_id,
                    weapon_id=weapon_id,
                    adventure=adventure,
                )
            )

        Battler.objects.bulk_create(battlers)
        return battlers

    def create_teammates(self, team: Team, battlers: list[Battler]) -> None:
        mates = []
        for battler in battlers:
            mates.append(
                Teammate(
                    team=team,
                    battler=battler,
                )
            )
        Teammate.objects.bulk_create(mates)

    @property
    def planets_ids(self) -> list[int]:
        return self.data['planets']

    @property
    def creatures_ids(self) -> list[int]:
        return [row['creature'] for row in self.data['creatures_with_weapons']]

    @property
    def weapons_ids(self) -> list[int | None]:
        return [row['weapon'] for row in self.data['creatures_with_weapons']]

    @cached_property
    def planets(self) -> QuerySet[Planet]:
        return Planet.objects.filter(id__in=self.planets_ids)

    @cached_property
    def creatures(self) -> QuerySet[Creature]:
        return Creature.objects.filter(id__in=self.creatures_ids)

    @cached_property
    def weapons(self) -> QuerySet[Weapon]:
        return Weapon.objects.filter(id__in=self.weapons_ids)

    def validate_planets_universes(self):
        universes = {planet.universe_id for planet in self.planets}
        if len(universes) > 1:
            raise ValidationError('All planets must be from one universe')

    def validate_creatures_universes(self):
        universes = {planet.universe_id for planet in self.planets}
        if len(universes) > 1:
            raise ValidationError('All planets must be from one universe')

    def get_validators(self) -> list[Callable]:
        return [
            lambda: validate_primary_key(Planet, self.planets_ids),
            lambda: validate_primary_key(Creature, self.creatures_ids),
            lambda: validate_primary_key(Weapon, self.weapons_ids),
            self.validate_creatures_universes,
            self.validate_planets_universes,
        ]
