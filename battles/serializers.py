from rest_framework import serializers

from affects.serializers import WeaponSerializer, EffectSerializer
from battles.models import Battler, BattleMember, BattleReport, BattlerEffect, Battle
from creatures.serializers import ProtectedCreatureSerializer
from planets.serializers import ProtectedPlanetSerializer


class BattlerSerializer(serializers.ModelSerializer):
    weapon = WeaponSerializer(read_only=True)
    creature = ProtectedCreatureSerializer(read_only=True)

    # TODO: add creature serializer

    class Meta:
        model = Battler
        fields = [
            'id',
            'creature',
            'weapon',
        ]


class BattleMemberSerializer(serializers.ModelSerializer):
    battler = BattlerSerializer(read_only=True)

    class Meta:
        model = BattleMember
        fields = [
            'battler',
            'is_opponent',
        ]


class BattleReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BattleReport
        fields = [
            'allies_power',
            'opponents_power',
        ]


class BattlerEffectSerializer(serializers.ModelSerializer):
    effect = EffectSerializer
    battler = BattlerSerializer

    class Meta:
        model = BattlerEffect
        fields = [
            'battler',
            'effect',
        ]


class BattleSerializer(serializers.ModelSerializer):
    planet = ProtectedPlanetSerializer(read_only=True)
    members = serializers.ListSerializer(child=BattleMemberSerializer(), read_only=True)
    applied_effects = serializers.ListSerializer(child=BattlerEffectSerializer(), read_only=True)

    class Meta:
        model = Battle
        fields = [
            'applied_effects',
            'planet',
            'members',
            'created_at',
        ]
