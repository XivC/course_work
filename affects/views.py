from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from affects.models import CreatureEffectRule
from affects.models import Effect
from affects.models import PlanetEffectRule
from affects.models import Weapon
from affects.serializers import CreatureEffectRuleSerializer
from affects.serializers import EffectSerializer
from affects.serializers import PlanetEffectRuleSerializer
from affects.serializers import WeaponSerializer


class WeaponViewSet(ModelViewSet):
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializer


class EffectViewSet(ModelViewSet):
    queryset = Effect.objects.all()
    serializer_class = EffectSerializer


class PlanetEffectRuleViewSet(ModelViewSet):
    queryset = PlanetEffectRule.objects.all()
    serializer_class = PlanetEffectRuleSerializer

    @property
    def effect(self):
        return get_object_or_404(Effect.objects.all(), id=self.kwargs.get('effect_pk'))

    def get_queryset(self):
        return super().get_queryset().filter(effect=self.effect)


class CreatureEffectRuleViewSet(ModelViewSet):
    queryset = CreatureEffectRule.objects.all()
    serializer_class = CreatureEffectRuleSerializer

    @property
    def effect(self):
        return get_object_or_404(Effect.objects.all(), id=self.kwargs.get('effect_pk'))

    def get_queryset(self):
        return super().get_queryset().filter(effect=self.effect)
