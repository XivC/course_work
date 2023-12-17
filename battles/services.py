from dataclasses import dataclass

from django.db.transaction import atomic

from adventures.models import Adventure
from affects.models import Weapon
from battles.models import Battler
from course_work.services import ServiceBase
from creatures.models import Creature


@dataclass
class BattlersBulkCreator(ServiceBase):
    creatures: list[Creature]
    weapons: list[Weapon]
    adventure: Adventure
    @atomic
    def action(self) -> list[Battler]:
        battlers = []
        self.weapons += [None] * (len(self.creatures) - len(self.weapons))
        for creature, weapon in zip(self.creatures, self.weapons):
            battlers.append(
                Battler(
                    creature=creature,
                    weapon=weapon,
                    adventure=self.adventure,
                )
            )
        Battler.objects.bulk_create(battlers, ignore_conflicts=True)
        return list(Battler.objects.filter(creature__in=self.creatures, adventure=self.adventure))
