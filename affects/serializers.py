from rest_framework import serializers

from affects.models import CreatureEffectRule
from affects.models import Effect
from affects.models import PlanetEffectRule
from affects.models import Weapon


class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = '__all__'


class EffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Effect
        fields = '__all__'


class CreatureEffectRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreatureEffectRule
        fields = '__all__'


class PlanetEffectRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetEffectRule
        fields = '__all__'
