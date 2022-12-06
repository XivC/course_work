from rest_framework import serializers

from affects.models import Weapon, Effect, CreatureEffectRule, PlanetEffectRule


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
