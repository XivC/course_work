from rest_framework.viewsets import ModelViewSet

from course_work.security import make_readonly_permissions
from creatures.models import Creature
from creatures.serializers import CreatureSerializer


class CreatureViewSet(ModelViewSet):
    queryset = Creature.objects.all()
    serializer_class = CreatureSerializer

    def get_permissions(self):
        return make_readonly_permissions(self.action)