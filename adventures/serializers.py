from rest_framework import serializers

from adventures.models import Adventure
from adventures.models import Team
from battles.serializers import BattlerSerializer
from planets.serializers import PlanetSerializer


class TeamSerializer(serializers.ModelSerializer):
    mates = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            'name',
            'mates',
        ]

    def get_mates(self, instance: Team):
        return BattlerSerializer(
            [teammate.battler for teammate in instance.teammates.all()],
            many=True,
        ).data


class AdventureSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    planets = serializers.SerializerMethodField()

    class Meta:
        model = Adventure
        fields = [
            'id',
            'created_at',
            'started_at',
            'finished_at',
            'is_successful',
            'team',
            'planets',
        ]

    def get_planets(self, instance: Adventure):
        return PlanetSerializer([ap.planet for ap in instance.adventure_planets.all()], many=True).data


class CreatureWithWeaponSerializer(serializers.Serializer):
    creature = serializers.IntegerField()
    weapon = serializers.IntegerField(allow_null=True)


class EditAdventureSerializer(serializers.Serializer):
    adventure_name = serializers.CharField(max_length=255)
    team_name = serializers.CharField(max_length=255)
    planets = serializers.ListField(child=serializers.IntegerField())
    creatures_with_weapons = CreatureWithWeaponSerializer(many=True)
