from dataclasses import dataclass

from rest_framework.exceptions import ValidationError

from adventures.models import Adventure
from battles.models import Battle
from course_work.services import ServiceBase
from course_work.storage import FunctionCaller


@dataclass
class AdventureStepper(ServiceBase):
    adventure: Adventure

    def action(self):
        battle_id = FunctionCaller(
            function='adventure_step',
            args=[
                self.adventure.id,
            ]
        )()[0]
        try:
            return Battle.objects.get(id=battle_id)
        except Battle.DoesNotExist:
            raise ValidationError('Adventure already finished')
