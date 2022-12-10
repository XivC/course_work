from rest_framework.viewsets import ModelViewSet

from creatures.models import Creature
from creatures.serializers import CreatureSerializer


class CreatureViewSet(ModelViewSet):
    queryset = Creature.objects.all()
    serializer_class = CreatureSerializer
