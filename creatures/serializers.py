from rest_framework import serializers

from creatures.models import Creature


class ProtectedCreatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creature
        fields = [
            'id',
            'name',
            'power',
            'icon'
        ]


class CreatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creature
        fields = [
            'id',
            'name',
            'power',
            'icon',
            'planet'
        ]
