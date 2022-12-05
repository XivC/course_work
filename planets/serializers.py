from rest_framework import serializers

from planets.models import Universe, Planet


class ProtectedPlanetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planet
        fields = [
            'id',
            'name',
        ]


class ProtectedUniverseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Universe
        fields = [
            'id',
            'name'
        ]


class PlanetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Planet
        fields = [
            'id',
            'name',
            'universe',
        ]


class UniverseSerializer(serializers.ModelSerializer):
    planets = serializers.ListSerializer(
        child=ProtectedPlanetSerializer(),
        read_only=True,
    )

    class Meta:
        model = Universe
        fields = [
            'id',
            'name',
            'planets',
        ]
